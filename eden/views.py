from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, DetailView,
                                CreateView, UpdateView, DeleteView)
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import UserRegistrationForm
from .models import Post, Comment, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q


################# POST VIEWS #################
# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = "index.html"
    paginate_by = 5
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by("date_posted")
        paginator = Paginator(post_list, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_pk'] = self.object.pk
        return context



class PostCreateView(CreateView):
    model = Post
    fields = ["title", "body", "title_tag"]
    template_name = "create_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "body", "title_tag"]
    template_name = "update_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse("comment_update", kwargs={"post_pk": post_pk, "pk": self.object.pk})

    
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ["body"]
    template_name = "update_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_pk'] = self.object.post.pk
        return context


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse("post_detail", kwargs={"pk": post_pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return user == post.author or user.is_superuser

    def handle_no_permission(self):
        post = self.get_object()
        messages.error(self.request, "You are not authorized to delete this post.")
        return HttpResponseRedirect(reverse("post_detail", args=[str(post.pk)]))


def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "delete_comment.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        comment = self.get_object()
        return reverse("post_detail", kwargs={"pk": comment.post.pk})

    def handle_no_permission(self):
        comment = self.get_object()
        messages.error(self.request, "You are not authorized to delete this comment.")
        return redirect("post_detail", pk=comment.post.pk)



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by("-date_posted")
    if request.method == "POST":
        comment_form = post_comment(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = post_comment()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})



class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"




def search_results(request):
    query = request.GET.get('q')
    results = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(body__icontains=query) |
        Q(title_tag__icontains=query) |
        Q(author__username__icontains=query)
    )
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'search_results.html', context)



################# USER VIEWS #################
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully registered and logged in!")
            return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


def author_posts(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(author=user)
    context = {"user": user, "posts": posts}
    return render(request, "profile.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")
