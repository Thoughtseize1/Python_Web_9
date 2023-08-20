from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Quote, Author, Tag


# Create your views here.
def main(request, page=1):
    per_page = 5
    paginator = Paginator(Quote.objects.all().order_by('-created_at'), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request, "useful_quotes/index.html", context={"quotes": quotes_on_page}
    )


def author_page(request, author):
    print(author)
    needed_author = Author.objects.get(fullname=author)
    return render(
        request, "useful_quotes/author.html",
        context={"author_name": author, "author_description": needed_author.description,
                 'author_birth_date': needed_author.born_date}
    )


def create_quote(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        quote_text = request.POST.get('quote')
        tags_input = request.POST.get('tags')

        selected_author = Author.objects.get(id=int(request.POST.get('author')))
        tag_names = [tag.strip().replace(',', '') for tag in tags_input.split()]
        for tag in tag_names:
            Tag.objects.get_or_create(name=tag)
        exist_quote = bool(len((Quote.objects.filter(quote=quote_text))))
        if not exist_quote:
            q = Quote.objects.create(
                quote=quote_text,
                author=selected_author
            )
            for tag_name in tag_names:
                tag, *_ = Tag.objects.get_or_create(name=tag_name)
                q.tags.add(tag)

        return redirect('useful_quotes:root')
    context = {'authors': authors}
    return render(request, "useful_quotes/new_quote.html", context)


def create_author(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        new_author_fullname = request.POST.get('fullname')
        new_author_bio = request.POST.get('bio')
        new_author_born_location = request.POST.get('born_location')
        new_author_birthdate = request.POST.get('birthdate')
        parsed_date = datetime.strptime(new_author_birthdate, '%Y-%m-%d')
        formatted_date = parsed_date.strftime('%B %d, %Y')
        Author.objects.get_or_create(
            fullname=new_author_fullname,
            born_date=formatted_date,
            born_location=new_author_born_location,
            description=new_author_bio
        )
        return redirect('useful_quotes:root')
    return render(request, "useful_quotes/new_author.html")
