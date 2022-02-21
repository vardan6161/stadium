from django.urls import path

from . import views

urlpatterns =[
    path('signin',views.signin,name='signin'),
    path('verify_user', views.verify_user, name='verify_user'),
    path('records',views.records,name='records'),
    path('info',views.info,name='info'),
    path('update',views.update,name='update'),
    path('update_pwd',views.update_pwd,name='updatepwd'),
    path('update_index',views.update_index,name='update_index'),
    path('update_pwdindex',views.update_pwdindex,name='update_pwdindex'),
    path('signup', views.signup,  name='signup'),
    path('store_user', views.store_user, name='store_user'),
    path('home', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('events',views.events, name='events'),
    path('select_event', views.select_event, name='select_event'),
    path('login_book',views.login_book, name='login_book'),
    path('booked',views.booked, name='booked')



]
