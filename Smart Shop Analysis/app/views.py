from django.shortcuts import render,redirect    
from app.models import User,Product,Complaint,SpecialOffer,Cart
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
import uuid
from num2words import num2words
from .helpers import send_forget_password_mail
from decimal import Decimal
from datetime import date

from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def services(request):
    return render(request,"services.html")

def logout(request):
    return render(request,"login.html")

def vendorregister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')
        gmail = request.POST.get('email')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        profile = request.FILES.get('profile')
        vendor=User.objects.filter(email=gmail)
        if vendor:
            messages.error(request,"This Email already Exist")
            return render(request,"vendorreg.html")
        else:
            if pass1 != pass2:
                messages.success(request,"your password doesn't match each other - Enter the same password")
                return render(request,"vendorreg.html")
            else:
                vendorreg = User.objects.create_user(name=name,address=address,phoneno=phoneno,email=gmail,username=username,password=pass1,is_vendor=True,profile=profile)
                vendorreg.save()
                messages.success(request,"Vendor Registered Successfully")
                return redirect("login")
    return render(request,"vendorreg.html")

def customerregister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')
        gmail = request.POST.get('gmail')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        profile = request.FILES.get('profile')
        cust=User.objects.filter(email=gmail)
        if cust:
            messages.error(request,"this user Is already exist")
            return render(request,"customerreg.html")
        else:
            if pass1 != pass2:
                messages.success(request,"your password doesn't match each other - Enter the same password")
                return render(request,"customerreg.html")
            else:
                customerreg = User.objects.create_user(name=name,address=address,phoneno=phoneno,email=gmail,username=username,password=pass1,is_customer=True,profile=profile)
                customerreg.save()
                messages.success(request,"Customer Registered Successfully")
                return redirect("login")
    return render(request,"customerreg.html")

def login1(request):
    if request.method=="POST":
        name=request.POST.get('name')
        password=request.POST.get('password')
        user=authenticate(request,username=name,password=password)
        
        if user is not None:
            login(request,user)
            if request.user.is_vendor:
                print(f"MEDIA_ROOT = {settings.MEDIA_ROOT}")
                print(f"MEDIA_URL = {settings.MEDIA_URL}")
                print("hello")
                return redirect("vendordash")
            elif request.user.is_customer:
                return redirect("customerdash")
        else:
            messages.success(request,"Invalid username / password ")
            return render(request,"login.html")
    return render(request,"login.html")

@login_required  # Requires user authentication
def vendordash(request):
    return render(request,"vendordash.html")

@login_required  # Requires user authentication
def customerdash(request):
    return render(request,"customerdash.html")

@login_required  # Requires user authentication
def addproduct(request):
    if request.method == "POST":
        productname = request.POST.get('product_name')
        # modelnumber = request.POST.get('model_number')
        serialnumber = request.POST.get('serial_number')
        mrp = request.POST.get('mrp')
        # mop = request.POST.get('mop')
        desc = request.POST.get('desc')
        image=request.FILES['image']
        pr1=Product.objects.create(uploaded_by=request.user,product_name=productname,cerial_number=serialnumber,mrp=mrp,product_image=image,desc=desc)
        pr1.save()
        messages.success(request,"Product added Successfully!!!")
        return render(request,"addproduct.html")
    return render(request,"addproduct.html")

@login_required  # Requires user authentication
def view_product(request):
    if request.user.is_vendor:
        product=Product.objects.filter(uploaded_by=request.user)
        if request.method=="POST":
            dele=request.POST.get('delete')
            ob=Product.objects.filter(id=dele)
            ob.delete()
            return render(request,"view_product.html",{'product':product})
        return render(request,"view_product.html",{'product':product})
    
def passwordreset(request):
    if request.method=='POST':
        name=request.POST.get('name')
        ob=User.objects.get(username=name)
        emailid=ob.email
        id=ob.id
        if not User.objects.get(username=name):
             return render(request,'forgot_pass.html')
        else:
            token=str(uuid.uuid4())
            User.objects.all().filter()
            send_forget_password_mail(emailid,token,id)
            return render(request,'emailsent.html')
    return render(request,'forgot_pass.html')

def newpassword(request,token,id1):
    if request.method=="POST":
        user=User.objects.get(id=id1)
        pass1=request.POST.get('password')
        pass2=request.POST.get('password1')
        user.set_password(pass2)
        user.save()
        messages.success(request,"Password changed Successfully!!!")
        return render(request,'newpassword.html')
    return render(request,'newpassword.html')

@login_required  # Requires user authentication
def generate_bill(request):
    if request.method == "POST":
        name = request.POST['name']
        product = request.POST['product']
        mobnum = request.POST['mobNumber']
        discount = request.POST['discount']
        discount = Decimal(discount)
        prod = Product.objects.get(product_name=product)
        mrp = Decimal(prod.mrp) 
        # Access the special offer amount and vendor
        special_offer = SpecialOffer.objects.filter(product=prod).first()
        # Check if special offer exists and is added by the currently logged-in user
        if special_offer and special_offer.vendor_name == request.user:
            offer_amount = special_offer.amount
            offer_amount=Decimal(offer_amount)
        else:
            offer_amount = 0.0
            offer_amount=Decimal(offer_amount)
        amount = prod.mrp - (prod.mrp * Decimal('0.9') / 100) - (prod.mrp * Decimal('0.9') / 100)
        gst = prod.mrp * Decimal('0.9') / 100
        total = mrp  - discount - offer_amount
        print(mrp,discount,offer_amount)     
        return render(request, 'bill_generate.html', {"product": prod, "name": name, "mobnum": mobnum, "date": date.today(), "amount": amount, "gst": gst, "discount": discount, "total": total, "offer_amount": offer_amount})
    return render(request, 'bill_generate.html')

