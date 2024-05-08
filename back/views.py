import base64
import datetime
import io
import json

from django.apps import apps
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseBadRequest, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View

from django.views.generic import TemplateView, DetailView, DeleteView
from django.views.generic import ListView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from back.models import User
from back.models import Role
from back.models import Project

from back.forms import UserForm
from back.forms import RoleForm
from back.forms import form_factory
from back.search_forms import SearchForm


def get_model(model_name):
    try:
        model = apps.get_model("back", model_name)
        return model
    except KeyError:
        raise Http404("Model does not exist")


def generate_pdf(model_name, objects_list, fields):
    generated_date = datetime.datetime.now().strftime("%Y-%m-%d")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, model_name)

    p.setFont("Helvetica", 12)
    p.drawString(100, 730, "Generated on: " + generated_date)

    y = 700  # initial x pos
    x = 100  # initial y pos
    for obj in objects_list:
        x = 100
        for field in fields:
            p.drawString(x, y, str(getattr(obj, field)))
            x += 100
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


class ModelListView(View):
    template_name = 'pages/index.html'

    def get(self, request, model_name):
        model = get_model(model_name)

        sort_by = request.GET.get('sort_by', 'id')  # id io le default raha tsy misy sort_by ao amn le request
        sort_order = request.GET.get('sort_order', 'asc')

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

        if sort_order == 'asc':
            objects_list = objects_list.order_by(sort_by)
        else:
            objects_list = objects_list.order_by("-" + sort_by)

        if request.GET.get('export'):
            buffer = generate_pdf(model_name, objects_list, model.fields_to_show)
            # generated_date = datetime.datetime.now().strftime("%Y-%m-%d")
            # response = FileResponse(buffer, content_type='application/pdf')
            # response['Content-Disposition'] = f'attachment; filename="{model_name}_{generated_date}.pdf"'
            pdf_content = buffer.getvalue()
            encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
            embedded_pdf = f'<embed src="data:application/pdf;base64,{encoded_pdf}" type="application/pdf" width="100%" height="600px" />'
            return HttpResponse(embedded_pdf)

        return render(request, self.template_name,
                      {'form': form, 'search_form': search_form, 'data': objects_list, 'fields': model.fields_to_show,
                       'model_name': model_name, 'sort_order': sort_order})

    def post(self, request, model_name):
        model = get_model(model_name)

        form = form_factory(model, request=request.POST)
        if form.is_valid():
            form.save()
            return self.get(request, model_name)
        else:
            errors = dict([(k, [str(e) for e in v]) for k, v in form.errors.items()])
            return JsonResponse({'success': False, 'errors': errors})


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
