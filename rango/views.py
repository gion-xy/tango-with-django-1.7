from django.shortcuts import render
from rango.models import (
    Category,
    Page,
)
from rango.forms import CategoryForm


def index(req):
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-views')[:5]
    ctx_dict = {
        'categories': category_list,
        'most_viewed_pages': most_viewed_pages,
    }

    return render(req, 'rango/index.html', ctx_dict)


def about(req):
    return render(req, 'rango/about.html')


def category(req, category_name_slug):
    ctx_dict = {}

    try:
        requested_category = Category.objects.get(slug=category_name_slug)
        ctx_dict['category'] = requested_category
        ctx_dict['category_name'] = requested_category.name

        pages = Page.objects.filter(category=requested_category)
        ctx_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(req, 'rango/category.html', ctx_dict)


def add_category(req):
    if req.method == 'POST':
        form = CategoryForm(req.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(req)
        else:
            print(form.errors)

    else:
        form = CategoryForm()

    ctx_dict = {'form': form}
