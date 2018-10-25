"""
Django settings for pur_beurre project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""


from .local import *
import django_heroku
from whitenoise.storage import CompressedManifestStaticFilesStorage

class ErrorSquashingStorage(CompressedManifestStaticFilesStorage):

    def url(self, name, **kwargs):
        try:
            return super(ErrorSquashingStorage, self).url(name, **kwargs)
        except ValueError:
            return name

DEBUG = False

ALLOWED_HOSTS = ['purb.herokuapp.com']


django_heroku.settings(locals())
