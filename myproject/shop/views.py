from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Category, Product, Cart, CartItem, Order, Review
from django.contrib.auth.models import User

def index(request):
    Category.ensure_categories_exist()
    Product.ensure_products_exist()
    
    categories = Category.objects.all()
    new_products = Product.objects.filter(is_new=True, in_stock=True)[:8]
    bestsellers = Product.objects.filter(is_bestseller=True, in_stock=True)[:8]
    reviews = Review.objects.filter(is_verified=True)[:6]
    
    total_reviews = Review.objects.count()
    total_ratings = Review.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'categories': categories,
        'new_products': new_products,
        'bestsellers': bestsellers,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'total_ratings': total_ratings,
        'avg_rating': round(avg_rating, 1),
    }
    return render(request, 'shop/index.html', context)


def catalog(request):
    Category.ensure_categories_exist()
    Product.ensure_products_exist()
    
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)

    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    search = request.GET.get('search')
    if search:
        search = search.lower()
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'new':
        products = products.order_by('-created_at')
    
    context = {
        'categories': categories,
        'products': products,
        'current_category': category_slug,
        'search_query': search,
    }
    return render(request, 'shop/catalog.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'shop/product_detail.html', {'product': product})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают!')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует!')
            return render(request, 'users/register.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        messages.success(request, 'Регистрация успешна! Добро пожаловать в FlowerPower!')
        return redirect('shop:index')
    
    return render(request, 'users/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if request.session.session_key:
                session_cart = Cart.objects.filter(session_key=request.session.session_key).first()
                user_cart, created = Cart.objects.get_or_create(user=user)
                if session_cart:
                    for item in session_cart.items.all():
                        user_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=item.product,
                            defaults={'quantity': item.quantity}
                        )
                        if not created:
                            user_item.quantity += item.quantity
                            user_item.save()
                    session_cart.delete()
            
            messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
            return redirect('shop:index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
    
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('shop:index')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {'orders': orders})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} добавлен в корзину! ({quantity} шт.)')
    return redirect('shop:cart')


def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    return render(request, 'shop/cart.html', {'cart': cart})


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')
    quantity = int(request.POST.get('quantity', 1))
    
    if action == 'set':
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    elif action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()
    
    return redirect('shop:cart')


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if cart.get_total_items() == 0:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('shop:catalog')
    
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment', '')
        
        if not address or not phone:
            messages.error(request, 'Заполните все обязательные поля!')
            return render(request, 'shop/checkout.html', {'cart': cart})
        
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_price=cart.get_total_price(),
            address=address,
            phone=phone,
            comment=comment
        )
        cart.items.all().delete()
        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect('shop:profile')
    
    return render(request, 'shop/checkout.html', {'cart': cart})


@login_required
def add_review(request):
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        text = request.POST.get('text', '')
        
        Review.objects.create(
            user=request.user,
            rating=rating,
            text=text,
            is_verified=True
        )
        messages.success(request, 'Спасибо за ваш отзыв!')
        return redirect('shop:index')
    
    return render(request, 'shop/add_review.html')