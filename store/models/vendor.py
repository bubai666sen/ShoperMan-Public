from django.db import models

class Vendor(models.Model):
    company_name = models.CharField(max_length=50, null=True,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField (max_length=50)
    phone = models.CharField(max_length=10)
    email=models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    #to save the data
    def register(self):
        self.save()

    def __str__(self):           
        return str(self.first_name + ' ' +self.last_name + '(' +self.email+ ')')


    @staticmethod
    def get_vendor_by_email(email):
        try:
            return Vendor.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Vendor.objects.filter(email = self.email):
            return True

        return False