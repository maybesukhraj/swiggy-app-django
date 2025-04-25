from django.urls import path
from .views import RestaurantListView, RestaurantCreateView, RestaurantUpdateView, RestaurantDeleteView

app_name = 'restaurantmgmt'

urlpatterns = [
    path('', RestaurantListView.as_view(), name='list'),
    path('create/', RestaurantCreateView.as_view(), name='create'),
    path('<int:pk>/update/', RestaurantUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', RestaurantDeleteView.as_view(), name='delete'),
]
