from django.contrib import admin
from scholar.models import Docs,ApplicationStatus


class DocsAdmin(admin.ModelAdmin):
    list_display = ['student', 'applicant_photo', 'domicile_certificate', 'income_certficate', 'caste_certificate', 'aadhar_card', 'bonafide', 'fee_receipt', 'passbook']
    search_fields = ['student__user__username']  # Allows searching by student's username

# Register your models here.
# admin.site.register(Docs, DocsAdmin)
admin.site.register(ApplicationStatus)

