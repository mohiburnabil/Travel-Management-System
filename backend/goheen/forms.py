
from pyexpat import model
from attr import fields
from django.forms import ModelForm
from matplotlib import widgets
from matplotlib.pyplot import cla
from .models import Blog,Traveller,BlogImages,Package
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
class BlogForm(ModelForm):
   
    class Meta:
        model = Blog
        fields = '__all__' 
        exclude = ['blogger']
        widgets={
            'place':forms.TextInput(attrs={"class":"form-control"}),
              'description':forms.Textarea(attrs={"class":"form-control"}),
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = BlogImages
        fields = ('image', )

class UserForm(UserCreationForm):
     first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class":"form-control"}))
     last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class":"form-control"}))
     email = forms.EmailField(max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
     class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        help_texts = {
            'password ': None,
            'username': None,
            'email': None,
           
        }
     def __init__(self,*args,**kwargs):
         super(UserForm, self).__init__( *args,**kwargs)

         self.fields['username'].widget.attrs['class'] = 'form-control'
         self.fields['password1'].widget.attrs['class'] = 'form-control'
         self.fields['password2'].widget.attrs['class'] = 'form-control'


     def save(self,commit = True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name  = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


        if commit:
            user.save()
        return user


class RegistrationForm(ModelForm):
    class Meta:
        model =  Traveller
        fields = ['phone_number','profile_pic']
        widgets={
            'phone_number':forms.TextInput(attrs={"class":"form-control"}),
            'profile_pic':forms.FileInput(attrs={"class":"form-control"})
        }

class CreatePackages(ModelForm):
    class Meta:
        model = Package
        fields = ['place','duration','per_person_cost','hotel_name','bus_name']
        widgets={
            'place':forms.TextInput(attrs={"class":"form-control"}),
            'duration':forms.TextInput(attrs={"class":"form-control"}),
            'per_person_cost':forms.TextInput(attrs={"class":"form-control"}),
            'hotel_name':forms.TextInput(attrs={"class":"form-control"}),
            'bus_name':forms.TextInput(attrs={"class":"form-control"}),
        }
        