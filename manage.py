# manage.py

import os
import sys
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'django-admin' command
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DevTest.settings')  # Replace 'your_project_name' with your project name

# Make the WSGI application available as 'app' for Vercel
app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)