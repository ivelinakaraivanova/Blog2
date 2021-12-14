from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login

from articles.forms import LoginForm, UserRegistration
from articles.models import Article


def articles_list(request):
    articles = Article.objects.all().order_by('-date_published')

    context = {
        'articles': articles
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
        user_form = UserRegistration(request.POST)

    return render(request, 'account/register.html', {'user_form': user_form})
