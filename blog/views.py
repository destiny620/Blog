from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import BlogPost, Category, About, Profile, Comment
from django.views.generic import CreateView, UpdateView, DeleteView, ListView #DetailView
from .forms import BlogPostForm, EditForm, ProfileForm #CommentForm

# Create your views here.

# def home(request):
#     posts = BlogPost.objects.all().order_by('-created_at')
#     return render(request, 'home.html', {'posts': posts})

class HomeView(ListView):
     model = BlogPost
     template_name = 'home.html'
     cats = Category.objects.all()
     ordering = ['-created_at']

     def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu

        return context
     
def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})

def CategoryView(request, cats):
    category_posts = BlogPost.objects.filter(category=cats)
    return render(request, 'category.html', {'cats': cats, 'category_posts': category_posts})

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = ['name']



class AddPostView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'add_post.html'
  

class UpdatePostView(UpdateView):
    model = BlogPost
    form_class = EditForm
    template_name = 'update_blog.html'
    

class DeletePostView(DeleteView):
    model = BlogPost
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('home')

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()

    return render(request, "blog.html", {'post':post, 'comments':comments})



# class AddCommentView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'add_comment.html'
#     #fields = '__all__'

#     def form_invalid(self, form):
#         form.instance.posts_id = self.request.kwargs['pk']
#         return super().form_invalid(form)

#     success_url = reverse_lazy('home')

   
    


def about(request):
    posts = About.objects.all()
    return render(request, 'about.html', {'posts':posts})



def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title=searched)
        return render(request, 'search.html', {'searched':searched, 'blogs':blogs})
    else:
        return render(request, 'search.html', {})
    
def profile(request):
    # my_profile = Profile.objects.all()
    return render(request, 'profile.html')

def user_profile(request, pk):
     post = BlogPost.objects.filter(id=pk)
     return render(request, "user_profile.html", {'post':post})

def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'password not the same')
            return redirect('register')
        
    else:
        return render(request, 'register.html')
    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')
   