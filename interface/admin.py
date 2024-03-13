import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import ResultData

class ResultDataAdmin(admin.ModelAdmin):
    search_fields = ['target_url', 'key_name']
    list_display = ['target_url', 'func_name', 'key_name', 'receipt_date']
    list_filter = ['target_url', 'key_name']
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "CSV Export Selected"

admin.site.register(ResultData, ResultDataAdmin)