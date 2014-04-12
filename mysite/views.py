import cPickle

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django import forms
from django.shortcuts import render
from django.core.cache import cache
import random
import string
from django.core.exceptions import ValidationError

from namerator.probs import BabyNames


def letter_validator(input_str):
    if input_str and not input_str.isalpha():
        raise ValidationError("Invalid name sting: %(value).", params={'value': input_str})

class name_form(forms.Form):
    start_of_name = forms.CharField(max_length=100, validators=[letter_validator], required=False)
    wackiness = forms.ChoiceField(choices=((1, 'Wacky'), (2, 'Strange')))
    gender = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')))

def input_form(request):
    return render(request, 'input_form.html', {'form': name_form()})

def make_random_name(request):
    # print cache.__dict__.keys()
    f = name_form(request.POST)
    if f.is_valid():
        if 'start_of_name' in f.cleaned_data:
            start = f.cleaned_data['start_of_name']
        else:
            start = random.choice(string.ascii_lowercase)
        number = 100 #f['']

        if 'gender' in f.cleaned_data:
            x = cache.get(f.cleaned_data['gender'])
            if not x:
                x = BabyNames(f.cleaned_data['gender'])
                cache.set(f.cleaned_data['gender'], x, 7200)
        else:
            x = cache.get('F')
            if not x:
                x = BabyNames('F')
                cache.set('F', x, 7200)
        start = "<" + start
        # meg = x.mega_stringify()
        all_names = []
        for i in range(number):
            first_name, prob, real_name = x.generate_name(x.tdict, start=start)
            first_name = first_name.strip("<>").title()
            while first_name in [name['name'] for name in all_names]:
                first_name, prob, real_name = x.generate_name(x.tdict, start=start, n_gram=int(f.cleaned_data['wackiness']))
                first_name = first_name.strip("<>").title()
            all_names.append({'name': first_name, 'p': prob, 'real': real_name})

        all_names.sort(key=lambda x: x['p'], reverse=True)
        t = get_template('random_names.html')
        html = t.render(Context({'names': all_names, 'start': start[1:]}))
    else:
        html = "<center><h1>Y U NO PUT IN LEGITIMATE START OF NAME?</h1></center>"

    return HttpResponse(html)






