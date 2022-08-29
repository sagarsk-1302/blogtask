from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from .models import Post,Comments
from django.urls import reverse
from django.views.generic import ListView
# Create your views here.

def user_login(request):
    credentials_failed = False
    if(request.method=="POST"):
        email = request.POST['email']
        password = request.POST['password']
        user = None
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
        else:
            credentials_failed=True
    return render(request,"login.html",{'credentials_failed':credentials_failed})

def user_registration(request):
    registered = False
    username_exists = False
    email_exists = False
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email = email)
            email_exists = True
        except User.DoesNotExist:
            try:
                User.objects.get(username = username)
                username_exists = True
            except User.DoesNotExist:
                user = User.objects.create_user(username= username,email=email,password=password)
                user.save()
                registered = True
                print('user created')
            finally:
                return render(request,'registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})
        finally:
            return render(request,'registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})
    else:
        return render(request,'registration.html',{'registered':registered,"username_exists":username_exists,
                                                                        "email_exists":email_exists})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home')) #redirects to index after logging out


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.all().order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5

def PostDetail(request,id):
    post = Post.objects.get(id=id)
    if(request.method=="POST"):
        body = request.POST["body"]
        user = request.user
        newComment = Comments.objects.create(user=user,post=post,body=body)
        newComment.save()
    comments = Comments.objects.filter(post=post)
    count = comments.count()
    return render(request,"post_detail.html",{"comments":comments,"post":post,"count":count,"id":id})

def Share(request):
    if(request.method=="POST"):
        id = request.POST["id"]
        post = Post.objects.get(id=id)
        return render(request,"share.html",{"post":post})
    return HttpResponseRedirect(reverse('home'))


def userDetails(request):
    user = request.user
    return render(request,"profile.html",{"user":user})
