from django.urls import path
from .import views
from .views import register, activate, my_animals, add_weighting
from django.contrib.auth import views as auth_views



app_name = 'main'

urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('animal_list/', views.animal_list, name='animal_list'),
    path('my_animals/', my_animals, name='my_animals'),
    path('add_weighting/', add_weighting, name='add_weighting'),
    path('register/', register, name='register'), # Регистрация 
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Вход в систему
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Выход из системы
    path('<slug:slug>/', views.product_detail, name='product_detail'),

]