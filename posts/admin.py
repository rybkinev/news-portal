from django.contrib import admin

from posts.models import Post, Category, Comment, Censor


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'header', 'rating', 'visible', 'preview')
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = ('created_at', 'created_by', 'header')
    search_fields = ('header', 'categories__name')
    actions = [nullfy_rating]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'valid')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_id_id', 'visible', 'created_by_id', 'rating')


class CensorAdmin(admin.ModelAdmin):
    list_display = ('word',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Censor, CensorAdmin)
