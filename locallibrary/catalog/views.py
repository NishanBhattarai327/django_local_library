from django.http import HttpResponse
from django.shortcuts import render

from .models import Book, BookInstance, Genre, Language, Author

# Create your views here.
def index(request):
    '''View function for home page of the site.'''
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available book (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    return render(request, 'index.html', context=context)