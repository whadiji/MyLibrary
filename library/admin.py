from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Borrow

admin.site.register(Book)
admin.site.register(Borrow)
