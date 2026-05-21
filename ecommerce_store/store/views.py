from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'productDetails.html', {
        'product': product
    })

@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart(request):

    cart = Cart.objects.get(user=request.user)

    items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })

@login_required
def checkout(request):

    cart = Cart.objects.get(user=request.user)

    items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    items.delete()

    return render(request, 'success.html')

def register(request):

    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')

    return render(request, 'register.html', {
        'form': form
    })