from django.contrib import admin
from django.contrib.auth import get_user_model

from beauty_salon.models import (
    SMSCode,
    Master,
    Salon,
    Entry,
    SchedulePoint,
    Procedure,
    Comment
)


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'first_name']


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'photo']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'specialty',
        'photo',
        'start_date',
        'experience',
        'salon'
    ]


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price',
        'photo'
    ]


@admin.register(SchedulePoint)
class SchedulePointAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'time',
        'status',
        'master'
    ]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status',
        'master',
        'client',
        'service',
        'salon'
    ]


@admin.register(SMSCode)
class SMSCodeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'number',
        'client'
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'client',
        'master',
        'rating',
        'text'
    ]

