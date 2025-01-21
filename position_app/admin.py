from django.contrib import admin
from .models import (
    Division, Position, Employee, Applicant,
    RecruitmentDocument, Contract, ActivityLog
)

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'plantilla_item_no', 'salary_grade', 'status', 'division')
    list_filter = ('status', 'division')
    search_fields = ('title', 'plantilla_item_no')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'year', 'employment_status')
    search_fields = ('last_name', 'first_name')

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position_applied', 'current_stage', 'status')
    list_filter = ('current_stage', 'status')
    search_fields = ('last_name', 'first_name')

@admin.register(RecruitmentDocument)
class RecruitmentDocumentAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'description', 'uploaded_at')
    search_fields = ('applicant__last_name', 'description')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    search_fields = ('action', 'user__username')
    list_filter = ('created_at',)
