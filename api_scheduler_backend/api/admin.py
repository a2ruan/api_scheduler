from django.contrib import admin

# Auto-registering all models to be viewable in admin homepage
from django.apps import apps


models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass