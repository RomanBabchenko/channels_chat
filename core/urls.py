from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'reg/', views.RegisterView.as_view()),
    url(r'login/', views.LoginView.as_view()),
    url(r'logout/', views.LogoutView.as_view()),
]