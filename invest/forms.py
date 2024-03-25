from django import forms
from invest.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['record_date', 'type', 'subject', 'content']
        labels = {
            'record_date': 'Date',
            'type': 'Type',
            'subject': 'Subject',
            'content': 'Content',
        }