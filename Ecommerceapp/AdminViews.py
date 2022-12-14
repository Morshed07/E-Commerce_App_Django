from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,DetailView,UpdateView,View
from .models import Categories,SubCategories,CustomUser,MerchantUser
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q


@login_required(login_url="/admin/")

def Admin_home(request):
    return render(request, 'admin_templates/home.html')


class CategoriesListView(ListView):
    model= Categories
    template_name="admin_templates/category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val= self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter !="":
            cat=Categories.objects.filter(Q(title__contains=filter_val)| Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Categories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self, **kwargs):
        context=super(CategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Categories._meta.get_fields()
        return context



class CategoriesCreate(SuccessMessageMixin,CreateView):
    model=Categories
    success_message="Category Added!"
    fields="__all__"
    template_name="admin_templates/category_create.html"


class CategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=Categories
    success_message="Category Updated!"
    fields="__all__"
    template_name="admin_templates/category_update.html"


class SubCategoriesListView(ListView):
    model= SubCategories
    template_name="admin_templates/sub_category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val= self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter !="":
            cat=SubCategories.objects.filter(Q(title__contains=filter_val)| Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self, **kwargs):
        context=super(SubCategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

class SubCategoriesCreate(SuccessMessageMixin,CreateView):
    model=SubCategories
    success_message=" Sub Category Added!"
    fields="__all__"
    template_name="admin_templates/sub_category_create.html"


class SubCategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategories
    success_message="Sub Category Updated!"
    fields="__all__"
    template_name="admin_templates/sub_category_update.html"


class MerchantUserListView(ListView):
    model= MerchantUser
    template_name="admin_templates/merchant_list.html"

class MerchantUserCreateView(SuccessMessageMixin, CreateView):
    template_name = "admin_templates/merchant_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]
        
        #saving custom user object for merchant user
    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        #saving merchant user field,added manually

        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.merchantuser.profile_pic=profile_pic_url
        user.merchantuser.company_name=self.request.POST.get("company_name")
        user.merchantuser.nid_details=self.request.POST.get("nid_details")
        user.merchantuser.address=self.request.POST.get("address") 
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        user.merchantuser.is_added_by_admin=is_added_by_admin
        user.save()
        messages.success(self.request, "Merchant User Created")
        return HttpResponseRedirect(reverse("merchant_list"))

class MerchantUserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = "admin_templates/merchant_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]
        

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        merchantuser=MerchantUser.objects.get(auth_user_id=self.object.pk)
        context["merchantuser"]=merchantuser
        return context

        #saving custom user object for merchant user
    def form_valid(self,form):
        user=form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        #saving merchant user field,added manually
        merchantuser = MerchantUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            merchantuser.profile_pic=profile_pic_url
        merchantuser.company_name=self.request.POST.get("company_name")
        merchantuser.nid_details=self.request.POST.get("nid_details")
        merchantuser.address=self.request.POST.get("address") 
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        merchantuser.is_added_by_admin=is_added_by_admin
        user.save()
        messages.success(self.request, "Merchant User Updated")
        return HttpResponseRedirect(reverse("merchant_list"))


class ProductView(View):
    def get(self, request, *args, **kwargs):
        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category": sub_category})
        return render(request,"admin_templates/product_create.html",{"categories":categories_list})