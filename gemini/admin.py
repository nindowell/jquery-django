from django.contrib import admin
from gemini.models import Post, Favorited

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ru', 'date_created')


@admin.register(Favorited)
class FavoritedAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_added')
