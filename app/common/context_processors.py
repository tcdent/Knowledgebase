from django.conf import settings

def site(request):
    """
    Add site-related variables to the context.
    """
    return {
        'SITE_ID': settings.SITE_ID, 
        'SITE_NAME': settings.SITE_NAME, 
    }

