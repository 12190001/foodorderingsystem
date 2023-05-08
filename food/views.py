from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from food.models import CustomUser, MenuItems, OrderItems, Basket, Notification
from food.forms import CustomerForm
from django.conf import settings
import random
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.contrib.auth import authenticate,login,logout
from bson import ObjectId
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\chian\AppData\Local\Tesseract-OCR\tesseract.exe'
import cv2
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
def home(request):
    return render(request, 'index.html', {
        'room_name':'broadcast'
    })

from asgiref.sync import async_to_sync


def sign_up(request):
    if request.method == "POST":
        # form = CustomerForm(request.POST)
        first_name = request.POST['Firstname']
        last_name = request.POST['Lastname']
        email = request.POST['email']
        contact_number = request.POST['contact']
        password = request.POST['password']
        confirm = request.POST['confirmPassword']
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email already exists. Enter another email.")
        ### OTP verification ###
        else:
            try:
                current_site = get_current_site(request)
                subject = 'Food ordering system'
                otp = random.randint(100000, 999999)
                        # email_from = settings.EMAIL_HOST_USER

                message2 = f"Your otp is {otp}. Use it for verification in {current_site.domain}"
                        # First send OTP through email before saving data to Database

                send_mail(
                            subject,
                            message2,
                            settings.EMAIL_HOST_USER,
                            [email],
                            fail_silently = True

                )

                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['email'] = email
                request.session['password1'] = password
                request.session['password2'] = confirm
                request.session['contact'] = contact_number
                request.session['otp'] = str(otp)
                messages.success(request, "OTP has been sent to your mail for verification")
                return redirect('otp')

            except Exception as e:
                        messages.error(request,
                            "Failed to send OTP through Email."+str(e))

    return render(request, 'signup.html')

def verifyotp(request):
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    email = request.session['email']
    password = request.session['password1']
    contact_number = request.session['contact']
    if request.method == 'POST':
        d = request.POST
        for k,v in d.items():
            if k == 'resend':
                try:
                    current_site = get_current_site(request)
                    subject = 'Food ordering system'
                    otp = random.randint(100000, 999999)
                            # email_from = settings.EMAIL_HOST_USER

                    message2 = f"Your otp is {otp}."
                            # First send OTP through email before saving data to Database

                    send_mail(
                                subject,
                                message2,
                                settings.EMAIL_HOST_USER,
                                [email],
                                fail_silently = True

                    )
                    request.session['otp'] = str(otp)
                except Exception as e:
                            messages.error(request,
                                "Failed to send OTP through Email."+str(e))

            if k == 'submit':
                myotp = request.POST.get('otp')
                otp = request.session['otp']

                if str(myotp) == otp:
                    messages.success(
                        request, "OTP verification successful. You may now login to use our services.")

                    CustomUser.objects.create_user(
                        email = email,
                        first_name =first_name,
                        last_name = last_name,
                        password = password,
                        contact_number = contact_number
                    )
                    return redirect('signin')
                else:
                    messages.error(request, 'OTP is incorrect, please try again')
    return render(request, 'otp.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        myuser = authenticate(request, username=email, password=password)

        if myuser is not None:
            login(request, myuser)
            if CustomUser.objects.filter(email = myuser.email).first():
                user = CustomUser.objects.get(email = myuser.email)
                if user.role == 'owner':
                    messages.success(request, "Successfully logged in")
                    return redirect('owner')
                else:
                    messages.success(request, "Successfully logged in")
                    return redirect(f'/dashboard/{user.pk}')
            else:
                messages.error(request, "Email provided is not valid.")
        else:
            messages.error(request,"Incorrect Email or Password")
            return redirect('signin')
    return render(request, 'signin.html')
@login_required
def owner_dashboard(request):
    return render(request, 'owner_final/owner_dashboard.html')

@login_required
def owner_add_manager(request):
    data = ''
    if CustomUser.objects.filter(role='manager').first():
        data = CustomUser.objects.get(role='manager')
    if request.method == 'POST':
        d = request.POST
        for k,v in d.items():
            if k == 'edit':
                manager = CustomUser.objects.get(role = 'manager')
                first_name =request.POST['first_name'] if request.POST['first_name'] else  manager.first_name
                last_name = request.POST['last_name'] if request.POST['last_name'] else manager.last_name
                email = request.POST['email'] if request.POST['email'] else manager.email
                contact = request.POST['contact'] if request.POST['contact'] else manager.contact_number
                manager.first_name = first_name
                manager.last_name = last_name
                manager.email = email
                manager.contact_number = contact
                manager.save()
                messages.success(request, "Manager successfully Updated.")
                return redirect('addmanager')

            if k == 'add':
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                contact = request.POST['contact']
                password = request.POST['password']
                if CustomUser.objects.filter(role = 'manager').first():
                    messages.error(request, "Manager already exists in the system.")
                else:
                    CustomUser.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        contact_number = contact,
                        password = password,
                        role = 'manager'
                    )
                    messages.success(request, "Manager successfully Added.")
                    return redirect('addmanager')
    context = {
        'data':data
    }
    return render(request, 'owner_final/add_manager.html', context)

