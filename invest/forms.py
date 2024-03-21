from django import forms
from invest.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['type', 'subject', 'content']
        labels = {
            'type': '유형',
            'subject': '제목',
            'content': '내용',
        }