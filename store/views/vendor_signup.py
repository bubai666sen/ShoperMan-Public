from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.vendor import Vendor
from django.views import View


class VendorSignup (View):
    def get(self, request):
        return render (request, 'vendor-signup.html')

    def post(self, request):
        postData = request.POST
        company_name = postData.get ('companyname')
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'company_name': company_name,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        vendor = Vendor (company_name=company_name,
                             first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateVendor (vendor)

        if not error_message:
            print (company_name, first_name, last_name, phone, email, password)
            vendor.password = make_password (vendor.password)
            vendor.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'vendor-signup.html', data)

    def validateVendor(self, vendor):
        error_message = None
        if (not vendor.company_name):
            error_message = "Please Enter your Company Name !!"
        elif (not vendor.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (vendor.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not vendor.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (vendor.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not vendor.phone:
            error_message = 'Enter your Phone Number'
        elif len (vendor.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (vendor.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (vendor.email) < 5:
            error_message = 'Email must be 5 char long'
        elif vendor.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
