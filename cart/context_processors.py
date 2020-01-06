from .models import *
def add_variable_to_context(request):
    try:
        cart=Cart.objects.get(user=request.user) if request.user.is_authenticated else Cart.objects.get(session_key = request.session.session_key)
    except:
        if not request.session.session_key:
            request.session.save()
        cart = Cart(session_key=request.session.session_key)
        cart.save()
    return {
        'cart': cart
    }    
