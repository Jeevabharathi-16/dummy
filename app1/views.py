
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


def product_list(request):
    categories=Category.objects.prefetch_related('products')
    return render(request,'products.html',{'categories':categories})


def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            p_name=name,
            p_price=price,
            p_image=image,
            category=category
        )
        return redirect('product_list')

    return render(request, 'add_product.html', {'cat': categories})

def delete_product(request,pid):
    product = get_object_or_404(Product, id=pid)
    product.delete()
    return redirect('product_list')

def read_products(request):
    products =Product.objects.all()
    return render(request,'read_products.html',{'products':products})


def read_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    invalid_pids = []

    for pid, item in cart.items():
        try:
            product = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            invalid_pids.append(pid)
            continue

        product.quantity = item['quantity']
        product.subtotal = product.p_price * item['quantity']
        total += product.subtotal
        products.append(product)

    for pid in invalid_pids:
        del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })

def add_cart(request,pid):
    cart = request.session.get('cart',{})

    pid=str(pid)

    if pid in cart:
        cart[pid]['quantity'] +=1
    else:
        cart[pid] ={
            'quantity':1
        }
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('product_list')


def increase_cart(request, pid):
    cart = request.session.get('cart', {})
    pid = str(pid)

    if pid in cart:
        cart[pid]['quantity'] += 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('read_cart')

def decrease_cart(request, pid):
    cart = request.session.get('cart', {})
    pid = str(pid)

    if pid in cart:
        cart[pid]['quantity'] -= 1
        if cart[pid]['quantity'] <= 0:
            del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('read_cart')

def remove_cart(request, pid):
    cart = request.session.get('cart', {})
    pid = str(pid)

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('read_cart')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('read_cart')


def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2= request.POST.get('password2')

        if password1!=password2:
            return render(request,'register.html',{"info":"Password does not match with confirm password"})
        else:
            user=User.objects.create_user(username=username,password=password1)
            return redirect('login_user')
    else:
        return render(request,'register.html')


def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            merge_session_to_user(request)
            return redirect('product_list')
        else:
            return render(request,'login_user.html',{"info":"Invalid Credentials"})
    
    else:
        return render(request,"login_user.html")
    

def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def home_display(request):
    return HttpResponse("This is the first page after login is done by you")


@login_required(login_url='login_user')
def add_cart_user(request,pid):
    product=get_object_or_404(Product,id=pid)
    cart,_=Cart.objects.get_or_create(user=request.user)

    cart_item,created= CartItem.objects.get_or_create(cart=cart,product=product)

    if not created:
        cart_item.quantity+=1

    cart_item.save()
    return redirect('product_list')


@login_required(login_url='login_user')
def read_cart_user(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

  
    items = cart.items.all()

    total = 0
    for item in items:
        item.subtotal = item.product.p_price * item.quantity
        total += item.subtotal

    return render(request, 'cart.html', {
        'items': items,'total': total })

    
@login_required(login_url='login_user')
def increase_cart_user(request, pid):
    item = get_object_or_404(CartItem, cart__user=request.user, product_id=pid )
    item.quantity += 1
    item.save()
    return redirect('read_cart_user')


@login_required(login_url='login_user')
def decrease_cart_user(request, pid):
    item = get_object_or_404(CartItem,cart__user=request.user,product_id=pid )

    item.quantity -= 1
    if item.quantity <= 0:
        item.delete()
    else:
        item.save()

    return redirect('read_cart_user')



@login_required(login_url='login_user')
def remove_cart_user(request, pid):
    CartItem.objects.filter(cart__user=request.user,product_id=pid).delete()

    return redirect('read_cart_user')

@login_required(login_url='login_user')
def clear_cart_user(request):
    CartItem.objects.filter(cart__user=request.user).delete()
    return redirect('read_cart_user')


@login_required(login_url='login_user')
def merge_session_to_user(request):
    cart_session = request.session.get('cart', {})

    if not cart_session:
        return

    cart_user, _ = Cart.objects.get_or_create(user=request.user)

    for pid, data in cart_session.items():

        product = Product.objects.get(id=int(pid))

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart_user,
            product=product
        )

        if created:
            cart_item.quantity = data['quantity']
        else:
            cart_item.quantity += data['quantity']

        cart_item.save()

    
    del request.session['cart']
    request.session.modified = True
