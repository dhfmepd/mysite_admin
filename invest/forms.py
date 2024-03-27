from django import forms
from invest.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['record_date', 'type', 'state', 'ticker', 'price', 'quantity', 'subject', 'content']
        labels = {
            'record_date': 'Date',
            'type': 'Type',
            'state': 'State',
            'ticker': 'Ticker',
            'price': 'Price',
            'quantity': 'Qty',
            'subject': 'Subject',
            'content': 'Content',
        }