@login_required
def delete_manager(request):
    CustomUser.objects.filter(role = 'manager').delete()
    messages.success(request, "Manager successfully deleted.")
    return redirect('addmanager')

@login_required
def dashboard(request,object_id):
    return render(request, 'dashboard.html')

@login_required
def menu(request, object_id):
    data = MenuItems.objects.all()
    context = {
        'data':data,
    }
    return render(request, 'menu.html', context)
@login_required
def create_menu(request, object_id):
    if request.method == "POST":
        manager = CustomUser.objects.get(email = request.user)
        item_name = request.POST['name']
        image = request.FILES['image']
        description = request.POST['description']
        price = request.POST['price']
        MenuItems.objects.create(
            manager_id = manager,
            item_name = item_name,
            image = image,
            description = description,
            price = price
        )
        messages.success(request, "Menu successfully added.")

    return render(request, 'Manager/create_menu.html')

@login_required
def delete_menu(request, object_id):
    if request.method == "POST":
        MenuItems.objects.filter(pk = request.POST['delete_id']).delete()
        messages.success(request, "Menu successfully deleted.")
    return redirect('menu')

@login_required
def update_menu(request, object_id, pk):
    data = ''
    data = MenuItems.objects.get(pk = pk)
    if request.method == "POST":
        item_name = request.POST['name'] if request.POST['name'] else data.item_name
        price = request.POST['price'] if request.POST['price'] else data.price
        description = request.POST['description'] if request.POST['description'] else data.description
        item_image = request.FILES['image']
        data.item_name = item_name
        data.price = price
        data.description = description
        data.image = item_image
        data.save()
        messages.success(request, "Menu successfully updated.")
    context = {
        'data':data
    }
    return render(request, 'Manager/edit_menu.html', context)

def add_order(request, object_id, pk):
    cust = CustomUser.objects.get(email = request.user)
    order = MenuItems.objects.get(pk = pk)
    basket = ''
    if Basket.objects.filter(customer_id = CustomUser.objects.get(email = request.user), status = 'Waiting').first():
        basket = Basket.objects.filter(customer_id = CustomUser.objects.get(email = request.user), status = 'Waiting').first()
    else:
        Basket.objects.create(customer_id = CustomUser.objects.get(email = request.user), status = 'Waiting')
        basket = Basket.objects.filter(customer_id = CustomUser.objects.get(email = request.user), status = 'Waiting').first()

    if request.method == 'POST':
        if OrderItems.objects.filter(basket_id = basket, item_name = order.item_name).first():
            messages.error(request, "The item already exists.")
        else:
            OrderItems.objects.create(
                basket_id = basket,
                menu_id = order,
                customer_id = cust,
                item_name = order.item_name,
                quantity = 1,
                image = order.image,
                price = order.price
            )
            messages.success(request, "Order successfully added.")
    return redirect(f'/dashboard/{object_id}/menu/')


