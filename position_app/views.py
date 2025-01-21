from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q  # For combined search filters
from .models import (
    Position, Applicant, Employee, Contract, ActivityLog
)
from .forms import PositionForm, ApplicantForm, ContractForm
# position_app/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally, log the user in immediately
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def log_activity(user, action, details=""):
    ActivityLog.objects.create(
        user=user if user.is_authenticated else None,
        action=action,
        details=details
    )
@login_required
def dashboard_view(request):
    """
    Enhanced dashboard showing:
    - Basic stats (Positions count, Vacant, Filled, Applicants)
    - Top Applicants (Final Appointment) with search & pagination (5 per page)
    - Recently Filled Positions with search & pagination (5 per page)
    - Vacancy Analysis by status
    """
    # 1. Basic stats
    position_count = Position.objects.count()
    vacant_count = Position.objects.filter(status='Vacant').count()
    filled_count = Position.objects.filter(status='Filled').count()
    applicant_count = Applicant.objects.count()

    # 2. Top Applicants (Final Appointment) with search + pagination
    top_query = request.GET.get('top_search', '')
    top_applicants_qs = Applicant.objects.filter(current_stage='Final Appointment')
    if top_query:
        top_applicants_qs = top_applicants_qs.filter(
            Q(last_name__icontains=top_query) | Q(first_name__icontains=top_query)
        )

    top_paginator = Paginator(top_applicants_qs, 5)  # 5 per page
    top_page_number = request.GET.get('top_page')
    top_applicants_page = top_paginator.get_page(top_page_number)

    # 3. Recently Filled Positions with search + pagination
    filled_query = request.GET.get('filled_search', '')
    filled_qs = Position.objects.filter(status='Filled').exclude(target_date_of_appointment__isnull=True)
    if filled_query:
        filled_qs = filled_qs.filter(
            Q(title__icontains=filled_query) | Q(plantilla_item_no__icontains=filled_query)
        )

    filled_paginator = Paginator(filled_qs, 5)  # 5 per page
    filled_page_number = request.GET.get('filled_page')
    recently_filled_positions_page = filled_paginator.get_page(filled_page_number)

    # 4. Vacancy Analysis (positions_by_status)
    positions_by_status = (
        Position.objects.values('status')
        .annotate(count=Count('status'))
        .order_by('-count')
    )

    # 5. (Optional) Log Activity
    # log_activity(request.user, "Visited Dashboard with Extended Stats")

    # 6. Context
    context = {
        'position_count': position_count,
        'vacant_count': vacant_count,
        'filled_count': filled_count,
        'applicant_count': applicant_count,

        # Paginated top applicants
        'top_applicants': top_applicants_page,
        'top_query': top_query,

        # Paginated recently filled
        'recently_filled_positions': recently_filled_positions_page,
        'filled_query': filled_query,

        # Vacancy analysis data
        'positions_by_status': positions_by_status,
    }
    return render(request, 'position_app/dashboard.html', context)

@login_required
def position_list_view(request):
    query = request.GET.get('q', '')
    queryset = Position.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(plantilla_item_no__icontains=query)
        )

    # Paginate: 10 per page
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    positions_page = paginator.get_page(page_number)

    log_activity(request.user, "Viewed Position List", details=f"Search query: {query}")

    return render(request, 'position_app/position_list.html', {
        'positions': positions_page,
        'search_query': query
    })


@login_required
def position_detail_view(request, pk):
    position = get_object_or_404(Position, pk=pk)
    log_activity(request.user, "Viewed Position Detail", details=f"Position ID: {position.pk}")
    return render(request, 'position_app/position_detail.html', {'position': position})
