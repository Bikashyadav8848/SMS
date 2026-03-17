from django.contrib.admin import AdminSite

class SMSAdminSite(AdminSite):
    site_header = "Student Management System"
    site_title = "SMS Admin Portal"
    index_title = "Welcome to Student Management System Admin"
    site_url = "/"

admin_site = SMSAdminSite(name='sms_admin')