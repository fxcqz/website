from django.contrib import admin
from .models import ListItem, Post, Section

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ("title",)}

class SectionAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ("title",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ListItem)