@login_required
@permission_required('position_app.add_position', raise_exception=True)
def position_create_view(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save()
            messages.success(request, "Position created successfully.")
            return redirect('position_list')
    else:
        form = PositionForm()

    return render(request, 'position_app/position_create.html', {'form': form})


@login_required
def applicant_list_view(request):
    query = request.GET.get('q', '')
    queryset = Applicant.objects.all().order_by('-application_date')
    if query:
        queryset = queryset.filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query)
        )

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    applicants_page = paginator.get_page(page_number)

    log_activity(request.user, "Viewed Applicant List", details=f"Search query: {query}")

    return render(request, 'position_app/candidate_list.html', {
        'applicants': applicants_page,
        'search_query': query
    })


@login_required
def applicant_detail_view(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    log_activity(request.user, "Viewed Applicant Detail", details=f"Applicant ID: {applicant.pk}")
    return render(request, 'position_app/candidate_detail.html', {'applicant': applicant})

@login_required
@permission_required('position_app.add_applicant', raise_exception=True)
def applicant_create_view(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant_obj = form.save()
            messages.success(request, "Applicant created successfully.")
            log_activity(request.user, "Created Applicant", details=f"Applicant: {applicant_obj.last_name}")
            return redirect('applicant_list')
    else:
        form = ApplicantForm()
    return render(request, 'position_app/candidate_create.html', {'form': form})

@login_required
def contract_list_view(request):
    query = request.GET.get('q', '')
    queryset = Contract.objects.all().order_by('-start_date')
    if query:
        # Example: search by employee last_name or contract file name
        queryset = queryset.filter(
            Q(employee__last_name__icontains=query) |
            Q(contract_file__icontains=query)
        )

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    contracts_page = paginator.get_page(page_number)

    log_activity(request.user, "Viewed Contract List", details=f"Search query: {query}")

    return render(request, 'position_app/contracts_list.html', {
        'contracts': contracts_page,
        'search_query': query
    })


@login_required
def contract_detail_view(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    log_activity(request.user, "Viewed Contract Detail", details=f"Contract ID: {contract.pk}")
    return render(request, 'position_app/contract_detail.html', {'contract': contract})

@login_required
@permission_required('position_app.add_contract', raise_exception=True)
def contract_create_view(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract_obj = form.save()
            messages.success(request, "Contract added successfully.")
            log_activity(request.user, "Created Contract", details=f"Contract ID: {contract_obj.pk}")
            return redirect('contract_list')
    else:
        form = ContractForm()
    return render(request, 'position_app/contract_detail.html', {'form': form, 'is_create': True})
@login_required
def activity_logs_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view activity logs.")

    query = request.GET.get('q', '')
    logs_qs = ActivityLog.objects.all().order_by('-created_at')
    if query:
        logs_qs = logs_qs.filter(
            Q(action__icontains=query) |
            Q(details__icontains=query) |
            Q(user__username__icontains=query)
        )

    paginator = Paginator(logs_qs, 10)
    page_number = request.GET.get('page')
    logs_page = paginator.get_page(page_number)

    return render(request, 'position_app/activity_logs.html', {
        'logs': logs_page,
        'search_query': query
    })


@login_required
def reports_view(request):
    """
    Renders the reports page with Chart.js
    The actual data for charts is fetched from `reports_data` endpoint (JSON).
    """
    log_activity(request.user, "Viewed Reports Page")
    return render(request, 'position_app/reports.html')

@login_required
def reports_data_view(request):
    """
    Returns JSON data for chart consumption
    Example: Count positions by status
    """
    positions_data = {}
    statuses = [
        'Vacant', 'For Selection', 'For Assumption',
        'Reposted-For Exam', 'For Interview',
        'For Deliberation', 'Filled', 'Retired', 'Hold'
    ]
    for status in statuses:
        count = Position.objects.filter(status=status).count()
        positions_data[status] = count

    # Another example: Applicants by current_stage
    applicants_data = {}
    stages = [
        'Document Review', 'Examination',
        'Interview', 'Deliberation', 'Final Appointment'
    ]
    for stage in stages:
        applicants_data[stage] = Applicant.objects.filter(current_stage=stage).count()

    # You can add more data sets for the front-end charts
    return JsonResponse({
        'positionsData': positions_data,
        'applicantsData': applicants_data
    })
