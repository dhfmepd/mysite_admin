from django.contrib import admin
from .models import Note, Portfolio

class NoteAdmin(admin.ModelAdmin):
    search_fields = ['record_date', 'type', 'subject']
    list_display = ['record_date', 'type', 'subject', 'create_date', 'modify_date']
    list_filter = ['record_date', 'type', 'create_date']

class PortfolioAdmin(admin.ModelAdmin):
    search_fields = ['type', 'ticker']
    list_display = ['type', 'ticker', 'price', 'quantity', 'amount', 'create_date','modify_date']
    list_filter = ['type', 'ticker']

admin.site.register(Note, NoteAdmin)
admin.site.register(Portfolio, PortfolioAdmin)