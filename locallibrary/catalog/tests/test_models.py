from django.test import TestCase
from catalog.models import Author

# Create your tests here.

# class Author(models.Model):
#     """Model representing an author."""
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     date_of_death = models.DateField("Dead", null=True, blank=True)

#     class Meta:
#         ordering = ['last_name', 'first_name']
    
#     def get_absolute_url(self):
#         """Returns the URL to access a particular author instance."""
#         return reverse('author-detail', args=[str(self.id)])

#     def __str__(self):
#         """String for representing the Model object."""
#         return f'{self.last_name}, {self.first_name}'

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')
    
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')
    
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'dead')
    
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)
    
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        excepted_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), excepted_object_name)
    
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')
    