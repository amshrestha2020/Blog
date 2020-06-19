from django.shortcuts import render
from operator import attrgetter
from blog.models import BlogPost
from blog.views import get_blog_queryset
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

BLOG_POSTS_PER_PAGE = 10

# Create your views here.
def home_screen_view(request):
    context = {}
    #print(request.headers)
    #context = {
    #    'some_string' = "This is some string that i'm passing to the view",
    #    'some_number' = 123456,
    #}
    
    #list_of_values = []
    #list_of_values.append("first entry")
    #list_of_values.append("second entry")
    #list_of_values.append("third entry")
    #list_of_values.append("fourth entry")
    #context['list_of_values'] = list_of_values

    # accounts = Account.objects.all()
    # context['accounts'] = accounts
    
    query = ""
    if request.GET:
        query = request.GET('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
    # context['blog_posts'] = blog_posts
    
    #Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts
    
    return render(request, "FrontEnd/home.html", context)