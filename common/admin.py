import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Code

class CodeAdmin(admin.ModelAdmin):
    search_fields = ['group_code']
    list_display = ['group_code', 'detail_code', 'detail_code_name', 'reference_value', 'use_flag', 'sort_no']
    list_filter = ['group_code']
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

admin.site.register(Code, CodeAdmin)