from django.db import models
from .category import Category
from .tags import Tag
from tinymce.models import HTMLField

class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    description= HTMLField(null=True, blank=True)
    image= models.ImageField(upload_to='uploads/products/')
    tags= models.ManyToManyField(Tag,blank=True)

    def tag_names(self):
        return ', '.join([a.name for a in self.tags.all()])
    tag_names.short_description = "Tag Names"

    def __str__(self):           
        return str(self.name)

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id)
        else:
            return Products.get_all_products();

    class Meta:
        verbose_name_plural = "Products"
