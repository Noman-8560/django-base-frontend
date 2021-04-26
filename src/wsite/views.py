from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .models import *
from src.application.models import Article
from .forms import WebsiteForm


def home(request):

    context = {
        'site': Website.objects.filter().first(),
        'team_members': WebsiteTeam.objects.filter(is_active=True),
        'events': WebsiteEvents.objects.filter(is_active=True).order_by('sequence'),
        'blog': Article.objects.filter(active=True).order_by('-created_at')[0:3]
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


@user_passes_test(lambda u: u.is_superuser)
def site_builder(request):

    form = None
    message = None
    website = Website.objects.filter().first()

    if request.method == 'POST':
        if website:
            form = WebsiteForm(request.POST or None, request.FILES, instance=website)
            if form.is_valid():
                form.save(commit=True)
        else:
            form = WebsiteForm(request.POST or None, request.FILES)
            if form.is_valid():
                form.save(commit=True)
    else:
        if website:
            form = WebsiteForm(instance=website)
        else:
            form = WebsiteForm()

    return render(request=request, template_name='application/site_builder.html', context={'form': form})
