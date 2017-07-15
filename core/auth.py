import poplib
import socket
from django.conf import settings
from django.contrib.auth import get_user_model
import django.core.exceptions

class WebmailAuthenticationBackend(object):
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None

    def authenticate(self, request, **credentials):
        socket.setdefaulttimeout(5)
        webmail = credentials.get('webmail')
        password = credentials.get('password')
        mail_server = credentials.get('mail_server')

        user_model = get_user_model()
        try:
            kw = {user_model.USERNAME_FIELD : webmail}
            user = user_model.objects.get(**kw) 
        except user_model.DoesNotExist:
            #No raise. Its perfectly fine, as user object wont exist during first time login. The view handling authentication will handle this case.
            return None 

        try:
            # conn = poplib.POP3_SSL(host=mail_server, port=poplib.POP3_SSL_PORT)
            # conn.user(webmail)
            # if 'OK' in conn.pass_(password):
            #     conn.quit()
            #     return user
            if password=="password":
                return user
            else:
                raise poplib.error_proto("-ERR Authentication failed.")
        except poplib.error_proto:
            #For development use only. Use logging later.
            print  "\n"
            print "Poplib Error Proto" 
            print "\n"
            raise #Re-Raise the exception
        except socket.error as e:
            s = e.message
            if e.message=="timed out":
                s = "Socket Timed Out."
            #For development use only. Use logging later.
            print  "\n"
            print s
            print "\n"
            raise #Re-Raise exception
