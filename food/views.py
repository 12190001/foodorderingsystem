from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from food.models import CustomUser, Manager, Owner
from food.forms import CustomerForm
from django.conf import settings
import random
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    return render(request, 'index.html')

def sign_up(request):
    try:
        if request.method == "POST":
            form = CustomerForm(request.POST)
            first_name = request.POST['Firstname']
            last_name = request.POST['Lastname']
            email = request.POST['email']
            contact_number = request.POST['contact']
            password = request.POST['password']
            confirm = request.POST['confirmPassword']

            if form.is_valid():
                if CustomUser.objects.filter(email=email).exists():
                    print("Email already exists. Enter another email.")
                ### OTP verification ###
            else:
                try:
                    current_site = get_current_site(request)
                    subject = 'Food ordering system'
                    otp = random.randint(100000, 999999)
                            # email_from = settings.EMAIL_HOST_USER

                    message2 = f"Your otp is {otp}. Use it for verification in {current_site.domain}/otp"
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
                    print('success')
                    return redirect('otp')

                except Exception as e:
                            print(
                                "Failed to send OTP through Email."+str(e))


        else:
            form = CustomerForm()
    except Exception as e:
        messages.error(request,str(e))
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
                            print(
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
        print('here')
        print(CustomUser.objects.filter(email=email))
        print(myuser)
        if myuser is not None:
            login(request, myuser)
            print('okay')

                # if Manager.objects.mongo_find_one({'email':email}):
                # # Authenticate and login the manager
                #     print('manager')
                # elif Owner.objects.mongo_find_one({'email':email}):
                #     print('owner')
                # if User.objects.mongo_find_one({'email':email}):
                #     print('Customer')
            if CustomUser.objects.filter(email = myuser.email).first():
                return redirect('home')
            elif Manager.objects.filter(email = myuser.email).first():
                print('manager')
            elif Owner.objects.filter(email = myuser.email).first():
                print('owner')
            else:
                print('Email not available')


        else:
            print("Incorrect Email or Password")
            return redirect('signin')
    else:
         print('No')

    return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    return redirect('/')




