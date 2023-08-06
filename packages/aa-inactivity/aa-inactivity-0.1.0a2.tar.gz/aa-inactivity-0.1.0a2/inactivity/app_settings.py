from django.conf import settings

# put your app settings here


INACTIVITY_DARK_MODE = getattr(settings, "INACTIVITY_DARK_MODE", False)
