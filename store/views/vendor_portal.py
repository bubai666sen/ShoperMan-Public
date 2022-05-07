from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models import customer
from store.models.customer import Customer
from store.models.vendor import Vendor
from django.views import View
from store.models.product import Products , ProductForm
from store.models.tags import Tag
from store.models.orders import Order
from store.models.vendor import Vendor
from store.middlewares.auth import auth_middleware
from django.http import HttpResponseRedirect

class VendorPortalView(View):


    def get(self , request ):
        vendor = request.session.get('vendor')
        products = Products.get_products_by_vendor(vendor)
        order_list = []
        for product in products:
            #print(product)
            orders = Order.get_orders_by_product(product)
            order_list.append(orders)
        #print(order_list)
        
        return render(request , 'vendor-portal.html'  , {'order_list' : order_list,'products':products})

class AddProductView(View):


    def get(self , request ):
        #vendor = Vendor.objects.get(id=request.session.get('vendor'))
        msg = 'Add a Product'
        context ={}
        context['form'] = ProductForm()
        context['msg'] = msg
        return render(request , 'product.html'  , context)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.vendor = Vendor.objects.get(id=request.session.get('vendor'))
            tag_list = request.POST.getlist('tags')
            instance.save()
            instance.tags.set(tag_list)
            return HttpResponseRedirect('/vendor-portal')

        return render(request, self.template_name, {'form': form})