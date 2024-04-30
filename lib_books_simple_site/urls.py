from django.urls import path
from . import views

app_name='lib_books_simple_site'



# Переводим пустой домен в адресе на view 'index'
urlpatterns = [
    path('', views.index, name='index'),
]





urlpatterns += [
    path('api_update_bss_options_table', views.api_update_bss_options_table, name='api_update_bss_options_table'),
]






urlpatterns += [
    path('debug_results', views.debug_results, name='debug_results'),
]







