from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post, Category, Tag


# def index(request):
#
#     posts = Post.objects.all().order_by('-pk')
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )
#
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post': post,
#         }
#     )

class PostCreate(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'hook', 'head_image', 'attached_file', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields = ['title', 'content', 'hook', 'head_image', 'attached_file', 'category','tags']

    template_name = "blog/post_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


def show_category_posts(request, slug):
    if slug=="no-category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    context = {
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list' : post_list
    }

    return render(request, 'blog/post_list.html', context)


def show_tag_posts(request, slug):
    tag= Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'tag': tag,
        'post_list': post_list
    }

    return render(request, 'blog/post_list.html', context)
