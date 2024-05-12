"""
URL configuration for gestion_de_projet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from back.views import ModelListView, ModelDeleteView, ModelUpdateView, generate_pdf, Login, UserIndexView, Logout, \
    ImportCSVView, AdminIndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', AdminIndexView.as_view(), name='admin'),
    path('dashboard/<str:model_name>', ModelListView.as_view(), name='index'),
    path('dashboard/<str:model_name>/<int:pk>/delete/', ModelDeleteView.as_view(), name='model-delete'),
    path('dashboard/<str:model_name>/<int:pk>/update/', ModelUpdateView.as_view(), name='model-update'),
    path('dashboard/<str:model_name>/import/', ImportCSVView.as_view(), name='import-csv'),

    path('welcome/', UserIndexView.as_view(), name='welcome'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
