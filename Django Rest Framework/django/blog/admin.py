from django.contrib import admin
from . import models

# Finally, determine which of your application’s models should be editable 
# in the admin interface. For each of those models, register them with the 
# admin as described in ModelAdmin.

@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(models.Category)

# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/