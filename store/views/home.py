from itertools import product
from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category
from store.models import Order, Customer
from django.views import View


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    recommended_products = []
    all_products = Products.get_all_products()
    ordered_taglist = []
    all_ordered_tags= ''
    ordered_products=[]
    try:
        if request.session['customer']:
            customer = Customer.objects.get(id=request.session['customer'])
            orders = Order.objects.filter(customer=customer)
            print("Hi "+customer.first_name+" "+customer.last_name+". We have some reccomendations for you...")
            for order in orders:
                all_ordered_tags = all_ordered_tags + ' , ' + order.product.tag_names()
                ordered_products.append(order.product.id)
            ordered_taglist= all_ordered_tags.strip(' , ').split(' , ')
        else:
            print("You're not logged in..")
    except:
        print("You're not logged in...")
    for item in all_products:
        if(item.id not in ordered_products):
            dict_item = {'product': item,
                        'match': item.tagCount(ordered_taglist),
                        }
            recommended_products.append(dict_item)
        
    # print(recommended_products)
    # print('===============================================================')
    recommended_products = sorted(recommended_products, key = lambda i: i['match'],reverse=True)[:3]
    print (recommended_products) 
    # print('===============================================================')   

    data = {}
    data['products'] = products
    data['categories'] = categories
    data['recommended_products'] = recommended_products

    return render(request, 'index.html', data)


