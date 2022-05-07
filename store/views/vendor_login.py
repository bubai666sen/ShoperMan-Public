from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from store.models.vendor import Vendor
from django.views import View


class VendorLogin(View):
    return_url = None

    def get(self, request):
        VendorLogin.return_url = request.GET.get ('return_url')
        return render (request, 'vendor-login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        vendor = Vendor.get_vendor_by_email (email)
        error_message = None
        if vendor:
            flag = check_password (password, vendor.password)
            if flag:
                request.session['vendor'] = vendor.id

                if VendorLogin.return_url:
                    return HttpResponseRedirect (VendorLogin.return_url)
                else:
                    VendorLogin.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'vendor-login.html', {'error': error_message})

def vendorLogout(request):
    request.session.clear()
    return redirect('vendor-login')
