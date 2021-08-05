from django.contrib import admin
from rango.models import Category, Page, UserProfile, Comment, Friend, LikedCat

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Friend)
admin.site.register(LikedCat)