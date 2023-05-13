from django.urls import path
from .views import (HomeView, PostDetailView, PostCreateView,
                    PostUpdateView, PostDeleteView, CommentUpdateView, CommentDeleteView,
                    register, user_logout, user_login,
                    author_posts, about, contact, search_results, post_comment,)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comment/', post_comment, name='post_comment'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('comment/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('comment/<int:post_pk>/<int:pk>/comment_update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(template_name='delete_post'), name='post_delete'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('profile/<int:user_id>/', author_posts, name='author_posts'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', search_results, name='search_results'),
]

