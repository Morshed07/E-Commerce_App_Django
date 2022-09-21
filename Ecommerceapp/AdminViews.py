from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from .models import Categories
from django.contrib.messages.views import SuccessMessageMixin



@login_required(login_url="/admin/")

def Admin_home(request):
    return render(request, 'admin_templates/home.html')


class CategoriesListView(ListView):
    model= Categories
    template_name="admin_templates/category_list.html"

class CategoriesCreate(SuccessMessageMixin,CreateView):
    model=Categories
    success_message="Category Added!"
    fields="__all__"
    template_name="admin_templates/category_create.html"


class CategoriesCreate(SuccessMessageMixin,UpdateView):
    model=Categories
    success_message="Category Updated!"
    fields="__all__"
    template_name="admin_templates/category_create.html"