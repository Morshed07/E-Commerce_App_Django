"""djangoEcommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from Ecommerceapp import views
from Ecommerceapp import AdminViews
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', views.AdminLogin,name='admin_login'),
    path('', include('Ecommerceapp.urls')),
    #admin_part
    path("admin_home", AdminViews.Admin_home, name="admin_home"),
    path("admin_login_process",views.AdminloginProcess,name="admin_login_process"),
    path("admin_logout_process",views.AdminlogoutProcess,name="admin_logout_process"),

    #category_part
    path("category_list",AdminViews.CategoriesListView.as_view(),name="category_list"),
    path("category_create",AdminViews.CategoriesCreate.as_view(),name="category_create"),
    path("category_update/<slug:pk>",AdminViews.CategoriesUpdate.as_view(),name="category_update"),

    #subcategory_part
    path("sub_category_list",AdminViews.SubCategoriesListView.as_view(),name="sub_category_list"),
    path("sub_category_create",AdminViews.SubCategoriesCreate.as_view(),name="sub_category_create"),
    path("sub_category_update/<slug:pk>",AdminViews.SubCategoriesUpdate.as_view(),name="sub_category_update"),
   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
