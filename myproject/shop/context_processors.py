from .models import Cart

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.get_total_items()
    elif request.session.session_key:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        cart_count = cart.get_total_items()
    return {'cart_count': cart_count}