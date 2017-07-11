from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/' , views.LoginView.as_view() , name='login'),
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^login_success/' , views.LoginSuccessView.as_view() , name='login_success'),
    url(r'^signup_success/' , views.SignupSuccessView.as_view() , name='signup_success'),
]
