from django.urls import path
from . import views

app_name='lib_books_simple_site'



# Переводим пустой домен в адресе на view 'index'
urlpatterns = [
    path('', views.index, name='index'),
]

