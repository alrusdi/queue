# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings

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
        max_length=20
    )
    field_description =  models.TextField(
        verbose_name = u'Описание',
        null=True, blank=True
    )

    def __unicode__(self):
        return u'%s (%s)' % (self.field_title, self.get_field_type_display())

    class Meta:
        verbose_name = u'Запрашиваемый атрибут'
        verbose_name_plural = u'Запрашиваемые атрибуты'

