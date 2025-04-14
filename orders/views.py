from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from .models import Order

# Restaurant data
restaurants = {
    'Spicy Bites': {
        'description': "Authentic Indian flavors!",
        'menu': {'Biryani': 12, 'Noodles': 10, 'Paneer Tikka': 8},
        'image_url': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg',
        'delivery_time': '30-40 min',
        'rating': 4.5
    },
    'Pasta Palace': {
        'description': "Delicious Italian dishes.",
        'menu': {'Pasta Alfredo': 15, 'Garlic Bread': 5, 'Lasagna': 18},
        'image_url': 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg',
        'delivery_time': '25-35 min',
        'rating': 4.7
    },
    'Burger Hub': {
        'description': "Juicy burgers & crispy fries!",
        'menu': {'Cheeseburger': 8, 'Fries': 4, 'Milkshake': 6},
        'image_url': 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d',
        'delivery_time': '20-30 min',
        'rating': 4.3
    },
    'Sushi World': {
        'description': "Fresh sushi & Japanese delights.",
        'menu': {'Sushi Roll': 20, 'Miso Soup': 7, 'Tempura': 12},
        'image_url': 'https://images.pexels.com/photos/4198023/pexels-photo-4198023.jpeg',
        'delivery_time': '40-50 min',
        'rating': 4.8
    },
    'Taco Fiesta': {
        'description': "Delicious Mexican street food.",
        'menu': {'Tacos': 10, 'Quesadilla': 8, 'Nachos': 9},
        'image_url': 'https://images.unsplash.com/photo-1600891964599-f61ba0e24092',
        'delivery_time': '15-25 min',
        'rating': 4.6
    },
    'Healthy Greens': {
        'description': "Fresh & organic meals.",
        'menu': {'Salad Bowl': 12, 'Smoothie': 6, 'Avocado Toast': 10},
        'image_url': 'https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg',
        'delivery_time': '20-30 min',
        'rating': 4.9
    }
}

def index(request):
    return redirect('home' if request.user.is_authenticated else 'login')

@login_required
def home(request):
    current_year = timezone.now().year
    return render(request, 'orders/index.html', {'restaurants': restaurants, 'current_year': current_year})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'orders/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            next_page = request.GET.get('next')
            return redirect(next_page if next_page else 'home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        restaurant_name = request.POST.get('restaurant')
        food_item = request.POST.get('food')
        quantity = int(request.POST.get('quantity'))
        
        # Calculate price
        price_per_item = restaurants[restaurant_name]['menu'][food_item]
        total_price = price_per_item * quantity
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            name=name,
            contact=contact,
            restaurant=restaurant_name,
            food_item=food_item,
            quantity=quantity,
            total_price=total_price
        )
        
        # Store order details in session for success page
        request.session['order_details'] = {
            'name': name,
            'contact': contact,
            'restaurant': restaurant_name,
            'food_item': food_item,
            'quantity': quantity,
            'total_price': total_price,
            'order_id': order.id
        }
        
        return render(request, 'orders/bill.html', {
            'name': name,
            'contact': contact,
            'restaurant': restaurant_name,
            'food_item': food_item,
            'quantity': quantity,
            'total_price': total_price
        })
    
    return render(request, 'orders/order.html', {'restaurants': restaurants})

@login_required
def success(request):
    # Get order details from session
    order_details = request.session.get('order_details', {})
    if not order_details:
        messages.error(request, "No order information found.")
        return redirect('home')
    
    return render(request, 'orders/success.html', order_details)

@login_required
def history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders/history.html', {'orders': orders})
