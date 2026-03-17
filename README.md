# Student Management System (Django)

A simple Django-based Student Management System (SMS) with web UI and REST API.

## ✅ Features
- Student, Teacher, Class, Attendance, and Marks management.
- Web UI with Bootstrap styling (list/add/edit/delete flows).
- Django admin customization.
- REST API endpoints via Django REST Framework.

## 🚀 Quick Start
### 1) Clone / open project

```sh
cd full_django_sms
```

### 2) (Optional) Create / activate virtual environment

Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```sh
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install manually:
> `pip install django djangorestframework`

### 4) Run migrations

```sh
python manage.py migrate
```

### 5) Create superuser (admin)

```sh
python manage.py createsuperuser
```

### 6) Start server

```sh
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## 🧭 Routes
- Web UI: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`

## 🔐 Admin Credentials (example)
If you created the admin user as described, use those values to log in.

## 📦 Structure
- `students/`, `teachers/`, `classes/`, `attendance/`, `exams/`, `accounts/` — app modules
- `student_management/` — project config
- `templates/` — UI templates

---

If you want custom features (authentication, search, reports, export to CSV/PDF), just ask!
## Contributors
- Raj Gimbhal

---

## 👨‍💻 Author
✨ **Bikash Kumar Yadav** ✨

*Building amazing web applications with Django & Python*
