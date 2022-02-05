from django.contrib import admin

from .models import (
    User, Group, Message, Likes
)

class MessagesInline(admin.TabularInline):
    model = Message
    extra = 5


class LikesInline(admin.TabularInline):
    model = Likes
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','id','email','first_name','last_name']
    list_editable = ['email','first_name','last_name']
    read_only_fields = ['id',]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name','admin',]
    read_only_fields = ['id',]
    # inlines = [MessagesInline, ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'group','id',]
    read_only_fields = ['id',]
    inlines =[LikesInline, ]

@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    pass