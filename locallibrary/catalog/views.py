from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Book, BookInstance, Genre, Language, Author
from django.views import generic, View

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import RenewBookModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
        book_instance = get_object_or_404(BookInstance, pk=pk)

        # If this is post request then process form data
        if request.method == 'POST':
            # Create a Form instance and populate it with data from the request(binding):
            form = RenewBookModelForm(request.POST)

            # Check if form is valid:
            if form.is_valid():
                # process the data in form.clean_data as required (here we just write it to the model due_back field)
                book_instance.due_back = form.cleaned_data['due_back']
                book_instance.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('all-borrowed'))
        
        # If it is GET (or any other method) create the default form.
        else:
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
        
        context = {
            'form': form,
            'book_instance': book_instance,
        }
        
        return render(request, 'catalog/book_renew_librarian.html', context)


# Create your views here.
def index(request):
    '''View function for home page of the site.'''
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available book (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    '''Generic class-based view listing books on loan to current user'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LoanedBooksByAllUserListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    '''Generic class-based view listing books on loan to all user (accessible by staff)'''
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 6

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )


class BookListView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Book
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '26/12/2025'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    #Not recommended (potentially security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('author-delete', kwargs={'pk': self.object.pk})
            )