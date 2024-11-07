from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from store.forms import SignUpForm,SignInForm,UserProfileForm,ProjectForm
from django.views.generic import View,FormView,CreateView,TemplateView
from django.contrib.auth import authenticate,login,logout
from store.models import UserProfile,Project,WishListItem,Order
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from store.decorators import signin_required
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail

# Create your views here.
decs=[signin_required,never_cache]
def send_email():
    send_mail(
    "Codehub project download",
    "You have completed purchase of project",
    "shehnashaji1230@gmail.com",
    ["sr4sarath18@gmail.com"],
    fail_silently=False,
)

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

@method_decorator(decs,name='dispatch')
class IndexView(View):
    template_name='index.html'
    def get(self,request,*args,**kwargs):
        qs=Project.objects.all().exclude(developer=request.user)
        return render(request,self.template_name,{'data':qs})

def logout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

@method_decorator(decs,name='dispatch')
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

@method_decorator(decs,name='dispatch')
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

@method_decorator(decs,name='dispatch')
class MyProjectsListView(View):
    template_name='myprojects.html'
    def get(self,request,*args,**kwargs):
        qs=Project.objects.filter(developer=request.user)
        return render(request,self.template_name,{'data':qs})

@method_decorator(decs,name='dispatch')
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
    
@method_decorator(decs,name='dispatch')
class ProjectDetailView(View):
    template_name='project_detail.html'
    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')
        qs=Project.objects.get(id=id)
        return render(request,self.template_name,{'project':qs})

@method_decorator(decs,name='dispatch')
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

@method_decorator(decs,name='dispatch')
class MyWishListItemListView(View):
    template_name='mywishlist.html'
    def get(self,request,*args,**kwargs):
        
        qs=request.user.basket.basket_item.filter(is_order_placed=False)
           
        total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")
        print("total:",total)
           
        return render(request,self.template_name,{'data':qs,"total":total})

@method_decorator(decs,name='dispatch')
class WishListItemDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        WishListItem.objects.get(id=id).delete()
        return redirect('my-wishlist')


import razorpay
@method_decorator(decs,name='dispatch')
class CheckOutView(View):
    templatename='checkout.html'
    def get(self,request,*args,**kwargs):
        KEY_ID="rzp_test_Qeyj3CLL4v0F7y"
        KEY_SECRET="FosHlGlzr3zNzIIG05LNZIGh"
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        amount=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")
        data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        order_id=payment.get("id")
        order_object=Order.objects.create(order_id=order_id,customer=request.user)
        wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)
        for wi in wishlist_items:
            order_object.wishlist_item_objects.add(wi)
            wi.is_order_placed=True
            wi.save()

        # print(payment)
        return render(request,self.templatename,{"key_id":KEY_ID,"amount":amount,"order_id":order_id})

@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):
        
        print(request.POST)
        KEY_ID="rzp_test_Qeyj3CLL4v0F7y"
        KEY_SECRET="FosHlGlzr3zNzIIG05LNZIGh"

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        try:
            client.utility.verify_payment_signature(request.POST)
            order_id=request.POST.get('razorpay_order_id')
            Order.objects.filter(order_id=order_id).update(is_paid=True)
            send_email()
            print('ok')
        except:
            print('failed')


        return redirect('my-orders')

@method_decorator(decs,name='dispatch')
class MyOrdersView(View):
    template_name='myorders.html'
    def get(self,request,*args,**kwargs):
        qs=Order.objects.filter(customer=request.user)
        return render(request,self.template_name,{'data':qs})
