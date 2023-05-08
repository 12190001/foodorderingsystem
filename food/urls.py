from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('otp/', views.verifyotp, name='otp'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/<str:object_id>/', views.dashboard, name='dashboard'),
    path('dashboard/<str:object_id>/menu/', views.menu, name='menu'),
    path('dashboard/<str:object_id>/menu/create_menu', views.create_menu, name='create_menu'),
    path('dashboard/<str:object_id>/menu/update/<pk>', views.update_menu, name='update'),
    path('dashboard/<str:object_id>/menu/delete', views.delete_menu, name='delete'),
    path('owner_dashboard/', views.owner_dashboard, name='owner'),
    path('owner_dashboard/infomanager', views.owner_add_manager, name='addmanager'),
    path('owner_dashboard/infomanager/delete', views.delete_manager, name='deletemanager'),
    path('dashboard/<str:object_id>/menu/<pk>/added', views.add_order, name='order'),
    path('dashboard/<str:object_id>/menu/confirm', views.confirm_order, name='confirm'),
    path('dashboard/<str:object_id>/orders/', views.orders, name='orders'),
    path('dashboard/<str:object_id>/orders/<pk>/payment', views.payment, name='payment'),
    path('reset/', views.reset_password, name='reset'),
    path('reset/otp/', views.enter_otp, name='enter_otp'),
    path('reset/otp/password_reset', views.reset_password_confirm, name='reset_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)