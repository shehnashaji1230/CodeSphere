from django.db import models

from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

# request.user
class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

# UserProfile.objects.filter(owner=request.user)
# request.user.profile.profile_picture
class UserProfile(BaseModel):

    bio=models.CharField(max_length=200)

    profile_picture=models.ImageField(upload_to="profilepictures",null=True,blank=True)

    phone=models.CharField(max_length=200)

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    def __str__(self) -> str:
        return self.owner.username


class Tag(BaseModel):

    title=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title
    
class Project(BaseModel):

    title=models.CharField(max_length=200)

    description=models.TextField()

    preview_image=models.ImageField(upload_to="previewimages",null=True,blank=True)

    price=models.PositiveIntegerField()

    developer=models.ForeignKey(User,on_delete=models.CASCADE)

    files=models.FileField(upload_to="projects",null=True,blank=True)

    tag_objects=models.ManyToManyField(Tag,null=True)

    thumbnail=EmbedVideoField()

# WishList.objects.filter(owner=request.user)
# request.user.basket
class WishList(BaseModel):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")


class WishListItem(BaseModel):

    wishlist_object=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="basket_item")

    project_object=models.ForeignKey(Project,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)
# WishListItems.objects.filter(wishlist_object__owner=request.user,is_order_placed=False)
class Order(BaseModel):

    wishlist_item_objects=models.ManyToManyField(WishListItem)

    is_paid=models.BooleanField(default=False)

    order_id=models.CharField(max_length=200,null=True)

    




    









