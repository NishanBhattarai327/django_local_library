from django.contrib import admin
from .models import Book, BookInstance, Language, Author, Genre


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# Register the Admin classes for Book using decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Book', {
            'fields': ('book', 'imprint', 'id')
        }), 
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )

# Register your models here.
# admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(BookInstance)
