import cPickle

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django import forms
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
import datetime
import random
import string

from namerator.probs import BabyNames


class name_form(forms.Form):
    start_of_name = forms.CharField(max_length=100)
    wackiness = forms.ChoiceField(choices=((1, 'Wacky'), (2, 'Strange'), (3, 'Interesting')))
    gender = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')))

def input_form(request):
    return render(request, 'input_form.html', {'form': name_form()})

def make_random_name(request):
    # print cache.__dict__.keys()
    if 'start_of_name' in request.GET:
        start = request.GET['start_of_name']
    else:
        start = random.choice(string.ascii_lowercase)
    number = 100 #request.GET['']

    if 'gender' in request.GET:
        x = cache.get(request.GET['gender'])
        if not x:
            print "Not using cache :("
            x = BabyNames(request.GET['gender'])
            cache.set(request.GET['gender'], x, 7200)
        else:
            print "Using Cache!"
    else:
        x = cache.get('F')
        if not x:
            x = BabyNames('F')
            cache.set('F', x, 7200)
    start = "<" + start
    meg = x.mega_stringify()
    all_names = []
    for i in range(number):
        first_name, prob = x.generate_name(x.tdict, start=start)
        first_name = first_name.strip("<>").title()
        while first_name in [name['name'] for name in all_names]:
            first_name, prob = x.generate_name(x.tdict, start=start, n_gram=int(request.GET['wackiness']))
            first_name = first_name.strip("<>").title()
        all_names.append({'name': first_name, 'p': prob})

    all_names.sort(key=lambda x: x['p'], reverse=True)
    t = get_template('random_names.html')
    html = t.render(Context({'names': all_names, 'start': start[1:]}))

    return HttpResponse(html)






