from django.contrib import admin
from django.contrib import admin
from EMedix_App.models import *


# Register UserAdmin

admin.site.register(userinfo)
admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(BookingAppointment)
admin.site.register(medical_records)
admin.site.register(clinic)