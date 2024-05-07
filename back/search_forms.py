from django import forms


class SearchForm(forms.Form):
    def __init__(self, *args, model, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in model._meta.fields:
            if field.get_internal_type() == 'CharField':
                self.fields[field.name] = forms.CharField(required=False)
            elif field.get_internal_type() == 'IntegerField':
                self.fields[field.name] = forms.IntegerField(required=False)
                self.fields[f'{field.name}_operator'] = forms.ChoiceField(choices=[('>', '>'), ('<', '<'), ('=', '=')], required=False)
            elif field.get_internal_type() == 'DateField':
                self.fields[field.name] = forms.DateField(required=False)
                self.fields[f'{field.name}_operator'] = forms.ChoiceField(choices=[('>', '>'), ('<', '<'), ('=', '=')], required=False)
