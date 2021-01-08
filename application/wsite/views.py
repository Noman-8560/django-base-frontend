from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .models import *
from application.models import Article


def home(request):

    context = {
        'site': Website.objects.filter().first(),
        'team_members': WebsiteTeam.objects.all(),
        'events': WebsiteEvents.objects.all().order_by('sequence'),
        'blog': Article.objects.all().order_by('-created_at')[0:3]
    }
    return render(request=request, template_name='wsite/home.html', context=context)


def event(request, slug):
    context = {
        'site': Website.objects.filter().first(),
        'event': WebsiteEvents.objects.get(slug=slug),
    }
    return render(request=request, template_name='wsite/event.html', context=context)


def article(request, slug):

    article = None
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        redirect('wsite:articles', permanent=True)

    if article is None:
        redirect('wsite:articles', permanent=True)

    context = {
        'site': Website.objects.filter().first(),
        'article': article,
    }
    return render(request=request, template_name='wsite/article.html', context=context)


def articles(request):
    articles = Article.objects.all()

    articles = articles.order_by('-created_at')
    articles_list = Article.objects.all().order_by('-created_at').values('pk', 'topic', 'slug')

    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 1)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'site': Website.objects.filter().first(),
        'articles': articles,
        'articles_list': articles_list
    }
    return render(request=request, template_name='wsite/articles.html', context=context)