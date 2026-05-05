from multiprocessing import context

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from client.views import subscription_plans
from .forms import ArticleForm, UpdateUserForm
from .models import Article
from accounts.models import CustomUser


@login_required(login_url='accounts:my-login')
def writer_dashboard(request):
    context = {}
    return render(request, 'writer/writer-dashboard.html', context)


@login_required(login_url='accounts:my-login')
def create_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.article2customuser = request.user
            article.save()
            messages.success(request, "Article created successfully")
            return redirect('writer:my-articles')
    context = {
        'form': form,
    }
    return render(request, 'writer/create-article.html', context)


@login_required(login_url='accounts:my-login')
def my_articles(request):
    current_user = request.user
    articles = Article.objects.filter(article2customuser=current_user)
    context = {
        'articles': articles,
    }
    return render(request, 'writer/my-articles.html', context)


@login_required(login_url='accounts:my-login')
def update_article(request, pk):
    try:
        article = Article.objects.get(pk=pk, article2customuser=request.user)
    except:
        return redirect('writer:my-articles')
    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully")
            return redirect('writer:my-articles')
    context = {
        'form': form,
    }
    return render(request, 'writer/update-article.html', context)


@login_required(login_url='accounts:my-login')
def delete_article(request, pk):
    try:
        post = get_object_or_404(Article, pk=pk, article2customuser=request.user)
    except:
        return redirect('writer:my-articles')
    post.delete()
    messages.success(request, 'Post deleted successfully')
    return redirect('writer:my-articles')


@login_required(login_url='accounts:my-login')
def account_management(request):
    form = UpdateUserForm(instance=request.user)
    user = request.user
    if user.customuser2subscription.subscription_plan:
        subscription_plan = user.customuser2subscription.subscription_plan
        paypal_subscription_id = user.customuser2subscription.paypal_subscription_id
    else:
        subscription_plan = None
        paypal_subscription_id = None
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully")
            return redirect('writer:writer-dashboard')
    context = {
        'form': form,
        'subscription_plan': subscription_plan,
        'paypal_subscription_id': paypal_subscription_id,
    }
    return render(request, 'writer/account-management.html', context)


@login_required(login_url='accounts:my-login')
def delete_account(request):
    deleteUser = CustomUser.objects.get(id=request.user.id)
    deleteUser.delete()
    messages.success(request, "Account deleted successfully")
    return redirect('accounts:my-login')
