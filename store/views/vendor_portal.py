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
from datetime import date
from datetime import timedelta
# MatPlotLib
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

class VendorPortalView(View):


    def get(self , request ):
        vendor = request.session.get('vendor')
        products = Products.get_products_by_vendor(vendor)
        order_list = []
        product_list = []
        sales_list_by_product = []
        customer_list = []
        customer_orders = []
        customer_ordered_amount = []
        for product in products:
            #print(product)
            orders = Order.get_orders_by_product(product)
            order_list.append(orders)
            product_list.append(product.name)
            sales = 0.01
            for order in orders:
                sales += (order.price * order.quantity)
                if(order.customer.email not in customer_list):
                    customer_list.append(order.customer.email)
                    customer_orders.append(Order.objects.filter(product__in=products,customer=order.customer).count())
                    orders_customer = Order.objects.filter(product__in=products,customer=order.customer)
                    customer_sales = 0.0
                    for order in orders_customer:
                        customer_sales += (order.price * order.quantity)
                    customer_ordered_amount.append(customer_sales)
            sales_list_by_product.append(sales)
        
        #print(customer_list)
        #print(customer_orders)
        #print(customer_ordered_amount)
        #print(product_list)
        #print(sales_list_by_product)
        #print(order_list)

        #BarChart
        # Get today's date
        today = date.today()

        day_list = []
        order_qty_list=[]
        for i in range(7):
            day = today - timedelta(days = i)
            day_list.append(day.strftime("%b %d"))
            order_qty_list.append(Order.objects.filter(date=day,product__in=products).count())

        
        sorted_customer_list = [customer_list for _,customer_list in sorted(zip(customer_ordered_amount,customer_list),reverse=True)]
        sorted_customer_ordered_amount = sorted(customer_ordered_amount,reverse=True)
        
        objects = sorted_customer_list[:6]
        y_pos = np.arange(len(objects))
        amount = sorted_customer_ordered_amount[:6]
        plt.clf()
        plt.bar(y_pos, amount, align='center', alpha=1)
        plt.xticks(y_pos, objects)
        plt.ylabel('Ordered Amount')
        plt.title('Customer ordered amount')
        plt.savefig('static/bi/customer_amount_barchart.png')

        sorted_customer_list = [customer_list for _,customer_list in sorted(zip(customer_orders,customer_list),reverse=True)]
        sorted_customer_orders = sorted(customer_orders,reverse=True)

        y = np.array(sorted_customer_orders[:6])
        mylabels = sorted_customer_list[:6]

        plt.clf()
        plt.pie(y, labels = mylabels,autopct='%1.2f%%')
        plt.title('Number of Orders from Customers')
        plt.legend(title = "Customers:")
        plt.savefig('static/bi/customer_order_count_piechart.png')

        objects = day_list[::-1]
        y_pos = np.arange(len(objects))
        qty = order_qty_list[::-1]
        plt.clf()
        plt.bar(y_pos, qty, align='center', alpha=1)
        plt.xticks(y_pos, objects)
        plt.ylabel('Order Quantity')
        plt.title('Ordered Products by time')
        plt.savefig('static/bi/barchart.png')

        sorted_product_list = [product_list for _,product_list in sorted(zip(sales_list_by_product,product_list),reverse=True)]
        sorted_sales_list_by_product = sorted(sales_list_by_product,reverse=True)
        #print(sorted_product_list)
        #print(sorted_sales_list_by_product)

        y = np.array(sorted_sales_list_by_product[:6])
        mylabels = sorted_product_list[:6]

        plt.clf()
        plt.pie(y, labels = mylabels,autopct='%1.2f%%')
        plt.title('Pruducts and Sales')
        plt.legend(title = "Products:")
        plt.savefig('static/bi/piechart.png')
        

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