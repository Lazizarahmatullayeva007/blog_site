from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm
from .forms import SearchForm
from django.core.mail import send_mail
from .forms import EmailPostForm
from .forms import RegisterForm
from django.contrib.auth import login
from django.shortcuts import redirect

from django.views.generic import ListView
from taggit.models import Tag


class PostListView(ListView):
    model = Post
    template_name = "blog/post/list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):

        queryset = Post.published.all()

        tag_slug = self.kwargs.get("tag_slug")

        if tag_slug:

            tag = Tag.objects.get(slug=tag_slug)

            queryset = queryset.filter(tags__in=[tag])

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        tag_slug = self.kwargs.get("tag_slug")

        if tag_slug:

            context["tag"] = Tag.objects.get(slug=tag_slug)

        return context


def post_search(request):

    form = SearchForm()

    query = None

    results = []

    if "query" in request.GET:

        form = SearchForm(request.GET)

        if form.is_valid():

            query = form.cleaned_data["query"]

            results = Post.published.filter(
                title__icontains=query
            )

    return render(
        request,
        "blog/post/search.html",
        {
            "form": form,
            "query": query,
            "results": results,
        },
    )


# def post_list(request):
#     posts = Post.published.all()
#     return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()  # ✅ GET requestda bo'sh forma

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,  # ✅ templatega uzatish
        'post_tags': post.tags.all(),
    })

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} sizga tavsiya qiladi: {post.title}"
            message = f"{post.title} ni o'qing: {post_url}\n\n{cd['name']} izohi: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = form.cleaned_data["email"]

            user.save()

            login(request, user)

            return redirect("/")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )