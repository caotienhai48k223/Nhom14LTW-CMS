from django.contrib import admin
from .models import Post, Topic, Profile, Enjoy, Section, Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class EnjoyInline(admin.StackedInline):
  model = Enjoy
  extra = 0
  
class CommentInline(admin.StackedInline):
  model = Comment
  extra = 0
  
class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  inlines = [CommentInline]
  
class SectionAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title')}

class SectionInline(admin.StackedInline):
  model = Section
  extra = 0
  
class TopicAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  inlines = [SectionInline]

  
admin.site.register(Post, PostAdmin)
admin.site.register(Topic, TopicAdmin)


class ProfileInline(admin.StackedInline):
  model = Profile
  can_delete = False
  
class CustomUserAdmin(UserAdmin):
  inlines = (ProfileInline, EnjoyInline,)
  
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)