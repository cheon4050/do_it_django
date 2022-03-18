from django.views.generic import ListView, DetailView
# Create your views here.
from blog.models import Post


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

class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post