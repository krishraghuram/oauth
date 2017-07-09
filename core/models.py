from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    WEBMAIL_SERVERS = [
    ('202.141.80.13', 'Dikrong'),
    ('202.141.80.12', 'Teesta'),
    ('202.141.80.9', 'Namboor'),
    ('202.141.80.10', 'Disang'),
    ('202.141.80.11', 'Tamdil'),
    ]
    webmail = models.EmailField(_('webmail address'), unique=True)
    mail_server = models.CharField(_('mail server'), max_length=50, choices=WEBMAIL_SERVERS)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'webmail'
    EMAIL_FIELD = 'webmail'
    REQUIRED_FIELDS = ['mail_server']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def clean(self):
        '''
        Make sure webmail isnt duplicated
        I shouldnt be able to create two users, 
        one with webmail "user" and other with webmail "user@iitg.ernet.in"
        The simplest way to ensure is by removing "@iitg.ernet.in" before saving
        '''
        self.webmail = self.webmail.split('@')[0]

        '''
        We dont want users to have usable passwords, since we want to use WebmailAuthenticationBackend
        '''
        self.set_unusable_password()


    def save(self, *args, **kwargs):
        '''
        Its preferred to call self.full_clean()
        But that returns ValidationError
        {'webmail': [u'Enter a valid email address.'], 'password': [u'This field cannot be blank.']}
        Because we do webmail.split('@')[0] and we leave password empty.
        Thats why we call self.clean()
        '''
        self.clean() # Do some custom checks
        super(User, self).save(*args, **kwargs) # Call the "real" save() method.
