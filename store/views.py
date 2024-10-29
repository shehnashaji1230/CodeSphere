from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from store.forms import SignUpForm,SignInForm,UserProfileForm,ProjectForm
from django.views.generic import View,FormView,CreateView,TemplateView
from django.contrib.auth import authenticate,login,logout
from store.models import UserProfile,Project
from django.contrib import messages

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

class IndexView(View):
    template_name='index.html'
    def get(self,request,*args,**kwargs):
        qs=Project.objects.all().exclude(developer=request.user)
        return render(request,self.template_name,{'data':qs})

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

class ProjectCreateView(View):
    template_name='projectadd.html'
    form_class=ProjectForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST,files=request.FILES)
        if form_instance.is_valid():
            # add developer to form
            form_instance.instance.developer=request.user
            form_instance.save()
            return redirect('index')
        return render(request,self.template_name,{'form':form_instance})


class MyProjectsListView(View):
    template_name='myprojects.html'
    def get(self,request,*args,**kwargs):
        qs=Project.objects.filter(developer=request.user)
        return render(request,self.template_name,{'data':qs})

class ProjectUpdateView(View):
    template_name='project_update.html'
    form_class=ProjectForm

    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        project_object=Project.objects.get(id=id)
        form_instance=self.form_class(instance=project_object)
        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
         id=kwargs.get('pk')
         project_object=Project.objects.get(id=id)
         form_instance=self.form_class(request.POST,instance=project_object,files=request.FILES)
         if form_instance.is_valid():
             form_instance.save()
             return redirect('my-works')
         return render(request,self.template_name,{'form':form_instance})
    

class ProjectDetailView(View):
    template_name='project_detail.html'
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')
        qs=Project.objects.get(id=id)
        return render(request,self.template_name,{'project':qs})

class AddToWishListView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        project_object=get_object_or_404(Project,id=id)
        try:
            request.user.basket.basket_item.create(project_object=project_object)
            print('item added')
            messages.success(request,'added successfully')
        except Exception as e:
             messages.error(request,'failed to add')
        return redirect('index')

class MyWishListItemListView(View):
    template_name='mywishlist.html'
    def get(self,request,*args,**kwargs):
        
        qs=request.user.basket.basket_item.filter(is_order_placed=False)
           
        
           
        return render(request,self.template_name,{'data':qs})