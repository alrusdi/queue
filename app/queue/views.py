# -*- coding: utf-8 -*-
from datetime import datetime
import calendar
import pytils
import hashlib
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import auth


from models import Company, MenuItem, VisitingPoint, VisitRequest, Visitor, VisitAttributes

def index(request):
    return redirect('/company/')

def _get_company(company_id = False):
    if company_id:
        company = Company.objects.get(pk= company_id)
    else:
        company = Company.objects.get(subdomain = 'лефф')
    return company

def companies(request, company_id = False):
    t = loader.get_template('company.html')
    current_company = _get_company(company_id)
    if current_company.get_descendant_count() < 1:
        return redirect('/services/'+company_id)
    c = Context({
                'company':current_company,
                'page':'company',
                'current_user': request.user
                })
    return HttpResponse(t.render(c))

def services(request, company_id, service_id=False):
    t = loader.get_template('service.html')
    current_company = _get_company(company_id)
    if service_id:
        services = MenuItem.objects.get(pk=service_id).get_descendants().filter(parent=service_id)
    else:
        services = current_company.menuitem_set.all()

    if service_id and len(services) < 1:
        return redirect('/choosedate/'+company_id+'/'+service_id)

    c = Context({
                'company': current_company,
                'services': list(services),
                'page':'service',
                'current_user': request.user
                })
    return HttpResponse(t.render(c))

def choosedate(request, company_id, service_id):
    t = loader.get_template('choosedate.html')
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
        print locked, date_from, date_to
        raw_vispoints = list(VisitingPoint.objects.filter(service=service, date_from__gte=date_from, date_to__lte=date_to))
        for vp in raw_vispoints:
            key = vp.date_from.strftime('%Y-%m-%d')
            vispoints[key] = vispoints.get(key, [])
            vispoints[key].append(vp.pk)
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
                vp_ids = set(vispoints[key])
                vals[k1][k2] = {
                    'enabled':bool(vp_ids - set(locked)),
                    'working':vp_ids,
                    'day':d,
                    'date_str': key
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
                'vispoints': vispoints,
                'locked_vispoints': locked,
                'calendar': cal,
                'page': 'apply',
                'current_user': request.user
                })
    return HttpResponse(t.render(c))

def choosetime(request, company_id, service_id, day):
    t = loader.get_template('choosetime.html')
    company = Company.objects.get(pk = company_id)
    service = MenuItem.objects.get(pk = service_id)
    day = [int(i) for i in day.split('-')]
    date_from = datetime(*day)
    date_to = datetime(*day, hour=23, minute=59)
    locked = list(VisitRequest.objects.filter(
        visiting_point__service=service,
        visiting_point__date_from__gte=date_from,
        visiting_point__date_to__lte=date_to,
        ).values('visiting_point__pk'))
    locked = [i['visiting_point__pk'] for i in locked]

    raw_vispoints = list(VisitingPoint.objects.filter(service=service, date_from__gte=date_from, date_to__lte=date_to).order_by('date_from'))

    vispoints = []
    for vp in raw_vispoints:
        vispoints.append({
            'data':vp,
            'enabled': not(vp.pk in locked)
        })
    c = Context({
        'company': company,
        'service': service,
        'vispoints': vispoints,
        'current_user': request.user
    })
    return HttpResponse(t.render(c))

