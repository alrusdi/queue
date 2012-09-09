# -*- coding: utf-8 -*-
# Create your views here.
import os
import pkgutil
import pprint
import sys
import pwd

from cgi import escape

def dl(tuples):
    output = u''
    output += '<dl>\n'
    for title, description in tuples:
	if title:
	    output += ' <dt>%s</dt>\n' % escape(title)
	if description:
	    output += ' <dt>%s</dt>\n' % escape(description)
    output += '</dl>\n'
    return output

def group(seq):
    """(seq:(item, category)) -> {category:items}

    Groups items by supplied category, e.g.:
    group((e, e.tags[0]) for e in journal.get_recent_entries(100))

    Lifted from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/498223
    """
    result = {}
    for item, category in seq:
	result.setdefault(category, []).append(item)
    return result

def get_packages():
    return set([modname for importer, modname, ispkg in
	pkgutil.walk_packages(onerror=lambda x:x)
	if ispkg and '.' not in modname])

def format_packages():
    packages = group((pkg, pkg[0].lower()) for pkg in get_packages())
    # convert ('a',['apackage','anotherapackage]) into ('a', 'apackage, anotherapackage')
    packages = [(letter, ', '.join(pkgs)) for letter, pkgs in packages.items()]
    return '<h2>Installed Packages</h2>\n%s' % dl(sorted(packages))

def format_environ(environ):
    return '<h2>Environment (test)</h2>\n%s' % dl(sorted(environ.items()))

def format_python_path():
# differentiate between eggs and regular paths
    eggs = [p for p in sys.path if p.endswith('.egg')]
    paths = [p for p in sys.path if p not in eggs]
    return dl([('Paths', ',\n'.join(paths)),
	('Eggs', ',\n'.join(eggs)),
	])

def format_version():
    version, platform = sys.version.split('\n')
    sysname, nodename, release, osversion, machine = os.uname()
    return '<h2>Version</h2>\n%s' % dl([
	('Python Version', version),
	('Build Platform', platform),
	('OS', sysname),
	('OS Version', osversion),
	('Machine Type', machine),])
       
def format():
    output = u''
    output += 'Effective UID: ' + str(os.geteuid()) + " (" + pwd.getpwuid(os.geteuid())[0] + ")" + '<br>'
    output += '__file__: ' + __file__
    output += '<h1>Python Info</h1>\n'
    output += format_version()
    output += format_python_path()
    output += format_environ(os.environ)
    return output

def page(html):
    print "Content-type: text/html"
    print
    print '<html>\n<head><title>%s Python configuration</title></head>' % os.uname()[1]
    print '<body>\n%s</body>\n</html>' % html

if __name__ == '__main__':
    print format_version()
    print "-----------------------"
    print format_python_path()
    print "-----------------------"
    print format_environ(os.environ)
    print "-----------------------"
    page(format())

from django.http import HttpResponse    
from django.template import Context, loader

def index(request):
    r=HttpResponse()
    r['Content-type']='text/html'
    r.write('<html>\n<head><title>%s Python configuration</title></head>' % os.uname()[1])
    r.write('<body>\n%s</body>\n</html>' % format())
    return r

def logo(request):
    t = loader.get_template('defapp/index.html')
    c = Context({
                })
    return HttpResponse(t.render(c))