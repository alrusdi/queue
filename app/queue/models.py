# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.contrib.auth.models import User

class Company(MPTTModel):
    title = models.CharField(
        verbose_name = u'Название',
        max_length=50,
        unique=True
    )
    parent = TreeForeignKey(
        'self',
        verbose_name = u'Базовая фирма',
        help_text = u'Фирма, чьим филиалом является редактируемая в данный момент фирма',
        null=True, blank=True,
        related_name='children'
    )
    subdomain = models.CharField(
        verbose_name = u'Домен',
        max_length=20,
        help_text = u'Домен третьего уровня для фирмы. Если ввести "лефф" то меню фирмы будет на домене лефф.очереди-нет.рф',
        null=True, blank=True
    )
    logo = models.ImageField(
        upload_to = 'logos',
        max_length = 255,
        verbose_name = u'Логотип',
        null=True, blank = True
    )
    info = models.TextField(
        verbose_name = u'Бегущая строка',
        null=True, blank=True
    )

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = u'Фирма'
        verbose_name_plural = u'Фирмы'

class MenuItem(MPTTModel):
    company = models.ForeignKey(
        Company,
        verbose_name = u'Фирма',
    )
    title = models.CharField(
        verbose_name = u'Имя',
        max_length=255
    )
    parent = TreeForeignKey(
        'self',
        verbose_name = u'Родительский пункт меню',
        null=True, blank=True,
        related_name='children')
    icon = models.ImageField(
        upload_to = 'btn_img',
        verbose_name = u'Иконка кнопки',
        null=True, blank=True
    )

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = u'Пункт меню'
        verbose_name_plural = u'Пункты меню'

MENU_ITEM_DATA_TYPE_CHOICES = (
    ('string', u'Строка'),
)

class MenuItemAttribute(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        verbose_name = u'Пункт меню',
    )
    field_title =  models.CharField(
        verbose_name = u'Название',
        max_length=255
    )
    field_type =  models.CharField(
        verbose_name = u'Тип',
        choices = MENU_ITEM_DATA_TYPE_CHOICES,
        max_length=20,
        default = 'string'
    )
    field_description =  models.TextField(
        verbose_name = u'Описание',
        null=True, blank=True
    )

    @property
    def field_name(self):
        return u'sf_%s' % self.pk

    def __unicode__(self):
        return u'%s (%s)' % (self.field_title, self.get_field_type_display())

    class Meta:
        verbose_name = u'Запрашиваемый атрибут'
        verbose_name_plural = u'Запрашиваемые атрибуты'


class Operator(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=u'Аккаунт',
    )
    company = models.ForeignKey(
        Company,
        verbose_name=u'Фирма',
    )
    def __unicode__(self):
        return u'%s (%s)' % (self.user, self.company.title)

    class Meta:
        verbose_name = u'Оператор'
        verbose_name_plural = u'Операторы'

class Visitor(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=u'Аккаунт',
    )
    phone =  models.CharField(
        verbose_name = u'Номер телефона',
        max_length=255
    )

    def __unicode__(self):
        return u'%s %s (%s)' % (self.user.last_name,self.user.first_name, self.phone)

    class Meta:
        verbose_name = u'Посетитель'
        verbose_name_plural = u'Посетители'

class VisitingPoint(models.Model):
    service = models.ForeignKey(
        MenuItem,
        verbose_name = u'Пункт меню'
    )
    operator = models.ForeignKey(
        Operator,
        verbose_name = u'Оператор'
    )
    date_from = models.DateTimeField(u'Начало периода работы')
    date_to = models.DateTimeField(u'Завершение периода работы')

    def __unicode__(self):
        return u'%s %s %s %s-%s' % (
            self.service,
            self.operator,
            self.date_from.strftime('%Y-%m-%d'),
            self.date_from.strftime('%H:%M'),
            self.date_to.strftime('%H:%M')
            )

    class Meta:
        verbose_name = u'График работы'
        verbose_name_plural = u'Графики работы'

VISIT_REQUEST_STATUSES = (
    ('pending', u'Ожидает приема'),
    ('canceled', u'Отменена'),
    ('serving', u'Обслуживается'),
    ('served', u'Обслужена'),
)

class VisitRequest(models.Model):
    company = models.ForeignKey(
        Company,
        verbose_name = u'Фирма'
    )
    visitor = models.ForeignKey(
        Visitor,
        verbose_name=u'Посетитель',
    )
    visiting_point = models.ForeignKey(
        VisitingPoint,
        verbose_name = u'Дата/Время'
    )
    status = models.CharField(
        max_length = 100,
        choices = VISIT_REQUEST_STATUSES,
        default = 'pending'
    )

    def __unicode__(self):
        return u'%s %s' % (self.visitor, self.visiting_point)

    class Meta:
        verbose_name = u'Запись на прием'
        verbose_name_plural = u'Записи на прием'

class VisitAttributes(models.Model):
    visit_request = models.ForeignKey(
        VisitRequest,
        verbose_name = u'Заявка'
    )
    attr = models.ForeignKey(
        MenuItemAttribute,
        verbose_name = u'Аттрибут'
    )
    val = models.TextField(
        verbose_name = u'Значение'
    )

    def __unicode__(self):
        return u'%s %s=%s' % (self.visit_request, self.attr, self.val)

    class Meta:
        verbose_name = u'Значение запрашиваемого аттрибута'
        verbose_name_plural = u'Значения запрашиваемых аттрибутов'
