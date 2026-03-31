import os
import sys
import django
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from timetable.models import *
from subjects.models import *
from fees.models import *
from progress.models import *
from attendance.models import *
from exams.models import *
from classes.models import *
from students.models import *
from teachers.models import *

client = Client()

def test_view(url_name, data):
    url = reverse(url_name)
    print(f"\n[{url_name}] Testing POST at {url}...")
    
    # 1. Test GET request
    response = client.get(url)
    if response.status_code != 200:
        print(f"  -> ERROR: GET request returned {response.status_code}")
    else:
        print(f"  -> OK: GET request successful")
        
    # 2. Test POST request
    response = client.post(url, data)
    
    if response.status_code == 302:
        print(f"  -> OK: POST request successful (Redirects to {response.url})")
        return True
    elif response.status_code == 200:
        print(f"  -> ERROR: POST request failed (validation errors).")
        if hasattr(response, 'context_data') and response.context_data and 'form' in response.context_data:
            print("  -> Form Errors:", response.context_data['form'].errors)
        return False
    else:
        print(f"  -> ERROR: POST request returned {response.status_code}")
        return False

import time
import random
RAND_SFX = str(int(time.time()))[-4:] + str(random.randint(10, 99))

try:
    print("--- EXECUTING FORM TESTS ---")
    
    # Keep track of success count
    success = 0
    total = 0

    total += 1
    if test_view("teacher_add", {
        "teacher_id": f"TCH-{RAND_SFX}",
        "name": f"Test Teacher {RAND_SFX}",
        "email": f"teacher{RAND_SFX}@example.com",
        "phone": f"99{str(random.randint(10000000, 99999999))}",
        "designation": "Sr Teacher",
        "subject": "Mathematics",
        "experience_years": "5",
        "joining_date": "2023-01-01"
    }): success += 1
    
    t = Teacher.objects.filter(email=f"teacher{RAND_SFX}@example.com").first()
    t_id = t.id if t else ""
    
    total += 1
    if test_view("subject_add", {
        "name": f"Test Math {RAND_SFX}",
        "description": "Testing Subjects",
        "teacher": t_id
    }): success += 1
    
    sub = Subject.objects.filter(name=f"Test Math {RAND_SFX}").first()
    sub_id = sub.id if sub else ""

    total += 1
    if test_view("class_add", {
        "name": f"Test Class X {RAND_SFX}",
        "section": "A",
        "class_teacher": t_id,
        "capacity": 30
    }): success += 1
    
    c = Class.objects.filter(name=f"Test Class X {RAND_SFX}").first()
    c_id = c.id if c else ""

    total += 1
    if test_view("student_add", {
        "name": f"Test Student {RAND_SFX}",
        "roll_number": f"TX-{RAND_SFX}",
        "email": f"student{RAND_SFX}@example.com",
        "current_class": c_id,
        "blood_group": "A+",
        "contact_number": f"88{RAND_SFX}888",
        "address": "123 Test St",
        "date_of_birth": "2010-01-01"
    }): success += 1

    s = Student.objects.filter(roll_number=f"TX-{RAND_SFX}").first()
    s_id = s.id if s else ""

    total += 1
    if test_view("attendance_add", {
        "student": s_id,
        "date": "2026-04-05", # new date to avoid uniques
        "status": "Present"
    }): success += 1

    total += 1
    if test_view("fee_category_create", {
        "name": f"Test Tuition {RAND_SFX}",
        "description": "Tuition description",
        "is_active": "on"
    }): success += 1

    cat = FeeCategory.objects.filter(name=f"Test Tuition {RAND_SFX}").first()
    cat_id = cat.id if cat else ""

    total += 1
    if test_view("fee_structure_create", {
        "name": f"Test Total Fee {RAND_SFX}",
        "category": cat_id,
        "class_section": c_id,
        "fee_type": "fixed",
        "amount": "1500.00",
        "frequency": "monthly",
        "due_date": "2026-04-15",
        "is_active": "on"
    }): success += 1

    fs = FeeStructure.objects.filter(name=f"Test Total Fee {RAND_SFX}").first()
    fs_id = fs.id if fs else ""

    total += 1
    if test_view("student_fee_create", {
        "student": s_id,
        "fee_structure": fs_id,
        "academic_year": "2023",
        "total_amount": "1500.00",
        "status": "pending"
    }): success += 1

    sf = StudentFee.objects.filter(student_id=s_id).first()
    sf_id = sf.id if sf else ""

    total += 1
    if test_view("fee_payment_create", {
        "student_fee": sf_id,
        "amount": "1500.00",
        "payment_date": "2026-03-31",
        "payment_method": "cash",
        "remarks": "Paid in full"
    }): success += 1

    total += 1
    if test_view("timeslot_add", {
        "period_name": f"Period {RAND_SFX}",
        "start_time": "08:00",
        "end_time": "09:00"
    }): success += 1

    ts = TimeSlot.objects.filter(period_name=f"Period {RAND_SFX}").first()
    ts_id = ts.id if ts else ""

    total += 1
    if test_view("timetable_add", {
        "class_section": c_id,
        "day_of_week": "monday",
        "time_slot": ts_id,
        "subject": sub_id,
        "teacher": t_id
    }): success += 1

    total += 1
    if test_view("marks_add", {
        "student": s_id,
        "subject": sub_id,
        "exam_name": "Mid Term Test",
        "marks": 85,
        "out_of": 100
    }): success += 1
    
    print(f"\n--- SUMMARY: {success}/{total} TESTS PASSED ---")

except Exception as e:
    traceback.print_exc()
