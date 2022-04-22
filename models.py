from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Traveller(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE,null = True)
    User._meta.get_field('email')._unique = True
    phone_number = models.CharField(max_length=11,unique=True)
    user_type = models.CharField(max_length=10,default='Traveller')
    profile_pic = models.ImageField(upload_to  ='profile picture',blank = True)

    # def save(self,*args,**kwargs):
    #     self.user_type = 'Traveller'
    #     super.save(*args,**kwargs)
    # def __str__(self):
    #     return super.first_name

    def __str__(self):
        return self.user.username
class Agency(models.Model):
    company_name = models.CharField(max_length=30,unique=True)
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    company_logo = models.ImageField(upload_to  ='company logo',blank = True)

    def __str__(self):
        return self.company_name

class Contact_info(models.Model):
    phone_number = models.CharField(max_length=11,unique=True)
    email = models.EmailField(max_length=50,unique=True)
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE)

class Location(models.Model): 
    town = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    house_no = models.SmallIntegerField()
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE)

class AgencyMember(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE,null = True)
    User._meta.get_field('email')._unique = True
    phone_number = models.CharField(max_length=11,unique=True)
    user_type = models.CharField(max_length=30,default='agency_member')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE )
    profile_pic = models.ImageField(upload_to ='profile picture',blank = True)

    def __str__(self):
        return self.user.username

    # def save(self,*args,**kwargs):
    #     self.user_type = 'agency_member'
    #     super.save(*args,**kwargs)

class Blog(models.Model):
    place = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    blogger = models.ForeignKey(Traveller,on_delete=models.SET_NULL,null=True)

   

    def __str__(self):
        return self.place+'\n'+self.description[:20]

class BlogImages(models.Model):
    image = models.ImageField(upload_to ='blog picture' )
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='image')


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    traveller = models.ForeignKey(Traveller,on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.comment

class Package(models.Model):
   place = models.CharField(max_length=20)
   duration = models.SmallIntegerField()
   per_person_cost = models.DecimalField(max_digits=8,decimal_places=2)
   hotel_name = models.CharField(max_length=45)
   bus_name = models.CharField(max_length=45)
   agency = models.ForeignKey(Agency,on_delete=models.CASCADE)
   def __str__(self):
      return self.place+' package'

class Books(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.SmallIntegerField()
    traveller = models.ForeignKey(Traveller,on_delete=models.SET_NULL,null=True)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)

class Review(models.Model):
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    reviewer = models.ForeignKey(Traveller,on_delete=models.SET_NULL,null=True)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)

    def __str__(self):
        return 'rating: '+self.rating+'\n'+self.description[:10]






