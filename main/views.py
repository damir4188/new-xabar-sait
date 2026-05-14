from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Article, Category, Like, Comment
from .forms import RegisterForm, CommentForm


def home(request):
    articles = Article.objects.select_related('author', 'category').all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        articles = articles.filter(category__slug=selected_category)
    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'home.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.views += 1
    article.save()
    comments = article.comments.select_related('user').all()
    comment_form = CommentForm()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(article=article, user=request.user).exists()
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'likes_count': article.likes.count(),
    }
    return render(request, 'article_detail.html', context)


@login_required
@require_POST
def toggle_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    like, created = Like.objects.get_or_create(article=article, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': article.likes.count()})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')