import os


def static_version(request):
    return {'STATIC_VERSION': os.environ.get('STATIC_VERSION', '000')}
