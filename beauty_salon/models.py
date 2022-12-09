from datetime import datetime
import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(_('номер телефона'), unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.phone_number)


class Salon(models.Model):
    name = models.CharField(
        'название',
        unique=True,
        max_length=255,
        blank=False
    )
    address = models.CharField(
        'адрес',
        unique=True,
        max_length=255,
        blank=False,
    )
    photo = models.ImageField(
        blank=True,
        verbose_name='фото'
    )

    class Meta:
        verbose_name = _('салон красоты')
        verbose_name_plural = _('салоны красоты')

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(
        'имя и фамилия',
        unique=True,
        max_length=255,
        blank=False,
    )
    photo = models.ImageField(
        blank=True,
        verbose_name='фото'
    )
    specialty = models.CharField(
        'специализация',
        max_length=255
    )
    start_date = models.DateField(
        'дата начала работы',
        blank=True,
        null=True
    )
    experience = models.DurationField('стаж', blank=True, null=True)
    salon = models.ForeignKey(
        Salon,
        on_delete=models.DO_NOTHING,
        related_name='masters',
        verbose_name='салон',
        null=True
    )

    class Meta:
        verbose_name = _('мастер')
        verbose_name_plural = _('мастера')

    def __str__(self):
        return f'{self.specialty} {self.name}'

    def get_experience(self):
        self.experience = datetime.now().date() - self.start_date
        return self.experience
    
    def evaluate_rating(self):
        pass


class Procedure(models.Model):
    name = models.CharField(
        'название',
        unique=True,
        max_length=255,
        blank=False,
    )
    photo = models.ImageField(
        blank=True,
        verbose_name='фото'
    )
    price = models.PositiveIntegerField(
        'цена'
    )
    master = models.ManyToManyField(
        Master,
        related_name='procedures',
        verbose_name='мастера'
    )

    class Meta:
        verbose_name = _('процедура')
        verbose_name_plural = _('процедуры')

    def __str__(self):
        return self.name


class Client(CustomUser):
    photo = models.ImageField(
        blank=True,
        verbose_name='фото'
    )

    class Meta:
        verbose_name = _('клиент')
        verbose_name_plural = _('клиенты')

    def __str__(self):
        return f'Клиент {self.first_name}'


class SchedulePoint(models.Model):
    STATUSES = [
        ('available', 'available'),
        ('busy', 'busy')
    ]
    date = models.DateField('название')
    time = models.TimeField('время записи')
    status = models.CharField(
        'статус',
        max_length=10,
        choices=STATUSES,
        default='available'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='schedule_points',
        verbose_name='мастер',
        null=True
    )

    class Meta:
        verbose_name = _('расписание')
        verbose_name_plural = _('расписания')

    def __str__(self):
        return f'{self.date} {self.time} {self.master} {self.status}'


class Entry(models.Model):
    STATUSES = [
        ('payed', 'payed'),
        ('not_payed', 'not_payed')
    ]
    status = models.CharField(
        'статус',
        max_length=10,
        choices=STATUSES
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.DO_NOTHING,
        related_name='master_entries',
        verbose_name='мастер'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        related_name='client_entries',
        verbose_name='клиент'
    )
    service = models.ForeignKey(
        Procedure,
        on_delete=models.DO_NOTHING,
        related_name='procedure_entries',
        verbose_name='процедура'
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.DO_NOTHING,
        related_name='salon_entries',
        verbose_name='салон'
    )

    class Meta:
        verbose_name = _('запись')
        verbose_name_plural = _('записи')

    def __str__(self):
        return f'{self.salon} {self.service} {self.client}'


class Manager(CustomUser):
    photo = models.ImageField(
        blank=True,
        verbose_name='фото'
    )

    class Meta:
        verbose_name = _('менеджер')
        verbose_name_plural = _('менеджеры')

    def __str__(self):
        return f'Менеджер {self.first_name}'


class SMSCode(models.Model):
    number = models.CharField(
        'код',
        max_length=4,
        blank=True,
    )
    client = models.ForeignKey(
        CustomUser,
        related_name='code',
        verbose_name=_('клиент'),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('СМС код')
        verbose_name_plural = _('СМС коды')

    def __str__(self):
        return self.number


class Comment(models.Model):
    date = models.DateField('дата', auto_created=True)
    text = models.TextField('текст отзыва', blank=True, default='')
    rating = models.PositiveSmallIntegerField('оценка')
    master = models.ForeignKey(
        Master,
        on_delete=models.DO_NOTHING,
        related_name='ratings',
        verbose_name='мастер'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        related_name='comments',
        verbose_name='клиент'
    )

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

    def __str__(self):
        return f'{self.client} - {self.master}'
