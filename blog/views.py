from pdb import post_mortem
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView,DeleteView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import *
from .forms import *
from .tasks import send_mail_task
# Create your views here.

# create blog
def blogs(request):
    try:
        posts = BlogPost.objects.all()
        posts = BlogPost.objects.filter().order_by('-dateTime')
        return render(request, "blog.html", {'posts':posts})
    except:
        return render(request,"blog.html",{'posts':'try again'})  
# Add Blog post   
class AddPostView(CreateView):
    try:
        model = BlogPost
        #form_class = BlogPostForm
        template_name = 'add_blogs.html'
        fields = '__all__'
    except Exception as e:
        JsonResponse({'msg':'something missing'})
# Update blog post
class UpdatePostView(UpdateView):
    try:
        model = BlogPost
        template_name = 'edit_blog.html'
        fields = ['title','slug','content']
    except Exception as e:
        JsonResponse({'msg':'something missing'})
#class DeletePostView(DeleteView):
    #model = BlogPost
    #template_name = 'edit_blog.html'
# Subscribe blogs app
def subscribe(request):
    try:
        if request.method == "POST":
            post_data = request.POST.copy()
            email = post_data.get("email", None)
            name = post_data.get("name", None)
            subscribedUsers = SubscribedUsers(email=email,name=name)
            
            subscribedUsers.save()
            if email is None:
                return render(request,"subscribe.html",{'message':'Email is required'}) 
            elif SubscribedUsers.objects.get(email = email):
                return render(request,"subscribe.html",{'msg':'Email address alreaady exists'})
            else:
                
                #send a confirmation mail 
                subject = 'Heptagon technologies subscription'
                message = 'Hello ' + name +', Thanks for subscribing'
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [email,]
                send_mail(subject,message,email_from,recipient_list)
                return render(request,"subscribe.html",{'msg':'Thanks.subscribed success'}) 
                
        return render(request, "subscribe.html")
    except Exception as e:
        return render(request,"subscribe.html",{'msg':'something wrong'})

# Blogs comments
def blogs_comments(request, slug):
    try:
        post = BlogPost.objects.filter(slug=slug).first()
        comments = Comment.objects.filter(blog=post)
        if request.method=="POST":
            user = request.user
            content = request.POST.get('content','')
            blog_id = request.POST.get('blog_id','')
            comment = Comment(user = user, content = content, blog_id = blog_id)
            comment.save()
        return render(request, "blog_comments.html", {'post':post, 'comments':comments})
    except Exception as e:
        return render(request,'blog_comments', {'post':'something missing','comments':'something missing'})
# Delete blog post
def Delete_Blog_Post(request,slug, pk):
    try:
        posts = BlogPost.objects.get(slug=slug , pk=pk)
        if request.method == "POST":
            posts.delete()
            return redirect('/')
        return render(request, 'delete_blog_post.html', {'posts':posts})
    except Exception as e:
        return render(request, 'delete_blog_post.html', {'posts':'something went wrong'})

#search post
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})    

# Register post
def register(request):
    try:
        if request.method =="POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['possword2']

            if password1 != password2:
                messages.error(request, "passwords do not match.")
                return redirect('/register')
            user = User.objects.create_user(username,email,password1)
            user.first_name = first_name
            user.last_name = last_name 
            user.save()
            return render(request, 'login.html')
        return render(request,"register.html")
    except Exception as e:
        return render(request,"register.html",{'something missing'})
        
# Login into blog
def Login(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect("/")
            else:
                messages.error(request, "Invalid credentials.")
            return render(request,'blog.html')
        return render(request,"login.html")
    except Exception as e:
        return render(request,"login.html",{"something went wrong"})
 # logout blog       
def Logout(request):
    try:
        logout(request)
        messages.success(request,"succefully logged out")
        return redirect('/login')
    except Exception as e:
        return render(request,'blog.html',{"something missing"})

def sendmail(request):
    if request.method == "POST":
       
        form = SendEmailForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data['email']
            send_mail_task.delay()
            return render(request, 'mail.html', {'form': form})
            

    form = SendEmailForm()
    return render(request, 'mail.html', {'form': form})
        