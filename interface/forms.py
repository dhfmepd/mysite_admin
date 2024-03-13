from django import forms
from interface.models import ResultData

class ResultDataForm(forms.ModelForm):
    class Meta:
        model = ResultData
        fields = ['user_agent', 'target_url', 'func_name', 'key_name', 'base_data']
        labels = {
            'user_agent': 'User Agent',
            'target_url': 'Target URL',
            'func_name': 'Function Name',
            'key_name': 'Key Name',
            'base_data': 'Base Data(JSON)'
        }