from django.contrib import admin

from posts.models import Post, Category, Comment, Censor


class PostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'header', 'rating', 'visible', 'preview')


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
