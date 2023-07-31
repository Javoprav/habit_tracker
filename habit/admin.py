from django.contrib import admin
from .models import *


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'time', 'is_pleasurable', 'public')
    list_filter = ('name',)