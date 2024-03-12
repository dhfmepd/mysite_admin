from django import forms
from interface.models import ResultData

class ResultDataForm(forms.ModelForm):
    class Meta:
        model = ResultData
        fields = ['user_agent', 'target_url', 'soup_data', 'result_data']
        labels = {
            'user_agent': 'User Agent',
            'target_url': 'Target URL',
            'soup_data': 'SOUP Data',
            'result_data': 'Result Data'
        }