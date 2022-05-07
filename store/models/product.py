from django.db import models
from .category import Category
from .vendor import Vendor
from .tags import Tag
from tinymce.models import HTMLField
from django import forms

class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    description= HTMLField(null=True, blank=True)
    vendor= models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True, blank=True)
    image= models.ImageField(upload_to='uploads/products/')
    tags= models.ManyToManyField(Tag,blank=True)

    def tag_names(self):
        return ' , '.join([a.name for a in self.tags.all()])
    tag_names.short_description = "Tag Names"

    def tagCount(self,l):
        input_list = [] 
        [input_list.append(x) for x in l if x not in input_list]
        product_list = [] 
        [product_list.append(x) for x in self.tag_names().strip(' , ').split(' , ') if x not in product_list]
        tag_count = 0 
        for item in product_list:
            tag_count += input_list.count(item)
        return tag_count
    tagCount.short_description = "Number of tags matched against given list"

    def __str__(self):           
        return str(self.name)

    
        

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids).order_by('-id')
    @staticmethod
    def get_all_products():
        return Products.objects.all().order_by('-id')

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id).order_by('-id')
        else:
            return Products.get_all_products();

    @staticmethod
    def get_products_by_vendor(vendor_id):
        return Products.objects.filter (vendor=vendor_id).order_by('-id')

    class Meta:
        verbose_name_plural = "Products"

# create a ModelForm
class ProductForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Products
        fields = [ 'name', 'price', 'category', 'description'  , 'image',  'tags' ]