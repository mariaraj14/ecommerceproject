from django.shortcuts import render,redirect,get_object_or_404
from  shop.models import product
from . models import Cart,Cartitem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def cart__id(request):
    cart1=request.session.session_key
    if not cart1:
        cart1=request.session.create()
    return cart1
def add_cart(request,product_id):
    product1=product.objects.get(id=product_id)
    try:
        cart1=Cart.objects.get(cart_id=cart__id(request))
    except Cart.DoesNotExist:
        cart1=Cart.objects.create(
            cart_id=cart__id(request) )
        cart1.save()
    try:

        cart_item1=Cartitem.objects.get(product=product1,cart=cart1)
        if cart_item1.quantity < cart_item1.product.stock:
         cart_item1.quantity += 1
        cart_item1.save()
    except Cartitem.DoesNotExist:
        cart_item1=Cartitem.objects.create(
            product=product1,
            quantity=1,
            cart=cart1
        )
        cart_item1.save()
    return redirect('cart:cart_detail')
def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=cart__id(request))
        cart_items=Cartitem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            counter+=cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))
def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=cart__id(request))
    product1=get_object_or_404(product,id=product_id)
    cart_item=Cartitem.objects.get(product=product1,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    cart = Cart.objects.get(cart_id=cart__id(request))
    product1 = get_object_or_404(product, id=product_id)
    cart_item = Cartitem.objects.get(product=product1, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')