@login_required  # Requires user authentication
def customer_viewproduct(request):
    if request.user.is_customer:
        if request.method=="POST":
            id=request.POST.get("id")
            ob=Product.objects.get(id=id)
            cart_ob=Cart.objects.create(product=ob,added_by=request.user)
            cart_ob.save()
        product=Product.objects.all()
        return render(request,"view_product_user.html",{'product':product})

def complaint(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        print("hello 1")
        com1 = Complaint.objects.create(complaint_by=name,complaint_mail=email,complaint_description=description)
        com1.save()
        print("hello 2")
        return render(request,"contact_us.html")
    return render(request,"contact_us.html")

@login_required  # Requires user authentication
def search_product(request):
    if request.method == "POST":
        search_name = request.POST.get("search_name")
        search_product = Product.objects.all()
        offer = SpecialOffer.objects.all()
        search_products=[]
        if search_name == '':
            return render(request,"search_result.html",{'search_products':search_product})
        else:
            for i in search_product:
                if i.product_name == search_name:
                    search_products.append(i)
            return render(request,"search_result.html",{'search_products':search_products})
    return render(request,"search_product.html")

@login_required  # Requires user authentication
def registeredshops(request):
    if request.user.is_customer:
        user=User.objects.filter(is_vendor=True)
        return render(request,"registered_shops.html",{'user':user})
    return render(request,"registered_shops.html")

@login_required  # Requires user authentication
def profile(request):
    if request.method=="POST":
        pf=request.FILES.get("s-profile")
        name=request.POST.get("s-name")
        cno=request.POST.get("c-no")
        add=request.POST.get("s-add")
        gmail=request.POST.get("gmail")
        user=User.objects.get(id=request.user.id)
        user.profile=pf
        user.name=name
        user.phoneno=cno
        user.address=add
        user.email=gmail
        user.save()
        messages.success(request,"Profile Edited Sucessfully!!!")
        return render(request,"user.html")
    return render(request,"user.html")

@login_required  # Requires user authentication
def edit_product(request,id):
    ob1=Product.objects.get(id=id)
    if request.method == "POST":
        productname = request.POST.get('product_name')
        #modelnumber = request.POST.get('model_number')
        serialnumber = request.POST.get('serial_number')
        mrp = request.POST.get('mrp')
        #mop = request.POST.get('mop')
        desc = request.POST.get('desc')
        image=request.FILES['image']
        ob=Product.objects.get(id=id)
        ob.product_name=productname
        #ob.model_number=modelnumber
        ob.cerial_number=serialnumber
        ob.mrp=mrp
        #ob.mop=mop
        ob.desc=desc
        ob.product_image=image
        ob.save()
        messages.success(request,"Product edited Successfully!!!")
        return render(request,"edit_product.html")
    return render(request,"edit_product.html",{'ob1':ob1})

@login_required  # Requires user authentication
def add_special_product(request):
    if request.method=="POST":
        product_name=request.POST.get("product")
        price=request.POST.get('price')
        offer_name=request.POST.get('offer_name')
        vendor_name = request.user
        ob=Product.objects.get(product_name=product_name)
        print("product found")
        if ob:
            if ob.uploaded_by==request.user:
                spl=SpecialOffer.objects.create(product=ob,amount=price,offer_name=offer_name,vendor_name=vendor_name)
                spl.save()
                messages.success(request,"Offer Added Successfully!!!")
                return render(request,"add_special_offer.html")
        else:
            print("no product")
    return render(request,"add_special_offer.html")

@login_required  # Requires user authentication
def view_spl_offer(request):
    if request.user.is_customer:
        if request.method=="POST":
            id=request.POST.get("id")
            ob=SpecialOffer.objects.get(id=id)
            cart_ob=Cart.objects.create(product=ob.product,added_by=request.user)
            cart_ob.save()
        ob1=SpecialOffer.objects.all()
        return render(request,"view_spl_offer.html",{'pro':ob1})

@login_required  # Requires user authentication
def display_profile(request):
    return render(request,"display_profile.html")

@login_required  # Requires user authentication
def cart(request):
    if request.user.is_customer:
        ob=Cart.objects.filter(added_by=request.user,prebook=False)
        if ob:
            if request.method=="POST":
                id=request.POST.get("book")
               
                cob=Cart.objects.get(id=id)
                cob.prebook=True
                ob1=Product.booked_by=request.user.name
                cob.save()
            return render(request, "cart.html", {'pro': ob})
        else:
            text="no products in cart"
        return render(request,"cart.html" ,{'text':text})

@login_required  # Requires user authentication       
def v_special_offer(request):
    ob=SpecialOffer.objects.filter(vendor_name=request.user)
    if request.method=="POST":
        id=request.POST.get("delete")
        ob2=SpecialOffer.objects.get(id=id)
        ob2.delete()
    return render(request,"vendor_special_offer.html",{'pro':ob})

@login_required  # Requires user authentication       
def view_prebooked(request):
    if request.user.is_customer:
        ob = Cart.objects.filter(added_by=request.user, prebook=True)
        if request.method=="POST":
            id=request.POST.get("remove")
            ob3=Cart.objects.get(id=id)
            ob3.prebook=False
            ob3.save()
            print(id)
        if ob:
            return render(request, "c_preebook.html", {'products': ob})
        else:
            text = "No prebooked products"
            return render(request, "c_preebook.html", {'text': text})

@login_required
def booked_products(request):
    ob= Cart.objects.filter(product__uploaded_by=request.user,prebook=True)
    return render(request, "v_book.html", {'products': ob})
    # ob = Cart.objects.all()
    # l=[]
    # for o in ob:
    #     if o.product.uploaded_by == request.user:
    #         l.append(o)
    # return render(request, "v_book.html", {'products': l})