from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Quote, Tag, Author
from .forms import AddQuote, AddAuthor

# Create your views here.
from .utils import get_mongodb


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            form.save()

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author.html', {'form': form})

    return render(request, 'quotes/add_author.html', {'form': AddAuthor()})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = AddQuote(request.POST)
        if form.is_valid():
            form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                add_quote.tags.add(tag)

            author_name = request.POST.get('author')
            choice_author = Author.objects.filter(fullname=author_name).first()
            if choice_author:
                add_quote.author = choice_author
                add_quote.save()

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', {"tags": tags, 'authors': authors, 'form': form})

    return render(request, 'quotes/add_quote.html', {"tags": tags, 'authors': authors, 'form': AddQuote()})


def author_about(request, author_id):
    author = get_object_or_404(Author, fullname=author_id)
    return render(request, 'quotes/author.html', {"author": author})


def tagged_quotes(request, tag_name, page=1):
    tags = Tag.objects.all()
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)

    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'quotes/tags.html', context={'quotes': quotes_on_page, 'tags': tags})
