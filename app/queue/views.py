# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from queue.models import Company, MenuItem, VisitingPoint, VisitRequest
from django.shortcuts import redirect
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import pytils

def index(request):
    return redirect('/company/')

def _get_company(company_id = False):
    if company_id:
        company = Company.objects.get(pk= company_id)
    else:
        company = Company.objects.get(subdomain = 'лефф')
    return company

def companies(request, company_id = False):
    t = loader.get_template('index.html')
    current_company = _get_company(company_id)
    if current_company.get_descendant_count() < 1:
        return redirect('/services/'+company_id)
    c = Context({
                'company':current_company,
                'page':'company'
                })
    return HttpResponse(t.render(c))

def services(request, company_id, service_id=False):
    t = loader.get_template('index.html')
    current_company = _get_company(company_id)
    if service_id:
        services = MenuItem.objects.get(pk=service_id).get_descendants().filter(parent=service_id)
    else:
        services = current_company.menuitem_set.all()

    if service_id and len(services) < 1:
        return redirect('/apply/'+company_id+'/'+service_id)

    c = Context({
                'company': current_company,
                'services': list(services),
                'page':'service'
                })
    return HttpResponse(t.render(c))

def apply(request, company_id, service_id):
    t = loader.get_template('index.html')
    company = Company.objects.get(pk = company_id)
    service = MenuItem.objects.get(pk = service_id)
    url_date = datetime(int(request.GET.get('y')), int(request.GET.get('m',1)), 1) if request.GET.get('y', False) else False
    if url_date and url_date <= datetime.now():
        url_date = False
    date_from = url_date or datetime.now()
    # Есть ли доступное для посещения время
    locked = list(VisitRequest.objects.filter(
                                visiting_point__service=service,
                                visiting_point__date_from__gte=date_from
                                ).values('visiting_point__pk'))
    locked = [i['visiting_point__pk'] for i in locked]
    at = list(VisitingPoint.objects.filter(service=service, date_from__gte=date_from).exclude(pk__in=locked))

    vispoints = {}
    cal = False
    if url_date or len(at)>0:
        # Ищем ближайшее доступное для посещения время + 31 день
        date_from =  url_date or at[0].date_from
        date_to = date_from + relativedelta(days = +31)
        locked = list(VisitRequest.objects.filter(
                                    visiting_point__service=service,
                                    visiting_point__date_from__gte=date_from,
                                    visiting_point__date_to__lte=date_to,
                                    ).values('visiting_point__pk'))
        locked = [i['visiting_point__pk'] for i in locked]
        raw_vispoints = list(VisitingPoint.objects.filter(service=service, date_from__gte=date_from, date_to__lte=date_to))
        for vp in raw_vispoints:
            vispoints[vp.date_from.strftime('%Y-%m-%d')] = vp
        cal = {
            'year': int(date_from.strftime('%Y')),
            'month': int(date_from.strftime('%m')),
            'month_str': pytils.dt.ru_strftime(u'%B', date_from),
            'values': []
        }

        vals = calendar.monthcalendar(cal['year'],cal['month'])
        k1=-1
        for w in vals:
            k1 +=1
            k2=-1
            for d in w:
                k2 +=1
                if not d:
                    continue
                key = '%s-%.2d-%.2d' %(cal['year'],cal['month'],int(d))
                if key not in vispoints.keys():
                    continue
                vp = vispoints[key]
                vals[k1][k2] = {
                    'enabled':not(vp.id in locked),
                    'data':vp,
                    'day':d
                    }
        cal['values'] = vals

        cal['next_month_available'] = True

        if cal['next_month_available']:
            cal['next_month'] = cal['month']+1
            cal['next_year'] = cal['year']
            if cal['month']==12:
                cal['next_year'] += 1
                cal['next_month'] = 1

        cal['prev_month_available'] = url_date

        if cal['prev_month_available']:
            cal['prev_month'] = cal['month']-1
            cal['prev_year'] = cal['year']
            if cal['month']==1:
                cal['prev_year'] -= 1
                cal['prev_month'] = 12

    c = Context({
                'company': company,
                'service': service,
                'params': service.menuitemattribute_set.all(),
                'vispoints': vispoints,
                'locked_vispoints': locked,
                'calendar': cal,
                'page': 'apply'
                })
    return HttpResponse(t.render(c))
