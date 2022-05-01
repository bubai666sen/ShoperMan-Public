from django.db import models

class Tag(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_all_tags():
        return Tag.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
