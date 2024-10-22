from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from store.forms import SignUpForm,SignInForm,UserProfileForm
from django.views.generic import View,FormView,CreateView,TemplateView
from django.contrib.auth import authenticate,login,logout
from store.models import UserProfile

# Create your views here.

class SignUpView(CreateView):
    template_name='register.html'
    form_class=SignUpForm
    success_url=reverse_lazy("signin")
    # def get(self,request,*args,**kwargs):
    #     form_instance=self.form_class()
    #     return render(request,self.template_name,{'form':form_instance})
    
    # def post(self,request,*args,**kwargs):
    #     form_instance=self.form_class(request.POST)
    #     if form_instance.is_valid():
    #         form_instance.save()
    #         return redirect("signup")
    #     else:
    #         return render(request,self.template_name,{'form':form_instance})

class SignInView(FormView):
    template_name='login.html'
    form_class=SignInForm

    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            uname=form_instance.cleaned_data.get("username")
            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        return render(request,self.template_name,{'form':form_instance})                            

class IndexView(TemplateView):
    template_name='index.html'

def logout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class UserProfileEditView(View):
    template_name='profile_edit.html'
    form_class=UserProfileForm
    def get(self,request,*args,**kwargs):

        user_profile=request.user.profile
        form_instance=UserProfileForm(instance=user_profile)
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        user_profile_instance=request.user.profile
        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():
            form_instance.save()
            return redirect('index')
        else:
            return render(request,self.template_name,{'form':form_instance})