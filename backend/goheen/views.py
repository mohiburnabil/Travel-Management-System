
from struct import pack
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import re_path
from .models import Blog, BlogImages,Package,Traveller,Comment
from .forms import BlogForm,RegistrationForm,UserForm,ImageForm,CreatePackages
from django.forms import modelformset_factory

# Create your views here.


def homePage(request):
     blogs = Blog.objects.all()
    
     return render(request,"index.html",{'blogs':blogs})


def blog_details(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    photos = BlogImages.objects.filter(blog= blog)
    if request.method == 'POST':
         comment = Comment.objects.create(
             traveller = request.user.traveller,
             blog = blog,
             comment = request.POST.get('comment')
            
         )
         return redirect('blog_details',pk = blog.id)
    

    
    comments = blog.comment_set.all()
    print(comments)
    return render(request, 'blog_details.html', {
        'blog':blog,
        'photos':photos,
        'comments':comments
    })


def loginview(request):
    
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist.')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('homepage')
        
        else:
            messages.error(request,'username or password does not exist')


    return render(request,"Login.html")

def singupview(request):
       
     if request.method == 'POST':
         print('worked')
         userform = UserForm(request.POST)
         travellerform = RegistrationForm(request.POST, request.FILES)
         print( travellerform.is_valid())
         print(userform.errors)
         if userform.is_valid() and travellerform.is_valid():
             print('.......worked.........')
             user = userform.save()
             traveller = travellerform.save(commit=False)
             traveller.user = user

             traveller.save()
             return redirect('login')



     form = UserForm()
     traveller = RegistrationForm()
     context = {'userform':form,'travellerform':traveller}

     return render(request,"SignUp.html",context)

def profile(request,pk):
    user = Traveller.objects.get(id = pk)
    context={'user':user}
    return render(request,"Tourist-profile.html",context)

def logoutview(request):

    logout(request)
    return redirect('homepage')
@login_required(login_url = 'login')
def packageList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print(q)
    packages = Package.objects.filter(
        
    Q(place__icontains = q) | Q(agency__company_name = q)
    );

    total_packages = packages.count()
    return render(request,"Packages-List.html",{"packages":packages,"total_packages":total_packages})

def packageDetails(request,pk):
    package = Package.objects.get(id = pk)

    return render(request,"PackageDetails.html",{'package':package})



@login_required(login_url = 'login')
def createBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        post_form = BlogForm(request.POST)
        images = request.FILES.getlist('images')
        print(images)
        print( post_form.is_valid())
        if post_form.is_valid() :
            blog = post_form.save(commit=False)
            blog.blogger = request.user.traveller
            blog.save()
            for image in images:
                BlogImages.objects.create(
                    image = image,
                    blog = blog
                )
            

            return redirect('homepage')


    
    context = {'form':form}
    return render(request,"blogcreate.html",context)


@login_required(login_url = 'login')
def updateBlog(request,pk):
    blog = Blog.objects.get(id = pk)
    form = BlogForm(instance=blog)
     
    if request.user != blog.blogger:
        redirect('login')



    if request.method == 'POST':
        form = BlogForm(request.POST,instance = blog)
        if form.is_valid():
            form.save()
            return redirect('homepage')


    context = {'form':form}
    return render(request,'blogcreate.html',context)

@login_required(login_url = 'login')
def delete(request,pk):
    blog = Blog.objects.get(id = pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('homepage')
    return render(request,'delete.html',{"obj":blog})

def createpackage(request):
    if request.method == 'POST':
        packageform = CreatePackages(request.POST)
        if packageform.is_valid():
            package = packageform.save(commit=False)
            package.agency = request.user.agencymember.agency
            package.save()
            return redirect('packages')




    packageform = CreatePackages()
    return render(request,'createpackage.html',{"packageform":packageform})


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'About.html')
