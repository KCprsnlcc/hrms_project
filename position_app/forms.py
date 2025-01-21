from django import forms
from .models import Position, Applicant, Contract, Division
# position_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to include email, etc.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PositionForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        required=False,
        empty_label="Select a Division",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Position
        fields = [
            'title',
            'plantilla_item_no',
            'salary_grade',
            'status',
            'division',
            'date_of_publication',
            'expiration_date',
            'target_date_of_appointment',
        ]
class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'last_name',
            'first_name',
            'middle_name',
            'position_applied',
            'current_stage',
            'status',
        ]

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'employee',
            'contract_file',
            'start_date',
            'end_date',
            'is_active',
        ]
