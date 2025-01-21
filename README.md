# POSITION MANAGEMENT SYSTEM

Welcome to the HRMS, a comprehensive Django-based Human Resource Management System designed to streamline position management, recruitment workflows, contract handling, reporting & analytics, and more. This README provides an overview of the system, installation instructions, documentation on how to use it, and details on its features.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation & Setup](#installation--setup)
4. [Usage Instructions](#usage-instructions)
5. [System Documentation](#system-documentation)
   - [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
   - [Position Lifecycle Management](#position-lifecycle-management)
   - [Recruitment Workflow Automation](#recruitment-workflow-automation)
   - [Contract Management](#contract-management)
   - [Reporting & Analytics](#reporting--analytics)
   - [Document & File Management](#document--file-management)
   - [Search & Filter Functionality](#search--filter-functionality)
   - [Alerts & Notifications](#alerts--notifications)
   - [Integration with External Systems](#integration-with-external-systems)
6. [Contributing](#contributing)
7. [License](#license)

---

## Overview

The HRMS is a Django and MySQL-based application aimed at managing positions, tracking recruitment processes, handling contracts, generating reports, and more. It features a modern flat UI design, interactive visualizations using Chart.js, and tools for filtering, pagination, exporting to PDF, and printing reports.

---

## Features

- **Role-Based Access Control (RBAC):** Different access levels for HR, Department Head, Executive, and Employee.
- **Position Lifecycle Management:** Create, update, track statuses of positions (Vacant, For Selection, Filled, etc.).
- **Recruitment Workflow Automation:** Manage applicants through various stages (Document Review, Examination, Interview, Deliberation, Final Appointment).
- **Contract Management:** Attach employment contracts, manage renewals, and expiration alerts.
- **Reporting & Analytics:** Interactive charts providing insights on positions, applicants, salary distribution, and contract expirations.
- **Export & Print Reports:** Export reports to PDF and print functionality.
- **Document & File Management:** Central storage for job descriptions, resumes, examination results, and contracts.
- **Search & Filter Functionality:** Advanced search and filtering by department, salary grade, status, etc.
- **Alerts & Notifications:** Custom alerts for recruitment deadlines, contract renewals, and more.
- **Integration Points:** Placeholders for integrating payroll systems and government reporting platforms.
- **Modern UI:** Flat design, animations, hover effects, Boxicons tooltips for insights.

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL
- pip (Python package installer)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KCprsnlcc/hrms_project.git
   cd hrms_project
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database settings:**
   - In `hrms_project/settings.py`, set your MySQL database credentials:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'hrms_db',
             'USER': '',
             'PASSWORD': '',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

5. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set up an admin account.

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/` to access the HRMS.

8. **Set up initial groups and permissions:**
   Create groups like HR, Department Head, Executive, and Employee via Django Admin or a management command (as provided in the source code). Assign users to appropriate groups to enforce RBAC.

---

## Usage Instructions

- **Dashboard:** After logging in, the dashboard displays overall statistics, visual reports, and actionable insights.
- **Navigation:** Use the navigation bar to access different modules: Positions, Applicants, Contracts, Reports, Logs, etc.
- **Search & Filter:** Use the search bars and filters to narrow down lists of positions, applicants, and contracts.
- **Reports Module:** In the reports section, select a time filter (Weekly, Monthly, Annually) to dynamically update charts. Use the print and export PDF buttons to generate hard copies or PDF files of reports.
- **Admin Panel:** Visit `/admin/` to manage data, user groups, permissions, and more if needed.

---

## System Documentation

### Role-Based Access Control (RBAC)
- **HR Role:** Full management rights (create/edit positions, handle applicants, manage contracts).
- **Department Head Role:** Limited management rights within their division.
- **Executive Role:** View dashboards and strategic planning tools.
- **Employee Role:** Limited access to personal details and application status.

### Position Lifecycle Management
- Create and update positions.
- Track positions through statuses such as Vacant, For Selection, Filled, Retired.
- Manage deactivation of obsolete positions.

### Recruitment Workflow Automation
- Manage recruitment stages: Document Review, Examination, Interview, Deliberation, Final Appointment.
- Automated notifications for deadlines and milestones.
- Update applicant status through each stage.

### Contract Management
- Attach and store contract files for each position or employee.
- Alerts for contract expiration and renewal.
- Display contract history per employee/position.

### Reporting & Analytics
- **Interactive Charts:** Visualizations using Chart.js to display data on positions, applicants, salary distribution, and contract expirations.
- **Time Filtering:** Users can filter reports by week, month, or year.
- **Export & Print:** Options to export reports to PDF (using html2pdf.js) or print them directly.

### Document & File Management
- Central repository for uploading job descriptions, resumes, examination results, and contracts.
- Secure file storage and retrieval.

### Search & Filter Functionality
- Advanced search options by department, division, location, salary grade, status.
- Real-time filtering of applicants, positions, contracts.

### Integration with External Systems
- **Payroll Integration:** Sync salary and employee data with external payroll services.
- **Government Compliance:** Link with government platforms for reporting (plantilla reporting, PHIC tracking).
- **Audit Exports:** Export data to CSV/PDF for audits and compliance.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions, bug fixes, or new features.

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit and push your changes.
4. Open a pull request with a description of your modifications.

---

## License

This project is licensed under the [License](LICENSE). See the LICENSE file for details.

---

Enjoy using the HRMS! For further assistance, please refer to the project documentation or contact the development team.