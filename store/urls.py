from django.contrib import admin
from django.urls import path
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.vendor_login import vendorLogout , VendorLogin
from .views.vendor_signup import VendorSignup
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.vendor_portal import VendorPortalView , AddProductView
from .middlewares.auth import  auth_middleware, vendor_auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('vendor-signup', VendorSignup.as_view(), name='vendor-signup'),
    path('vendor-login', VendorLogin.as_view(), name='vendor-login'),
    path('vendor-logout', vendorLogout , name='vendor-logout'),
    path('vendor-portal', vendor_auth_middleware(VendorPortalView.as_view()) , name='vendor-portal'),
    path('add-product', vendor_auth_middleware(AddProductView.as_view()) , name='add-product'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
