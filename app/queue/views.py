# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from queue.models import Company, MenuItem
from django.shortcuts import redirect

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
                'company':current_company
                })
    return HttpResponse(t.render(c))

def services(request, company_id, service_id=False):
    t = loader.get_template('index.html')
    current_company = _get_company(company_id)
    if service_id:
        services = MenuItem.objects.get(pk=service_id).get_descendants()
    else:
        services = current_company.menuitem_set.all()

    if service_id and len(services) < 1:
        return redirect('/apply/'+company_id+'/'+service_id)

    c = Context({
                'company': current_company,
                'services': list(services)
                })
    return HttpResponse(t.render(c))

def apply(request, company_id, service_id):
    t = loader.get_template('index.html')
    company = Company.objects.get(pk = company_id)
    service = MenuItem.objects.get(pk = service_id)


    c = Context({
                'company': company,
                'services': [service],
                'params': service.menuitemattribute_set.all()
                })
    return HttpResponse(t.render(c))
