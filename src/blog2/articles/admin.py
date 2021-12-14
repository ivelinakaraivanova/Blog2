from django.contrib import admin

from articles.models import Article

# admin.site.register(Article)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'author')
    date_hierarchy = 'date_published'
    search_fields = ('title', 'description')