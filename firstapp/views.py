from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from .models import Blogger, Blog
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import BlogSerializer
from .permissions import IsSiteAdmin


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')  # replace 'home' with your desired URL after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')  # create a login.html template in your app's templates folder



def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # assuming you have a login URL named 'login'
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    #requests.urllib3.disable_warnings()
    
    api_key = 'fcab833e9d1d4812a379ad9a32294015'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url, verify=False, timeout=30)
    # response = requests.get(url)
    news_data = response.json()['articles']
    return render(request, 'home.html', {'news_data': news_data})





def blogList(request):
    blogs = Blogger.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def delete_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)

    # Check if the current user is the owner of the blog
    if request.user == blog.user:
        blog.delete()
        return redirect('blog_list')  # Redirect to wherever you want after deletion
    else:
        # Return some error or permission denied page
        return render(request, 'error.html', {'message': 'You are not authorized to delete this blog.'})
    



from .forms import BlogForm
from .models import Blog

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = request.user  # Assuming the user is logged in
            blog = Blog.objects.create(title=title, content=content, author=author)
            return redirect('blog_details')  # Redirect to blog detail page
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})


def blog_details(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_details.html', {'blogs': blogs})


@api_view(['GET'])
@permission_classes([IsSiteAdmin])
def blog_list(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)



def index(request):
    return render(request, 'index.html', {})