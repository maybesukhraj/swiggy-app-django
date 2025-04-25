from django.db import models
from django.contrib.auth.models import User
from orders.models import Restaurant

class RestaurantManagement(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='management')
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/')
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Management for {self.restaurant.name}"
