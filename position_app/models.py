from django.db import models
from django.contrib.auth.models import User

class Division(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    STATUS_CHOICES = [
        ('Vacant', 'Vacant'),
        ('For Selection', 'For Selection'),
        ('For Assumption', 'For Assumption'),
        ('Reposted-For Exam', 'Reposted-For Exam'),
        ('For Interview', 'For Interview'),
        ('For Deliberation', 'For Deliberation'),
        ('Filled', 'Filled'),
        ('Retired', 'Retired'),
        ('Hold', 'Hold'),
    ]

    title = models.CharField(max_length=200)
    plantilla_item_no = models.CharField(max_length=100, unique=True)
    salary_grade = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Vacant')
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_publication = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    target_date_of_appointment = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.plantilla_item_no}"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    # Additional fields from your table structure
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=True, null=True)
    appointment_date = models.DateField(blank=True, null=True)
    publication_date = models.CharField(max_length=50, blank=True, null=True)
    quarter = models.CharField(max_length=10, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    phic_number = models.CharField(max_length=30, blank=True, null=True)
    employment_status = models.CharField(max_length=50, blank=True, null=True)  # e.g., Original, Promotion
    nature_of_employment = models.CharField(max_length=50, blank=True, null=True)  # e.g., Permanent, Temporary

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Applicant(models.Model):
    """
    Tracks external or internal applicants going through the recruitment pipeline
    """
    STAGE_CHOICES = [
        ('Document Review', 'Document Review'),
        ('Examination', 'Examination'),
        ('Interview', 'Interview'),
        ('Deliberation', 'Deliberation'),
        ('Final Appointment', 'Final Appointment'),
    ]

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    position_applied = models.ForeignKey(Position, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    current_stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='Document Review')
    status = models.CharField(max_length=50, blank=True, null=True)  # e.g. "Approved", "Rejected"

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.position_applied.title})"

class RecruitmentDocument(models.Model):
    """
    Documents provided by applicants or for the recruitment process
    """
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    file = models.FileField(upload_to='recruitment_docs/')
    description = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc: {self.applicant} - {self.description}"

class Contract(models.Model):
    """
    Stores contract files and contract duration for employees
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    contract_file = models.FileField(upload_to='contracts/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Contract: {self.employee} ({self.start_date} - {self.end_date})"

class ActivityLog(models.Model):
    """
    Simple audit trail
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
