from django.contrib import admin
from .models import Article, Comment, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_date", "category")
    list_filter = ("category", "created_date")
    search_fields = ("title", "content")

# admin.py
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'article', 'created_date')
    search_fields = ('content', 'guest_name', 'user__username')
    list_filter = ('created_date',)

    def author_name(self, obj):
        return obj.author_name
    author_name.short_description = "Автор"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)