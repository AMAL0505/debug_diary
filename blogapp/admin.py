from django.contrib import admin
from .models import Category, Blog, Comment,Notification
from tinymce.widgets import TinyMCE
from django import forms

# Create a custom form for the Blog model to use TinyMCE
class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

# Create a custom admin class for Blog
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'created_at', 'is_published', 'user')
    list_filter = ('is_published', 'created_at', 'categories')
    search_fields = ('title', 'description')

# Register your models with the custom admin class
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Notification)