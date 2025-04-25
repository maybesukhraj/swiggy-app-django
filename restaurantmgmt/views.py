from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from orders.models import Restaurant
from .models import RestaurantManagement
from .forms import RestaurantForm, RestaurantManagementForm

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurantmgmt/list.html'
    context_object_name = 'restaurants'

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurantmgmt/form.html'
    success_url = reverse_lazy('restaurantmgmt:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['management_form'] = RestaurantManagementForm(self.request.POST, self.request.FILES)
        else:
            context['management_form'] = RestaurantManagementForm()
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        restaurant = form.save()
        management_form = RestaurantManagementForm(self.request.POST, self.request.FILES)
        if management_form.is_valid():
            management = management_form.save(commit=False)
            management.restaurant = restaurant
            management.created_by = self.request.user
            management.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurantmgmt/form.html'
    success_url = reverse_lazy('restaurantmgmt:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['management_form'] = RestaurantManagementForm(
                self.request.POST, 
                self.request.FILES,
                instance=self.object.management if hasattr(self.object, 'management') else None
            )
        else:
            context['management_form'] = RestaurantManagementForm(
                instance=self.object.management if hasattr(self.object, 'management') else None
            )
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        restaurant = form.save()
        management_form = RestaurantManagementForm(
            self.request.POST, 
            self.request.FILES,
            instance=restaurant.management if hasattr(restaurant, 'management') else None
        )
        if management_form.is_valid():
            management = management_form.save(commit=False)
            if not hasattr(restaurant, 'management'):
                management.restaurant = restaurant
                management.created_by = self.request.user
            management.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

class RestaurantDeleteView(LoginRequiredMixin, DeleteView):
    model = Restaurant
    template_name = 'restaurantmgmt/confirm_delete.html'
    success_url = reverse_lazy('restaurantmgmt:list')
