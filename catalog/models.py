from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class Genre(models.Model):

    name = models.CharField(max_length=200,help_text = "Enter a book genre")

    def __str__(self):

        return self.name

class Book(models.Model):

    title = models.CharField(max_length=200)
    auhtor = models.ForeignKey('Author' , on_delete=models.SET_NULL,null=True)
    summary = models.TextField(max_length=1000,help_text = "Enter a brief description")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        

    def __str__(self):
        
        return '%s (%s)' % (self.id,self.book.title)
    
class Author(models.Model):
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    def get_absolute_url(self):
        
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        
        return '%s, %s' % (self.last_name, self.first_name)
