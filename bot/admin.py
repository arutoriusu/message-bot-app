from django.contrib import admin
from .models import User, Message
from .forms import UserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    form = UserForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'date_for_send',)
