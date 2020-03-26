from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.decorators.debug import sensitive_post_parameters

from core.models import Restaurant, User
from api.serializers import RestaurantSerializer
from .filters import RestaurantFilter
from .forms import LoginForm, CreateUserForm, RestaurantForm, SearchForm


class IndexView(TemplateView):
    """View that displays initial entrypoint into app"""
    template_name = "index.html"

    def get(self, request):
        form = SearchForm()
        return render(request, self.template_name, {
            'form': form
        })


class SearchView(TemplateView):
    """View that displays initial entrypoint into app"""
    template_name = "table.html"

    def get(self, request):
        form = SearchForm()
        restaurants = RestaurantFilter(request.GET, queryset=Restaurant.objects.all())
        serializer = RestaurantSerializer(instance=restaurants.qs, many=True)
        return render(request, self.template_name, {
            'form': form,
            'restaurants': serializer.data
        })


class LoginView(View):
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = LoginForm(request)

        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():

            # Determine where to direct user after successful login
            redirect_to = request.POST.get('next', '')
            if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
                redirect_to = reverse('ui:index')

            # Authenticate user
            auth_login(request, form.get_user())
            messages.info(request, "Logged in as {}.".format(request.user))

            return HttpResponseRedirect(redirect_to)

        return render(request, self.template_name, {
            'form': form,
        })


class LogoutView(View):

    def get(self, request):

        # Log out the user
        auth_logout(request)
        messages.info(request, "You have logged out.")

        # Delete session key cookie (if set) upon logout
        response = HttpResponseRedirect(reverse('ui:index'))
        response.delete_cookie('session_key')

        return response


class GetReturnURLMixin(object):
    """
    Provides logic for determining where a user should be redirected after processing a form.
    """
    default_return_url = None

    def get_return_url(self, request, obj=None):

        # First, see if `return_url` was specified as a query parameter or form data. Use this URL only if it's
        # considered safe.
        query_param = request.GET.get('return_url') or request.POST.get('return_url')
        if query_param and is_safe_url(url=query_param, allowed_hosts=request.get_host()):
            return query_param

        # Next, check if the object being modified (if any) has an absolute URL.
        elif obj is not None and obj.pk and hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()

        # Fall back to the default URL (if specified) for the view.
        elif self.default_return_url is not None:
            return reverse(self.default_return_url)

        # If all else fails, return home. Ideally this should never happen.
        return reverse('index')


class ObjectEditView(GetReturnURLMixin, View):
    """
    Create or edit a single object.

    model: The model of the object being edited
    model_form: The form used to create or edit the object
    template_name: The name of the template
    """
    model = None
    model_form = None
    template_name = 'utilities/obj_edit.html'

    def get_object(self, kwargs):
        # Look up object by slug or PK. Return None if neither was provided.
        if 'slug' in kwargs:
            return get_object_or_404(self.model, slug=kwargs['slug'])
        elif 'pk' in kwargs:
            return get_object_or_404(self.model, pk=kwargs['pk'])
        return self.model()

    def alter_obj(self, obj, request, url_args, url_kwargs):
        # Allow views to add extra info to an object before it is processed. For example, a parent object can be defined
        # given some parameter from the request URL.
        return obj

    def get(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj = self.alter_obj(obj, request, args, kwargs)
        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}
        form = self.model_form(instance=obj, initial=initial_data)

        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })

    def post(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj = self.alter_obj(obj, request, args, kwargs)
        form = self.model_form(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            obj_created = not form.instance.pk
            obj = form.save()

            msg = '{} {}'.format(
                'Created' if obj_created else 'Modified',
                self.model._meta.verbose_name
            )
            if hasattr(obj, 'get_absolute_url'):
                msg = '{} <a href="{}">{}</a>'.format(msg, obj.get_absolute_url(), escape(obj))
            else:
                msg = '{} {}'.format(msg, escape(obj))
            messages.success(request, mark_safe(msg))

            if '_addanother' in request.POST:
                return redirect(request.get_full_path())

            return_url = form.cleaned_data.get('return_url')
            if return_url is not None and is_safe_url(url=return_url, allowed_hosts=request.get_host()):
                return redirect(return_url)
            else:
                return redirect(self.get_return_url(request, obj))

        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })


class CreateUserView(ObjectEditView):
    model = User
    model_form = CreateUserForm
    default_return_url = 'ui:index'

    def post(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj = self.alter_obj(obj, request, args, kwargs)
        form = self.model_form(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            try:
                user = User.objects.create(
                    **{
                        'name': form.data['name'],
                        'email': form.data['email']
                    }
                )
                user.set_password(form.data['password1'])
                user.save()
                messages.success(request, mark_safe(r"{form.data['email']} user created"))
                return HttpResponseRedirect(reverse('ui:index'))
            except:
                messages.error(request, mark_safe(r"{str(form.data)}"))
                return HttpResponseRedirect(reverse('createuser'))
        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })


@method_decorator(login_required, name='dispatch')
class CreateRestaurantView(ObjectEditView):
    model = Restaurant
    model_form = RestaurantForm
    default_return_url = 'ui:index'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj = self.alter_obj(obj, request, args, kwargs)
        form = self.model_form(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            obj_created = not form.instance.pk
            candidate = form.save(commit=False)
            candidate.user = User.objects.get(email=request.user)
            obj = candidate.save()

            msg = '{} {}'.format(
                'Created' if obj_created else 'Modified',
                self.model._meta.verbose_name
            )
            if hasattr(obj, 'get_absolute_url'):
                msg = '{} <a href="{}">{}</a>'.format(msg, obj.get_absolute_url(), escape(obj))
            else:
                msg = '{} {}'.format(msg, escape(obj))
            messages.success(request, mark_safe(msg))

            if '_addanother' in request.POST:
                return redirect(request.get_full_path())

            return_url = form.cleaned_data.get('return_url')
            if return_url is not None and is_safe_url(url=return_url, allowed_hosts=request.get_host()):
                return redirect(return_url)
            else:
                return redirect(self.get_return_url(request, obj))

        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })
