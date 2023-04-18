from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('otp/', views.verifyotp, name='otp'),
    path('logout/', views.logout_view, name='logout')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)