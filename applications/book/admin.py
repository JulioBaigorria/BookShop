from django.contrib import admin
from .models import Author, Book, Category


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date_created')
    list_filter = ('date_created', 'category')
    ordering = ('author',)


admin.site.register(Author)
admin.site.register(Category)