def apply(request, vis_point):
    t = False
    vp = VisitingPoint.objects.get(pk=vis_point)
    if len(vp.visitrequest_set.all()):
        t = loader.get_template('locked.html')
    service = vp.service
    params = list(service.menuitemattribute_set.all())
    company = service.company
    post = {}
    errors = {}
    keys = ['last_name', 'first_name', 'phone']
    keys.extend([i.field_name for i in params])
    vr = False
    pwd = False
    user = False
    if request.method == 'POST':
        post = request.POST
        error_happend = False
        for key in keys:
            if not post.get(key):
                error_happend = True
                errors[key] = u'Поле обязательно для заполнения'
        if not error_happend:
            if request.user.is_authenticated():
                user = request.user
            else:
                user, pwd = get_user_and_password(post)
            if user:
                vr = create_visit_request(user, vp, company, post)
                t = loader.get_template('success.html')
            else:
                errors['password'] = u'Введен неправильный пароль'

    t = t or loader.get_template('apply.html')

    c = Context({
        'company': company,
        'service': service,
        'params': params,
        'vispoint': vp,
        'post': post,
        'errors':errors,
        'visit_request': vr,
        'password': pwd,
        'current_user': request.user
    })
    return HttpResponse(t.render(c))

def create_visit_request(user, visiting_point, company, data):
    try:
        visitor = user.visitor
    except User.DoesNotExist:
        visitor = Visitor(user=user, phone=data['phone'])
        visitor.save()
    vr = VisitRequest(company=company, visitor=visitor, visiting_point=visiting_point)
    vr.save()
    for k,v in data.items():
        if k[0:3]=='sf_':
            va = VisitAttributes(visit_request=vr, attr_id = int(k[3:]), val=v)
            va.save()
    return vr

def get_user_and_password(data):
    uname = pytils.translit.slugify(data['last_name']+data['first_name'][0:1])
    pwd = False
    try:
        user = User.objects.get(username=uname)
        if not data['password'] or not user.check_password(data['password']):
            return False, pwd
    except User.DoesNotExist:
        pwd = data['password'] or hashlib.md5(uname+settings.SECRET_KEY).hexdigest()[0:8]
        user = User.objects.create_user(uname, uname+'@ocheredi-net.com', pwd)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
    return user, pwd

def login(request):
    t = loader.get_template('login.html')
    error = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                try:
                    op = user.operator
                    return redirect('/operator/')
                except:
                    pass
                if user.is_superuser:
                    return redirect('/admin/')
                return redirect('/company/')
            else:
                error = u'Ваш аккаунт заблокирован'
        else:
            error = u'Введен неправильный логин или пароль'
    c = Context({
        'error':error,
        'current_user': request.user
    })
    return HttpResponse(t.render(c))

def logout(request):
    auth.logout(request)
    return redirect('/login/')


def operator(request):
    t = loader.get_template('operator/index.html')
    try:
        op = request.user.operator
        date_from = datetime.now().replace(hour=0, minute=0, second=0)
        date_to = datetime.now().replace(hour=23, minute=59, second=59)
        vps = op.visitingpoint_set.filter(date_from__gte=date_from, date_to__lte=date_to).values('pk')
        vp_ids = [i['pk'] for i in vps]

        visit_requests = VisitRequest.objects.filter(visiting_point__id__in = vp_ids)
    except User.DoesNotExist:
        return redirect('/login/')
    c = Context({
        'current_user': request.user,
        'visit_requests':visit_requests,
    })
    return HttpResponse(t.render(c))

def operator_set_request_status(request, request_id, status):
    try:
        op = request.user.operator
    except User.DoesNotExist:
        return redirect('/login/1')

    try:
        vr = VisitRequest.objects.get(pk=request_id)
    except VisitRequest.DoesNotExist:
        return redirect('/login/2')

    if not vr.visiting_point.operator_id == op.id:
        return redirect('/login/3')

    try:
        vr.status = status
        vr.save()
    except:
        return redirect('/login/4')

    return redirect('/operator/')

def operator_view_request(request, request_id):
    try:
        op = request.user.operator
    except User.DoesNotExist:
        return redirect('/login/1')

    try:
        vr = VisitRequest.objects.get(pk=request_id)
    except VisitRequest.DoesNotExist:
        return redirect('/login/2')

    if not vr.visiting_point.operator_id == op.id:
        return redirect('/login/3')

    t = loader.get_template('operator/view_request.html')
    c = Context({
        'current_user': request.user,
        'visit_request':vr,
        })
    return HttpResponse(t.render(c))