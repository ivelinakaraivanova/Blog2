from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from articles.forms import LoginForm, UserRegistration, ArticleRegistrationForm, ArticleUpdateForm
from articles.models import Article


def articles_list(request):
    articles = Article.objects.all().order_by('-date_published')

    paginator = Paginator(articles, 3)
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
        'page': page
    }

    return render(request, 'articles_list.html', context)


def article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)

    context = {
        'article': article
    }

    return render(request, 'article_details.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                return HttpResponse('You are logged in')

            else:
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'account/login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()

            return render(request, 'account/register_done.html', {'user_form': user_form})

    else:
        user_form = UserRegistration()

    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def add_article(request):
    if request.method == "POST":
        article_form = ArticleRegistrationForm(request.POST)

        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles_list')

    else:
        article_form = ArticleRegistrationForm()

    context = {
        'article_form': article_form
    }

    return render(request, 'account/add_article.html', context)


def update_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    form = ArticleUpdateForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('articles_list')

    context = {
        'form': form
    }

    return render(request, 'account/update_article.html', context)


def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.delete()
    return redirect('articles_list')

