import json

from django.apps import apps
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View

from django.views.generic import TemplateView, DetailView, DeleteView
from django.views.generic import ListView

from back.models import User
from back.models import Role
from back.models import Project

from back.forms import UserForm
from back.forms import RoleForm
from back.forms import form_factory
from back.search_forms import SearchForm


def get_model(model_name):
    try:
        print("--------------------------------------------------------")
        model = apps.get_model("back", model_name)
        return model
    except KeyError:
        raise Http404("Model does not exist")


class ModelListView(View):
    template_name = 'pages/index.html'

    def get(self, request, model_name):
        model = get_model(model_name)

        search_form = SearchForm(request.GET, model=model)
        form = form_factory(model)

        if search_form.is_valid():
            query = Q()
            for field in model._meta.fields:
                if field.get_internal_type() == 'CharField':
                    if search_form.cleaned_data.get(field.name):
                        query &= Q(**{f'{field.name}__icontains': search_form.cleaned_data[field.name]})
                elif field.get_internal_type() in ['IntegerField', 'DateField']:
                    if search_form.cleaned_data.get(field.name):
                        operator = search_form.cleaned_data.get(f'{field.name}_operator')
                        value = search_form.cleaned_data[field.name]
                        # lookup = f'{field.name}__{operator}'
                        lookup = f'{field.name}'
                        if operator == '>':
                            lookup += '__gt'
                        elif operator == '<':
                            lookup += '__lt'
                        elif operator == '=':
                            lookup += '__exact'
                        query &= Q(**{lookup: value})
            objects_list = model.objects.filter(query)
        else:
            objects_list = []

        return render(request, self.template_name, {'form': form, 'search_form': search_form, 'data': objects_list, 'fields': model.fields_to_show, 'model_name': model_name})

    def post(self, request, model_name):
        model = get_model(model_name)

        form = form_factory(model, request=request.POST)
        if form.is_valid():
            form.save()
            # return JsonResponse({'success': True})
            return self.get(request, model_name)
        else:
            errors = dict([(k, [str(e) for e in v]) for k, v in form.errors.items()])
            return HttpResponseBadRequest(json.dumps({'errors': errors}), content_type='application/json')
            # return JsonResponse({'errors': errors}, status=403)
            # return self.get(request, model_name)


class ModelDeleteView(View):
    template_name = 'pages/model-delete.html'

    def get(self, request, model_name, pk):
        model = get_model(model_name)
        instance = get_object_or_404(model, pk=pk)
        return render(request, self.template_name, {'object': instance, 'model_name': model_name})

    def post(self, request, model_name, pk):
        model = get_model(model_name)
        instance = get_object_or_404(model, pk=pk)
        instance.delete()
        return redirect(reverse('index', args=[model_name]))

class ModelUpdateView(View):
    template_name = 'pages/model-update.html'

    def get(self, request, model_name, pk):
        model = get_model(model_name)
        instance = get_object_or_404(model, pk=pk)
        form = form_factory(model, instance=instance)
        return render(request, self.template_name, {'object': instance, 'model_name': model_name, 'form': form})

    def post(self, request, model_name, pk):
        model = get_model(model_name)
        instance = get_object_or_404(model, pk=pk)
        form = form_factory(model, request=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('index', args=[model_name]))
        else:
            return self.get(request, model_name, pk)

class ModelDetailView(View):
    template_name = 'pages/model-detail.html'