def confirm_order(request, object_id):
    import  json
    cust = CustomUser.objects.get(email = request.user)
    basket = Basket.objects.filter(customer_id = CustomUser.objects.get(email = request.user), status = 'Waiting').first()
    if request.method == 'POST':
        d = request.POST
        total = request.POST['total']
        for k,v in d.items():
            if 'q' in k:
                quantity,pk = k.split('-')
                orders = OrderItems.objects.get(pk = pk)
                orders.quantity = v
                orders.price = int(v) * int(orders.price)
                orders.save()
        basket.bill = total
        basket.save()
        Notification.objects.create(
            customer = cust,
            notification = "Hello"
        )
        messages.success(request, "Order has been sent. Please wait the order to be ready.")
    return redirect(f'/dashboard/{object_id}/menu/')

def orders(request, object_id):
    customer = CustomUser.objects.get(email = request.user)
    orders = Basket.objects.filter(customer_id = CustomUser.objects.get(email = request.user))
    context = {
        'make_orders':orders
        }
    return render(request,'Cust/orders.html',context )

def payment(request, object_id, pk):
    cust = CustomUser.objects.get(email = request.user)
    payment = Basket.objects.get(id = pk)
    if request.method == 'POST':
        scrn = request.FILES['scrn']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(scrn.name, scrn)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        # Read the image using OpenCV
        img = cv2.imread(file_path)
        # img = cv2.imread(scrn.temporary_file_path())
        print(scrn)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 250, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 11)
        text = pytesseract.image_to_string(thresh)
        print(text)
        print(text[(text.index('From')-9):(text.index('From'))])
        journal = int(text[(text.index('From')-9):(text.index('From'))])
        payment.jrnl_no = journal
        payment.screenshot = scrn
        payment.order_date = datetime.now()
        payment.save()
        messages.success(request, "Payment successful.")
        print(journal)

        os.remove(file_path)
    return redirect(f'/dashboard/{object_id}/orders/')

def logout_view(request):
    logout(request)
    return redirect('/')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            current_site = get_current_site(request)
            subject = 'Food ordering system'
            otp = random.randint(100000, 999999)
                    # email_from = settings.EMAIL_HOST_USER

            message2 = f"Your otp for resetting password is {otp}."
                    # First send OTP through email before saving data to Database

            send_mail(
                        subject,
                        message2,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently = True

            )
            request.session['email'] = email
            request.session['otp'] = str(otp)
            return render(request, "reset_okay.html")
        except Exception as e:
            messages.error(request,
                "Failed to send OTP through Email."+str(e))

    return render(request,"reset_password.html")

def enter_otp(request):
    email = request.session['email']
    if request.method == 'POST':
        d = request.POST
        for k,v in d.items():
            if k == 'resend':
                try:
                    current_site = get_current_site(request)
                    subject = 'Food ordering system'
                    otp = random.randint(100000, 999999)
                            # email_from = settings.EMAIL_HOST_USER

                    message2 = f"Your otp is {otp}."
                            # First send OTP through email before saving data to Database

                    send_mail(
                                subject,
                                message2,
                                settings.EMAIL_HOST_USER,
                                [email],
                                fail_silently = True

                    )
                    request.session['otp'] = str(otp)
                except Exception as e:
                            messages.error(request,
                                "Failed to send OTP through Email."+str(e))

            if k == 'submit':
                myotp = request.POST.get('otp')
                otp = request.session['otp']
                if str(myotp) == otp:
                    messages.success(request, "OTP verification successful. You may now reset your password.")
                    return redirect('reset_password')
                else:
                    messages.error(request, 'OTP is incorrect, please try again')
    return render(request, 'enter_otp.html')

def reset_password_confirm(request):
    email = request.session['email']
    if request.method == 'POST':
        password = request.POST['password']
        CustomUser.objects.filter(email = email).update(password = make_password(password))
        messages.success(request, 'Password has been reset.')
        return redirect('signin')
    return render(request, 'reset_password_confirm.html')




