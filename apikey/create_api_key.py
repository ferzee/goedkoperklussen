import os
import django

# Set the environment variable to point to your project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goedkoperklussen.settings')

# Initialize the Django application
django.setup()

import uuid
from apikey.models import APIKey

api_key = APIKey.objects.create(key=uuid.uuid4().hex)
print('created')
