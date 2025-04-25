from django import forms
from orders.models import Restaurant
from .models import RestaurantManagement

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location']

class RestaurantManagementForm(forms.ModelForm):
    class Meta:
        model = RestaurantManagement
        fields = ['description', 'image', 'rating']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
