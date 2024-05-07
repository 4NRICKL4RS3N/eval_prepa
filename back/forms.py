from django.forms import ModelForm, forms
from back.models import User, Project, Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

    def clean_level(self):
        level = self.cleaned_data['level']
        if level < 1 or level > 3:
            raise forms.ValidationError('Level must be between 1 and 3')
        return level

    # mametaka css amle form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': 'inputText'
            })
            field.label_suffix = ''


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': 'inputText'
            })
            field.label_suffix = ''


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'date_start', 'date_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': 'inputText'
            })
            field.label_suffix = ''


def form_factory(model, request=None, instance=None):
    if model == Role:
        return RoleForm(request, instance=instance)
    if model == User:
        return UserForm(request, instance=instance)
    if model == Project:
        return ProjectForm(request, instance=instance)
