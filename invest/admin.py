from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
    search_fields = ['record_date', 'type', 'subject']
    list_display = ['record_date', 'type', 'subject', 'create_date', 'modify_date']
    list_filter = ['record_date', 'type', 'create_date']

admin.site.register(Note, NoteAdmin)