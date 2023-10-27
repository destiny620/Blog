from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AddPostView, UpdatePostView, DeletePostView, HomeView, AddCategoryView #AddCommentView #BlogDetailView

urlpatterns = [
    # path("", views.home, name="home"),
    # path("posts/<str:pk>/", views.blog, name="posts"),
    path('', HomeView.as_view(), name='home'),
    # path('posts/<str:pk>/', BlogDetailView.as_view(), name='posts'),
    path("about/", views.about, name="about"),
    path("add_post/", AddPostView.as_view(), name="add_post"),
    path('posts/edit/<str:pk>', UpdatePostView.as_view(), name='update_blog'),
    path('posts/<str:pk>/delete', DeletePostView.as_view(), name='delete_blog'),
    path('search/', views.search, name='search'),
    path("category/<str:cats>/", views.CategoryView, name="category"),
    path("category-list/", views.CategoryListView, name="category-list"),
    path("add_category/", AddCategoryView.as_view(), name="add_category"),
    # path("posts/<str:pk>/comment/", AddCommentView.as_view(), name="add_comment"),
    path("posts/<str:slug>/", views.blogs_comments, name="posts"),
    
    #profile
    path('profile/', views.profile, name='profile'),
    path('user_profile/<str:pk>', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    #authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)