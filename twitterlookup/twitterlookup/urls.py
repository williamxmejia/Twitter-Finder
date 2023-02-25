from django.contrib import admin
from django.urls import path
from tweet import views

urlpatterns = [
    path('', views.index),
    path('activity/', views.get_name),
    path('admin/', admin.site.urls),

]
