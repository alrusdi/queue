# -*- coding: utf-8 -*-
from django.db import models
from queue.models import Company
from pytils import dt

YEAR_CHOICES = (
    (2012, 2012),
    (2013, 2013)
)

class Calendar(models.Model):
    company = models.ForeignKey(
        Company,
        verbose_name = u'Фирма',
        null=True, blank=True,
    )
    title = models.CharField(u'Название', max_length = 255)
    year = models.IntegerField(u'Год', choices = YEAR_CHOICES)

    def __unicode__(self):
        return u'%s %s (%s)' % (self.year, self.title, self.company if self.company else u'для любой фирмы')

    class Meta:
        verbose_name = u'Календарь'
        verbose_name_plural = u'Календари'

class Day(models.Model):
    calendar = models.ForeignKey(
        Calendar,
        verbose_name = u'Календарь',
    )
    date = models.DateField(u'Дата')
    is_short = models.BooleanField(u'Укороченный день', default=False)
    is_weekend = models.BooleanField(u'Выходной день', default=False)
    is_holiday = models.BooleanField(u'Праздничный день', default=False)

    def __unicode__(self):
        return dt.ru_strftime(u'%d %B %Y  (%a)', self.date, inflected=True) if self.date else u'--'

    class Meta:
        verbose_name = u'День календаря'
        verbose_name_plural = u'Дни календаря'
