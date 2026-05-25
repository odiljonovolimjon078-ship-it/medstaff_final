from django.contrib import admin
from .models import Hospital, Staff


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital_type', 'region', 'address', 'staff_count', 'is_active']
    list_filter = ['hospital_type', 'region', 'is_active']
    search_fields = ['name', 'address']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'age', 'position', 'hospital', 'experience_years', 'shift', 'is_active']
    list_filter = ['position', 'shift', 'is_active', 'hospital__region']
    search_fields = ['first_name', 'last_name', 'specialization']
