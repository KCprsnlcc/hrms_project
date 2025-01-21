from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from position_app.models import Position, Applicant, Contract

class Command(BaseCommand):
    help = 'Create default user groups with permissions.'

    def handle(self, *args, **options):
        # Create groups
        hr_group, _ = Group.objects.get_or_create(name='HR')
        dept_head_group, _ = Group.objects.get_or_create(name='DepartmentHead')
        exec_group, _ = Group.objects.get_or_create(name='Executive')
        employee_group, _ = Group.objects.get_or_create(name='Employee')

        # Grab some permissions
        add_position = Permission.objects.get(codename='add_position')
        change_position = Permission.objects.get(codename='change_position')
        view_position = Permission.objects.get(codename='view_position')

        add_applicant = Permission.objects.get(codename='add_applicant')
        change_applicant = Permission.objects.get(codename='change_applicant')
        view_applicant = Permission.objects.get(codename='view_applicant')

        add_contract = Permission.objects.get(codename='add_contract')
        change_contract = Permission.objects.get(codename='change_contract')
        view_contract = Permission.objects.get(codename='view_contract')

        # HR group - Full control
        hr_group.permissions.set([
            add_position, change_position, view_position,
            add_applicant, change_applicant, view_applicant,
            add_contract, change_contract, view_contract
        ])

        # Department Head - can view, change positions/applicants
        dept_head_group.permissions.set([
            view_position, change_position,
            view_applicant, change_applicant,
            view_contract
        ])

        # Executive - mostly view
        exec_group.permissions.set([
            view_position, view_applicant, view_contract
        ])

        # Employee - minimal view access
        employee_group.permissions.set([
            view_position, view_applicant
        ])

        self.stdout.write(self.style.SUCCESS("Default groups created/updated with necessary permissions."))
