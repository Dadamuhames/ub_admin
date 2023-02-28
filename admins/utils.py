import string
import datetime
from django.db.models import Q
import json
from django.apps import apps
from django.core.paginator import Paginator
from django.http import JsonResponse, QueryDict
import re
from django.core.files.storage import default_storage

# search_paginate
def search_pagination(request):
    url = request.path + '?'

    if 'q=' in request.get_full_path():
        if '&' in request.get_full_path():
            url = request.get_full_path().split('&')[0] + '&'
        else:
            url = request.get_full_path() + '&'

    return url



# list to queryset
def list_to_queryset(model_list):
    if len(model_list) > 0:
        return model_list[0].__class__.objects.filter(
            pk__in=[obj.pk for obj in model_list])
    else:
        return []


# list of dicts to queryset
def list_of_dicts_to_queryset(list, model):
    if len(list) > 0:
        return model.objects.filter(id__in=[int(obj['id']) for obj in list])
    else:
        return []






# pagination
def paginate(queryset, request, number):
    paginator = Paginator(queryset, number)

    try:
        page_obj = paginator.get_page(request.GET.get("page"))
    except:
        page_obj = paginator.get_page(request.GET.get(1))

    return page_obj


# get lst data
def get_lst_data(queryset, request, number):
    lst_one = paginate(queryset, request, number)
    page = request.GET.get('page')

    if page is None or int(page) == 1:
        lst_two = range(1, number + 1)
    else:
        start = (int(page) - 1) * number + 1
        end = int(page) * number

        if end > len(queryset):
            end = len(queryset)

        lst_two = range(start, end + 1)


    return dict(pairs=zip(lst_one, lst_two))




# clean text
def clean_text(str):
    for char in string.punctuation:
        str = str.replace(char, ' ')

    return str.replace(' ', '')



# requeired field errors
def required_field_validate(fields: list, data):
    error = {}

    for field in fields:
        if field not in data:
            error[field] = 'This field is reuqired'

    return error


