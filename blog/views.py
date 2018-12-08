from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


# Create your views here.

def post_list(request):
    # reverse order: adding a
    #  - before published_date will show latest to first entry
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    # default order: show first entry to latest entry
    # posts = Post.objects.filter(
    # published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_new(request):
    # handle situation: go back to the view with
    # all form data we just typed
    # you need to be logged in to post (admin) else submit gives error
    if request.method == "POST":
        # connect form to model Post
        form = PostForm(request.POST)
        if form.is_valid():
            # don't save yet, commit=False
            # because required user has to be added
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            # preserve added user (and date), with post.save
            # go back to form save to save to db
            post.save()
            return redirect('post_detail', pk=post.pk)
    # handle situation: access the page for the first time
    # with blank form
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # fill form with instance
        # instance =  post record (Post object)  with pk (primary key)
        # pk was added in url
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('created_date')
    return render(request,
                  'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # saved by publish method in Post model
    post.publish()
    # could also be saved like this, in this view
    # post.published_date = timezone.now()
    # post.save()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
