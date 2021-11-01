from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from uploadcare.forms import PostForm
from uploadcare.models import Post


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("post_list")


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("post_list")


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")
