from django.contrib import admin

from accounts.models import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('system_user', 'rating')


admin.site.register(Author, AuthorAdmin)
