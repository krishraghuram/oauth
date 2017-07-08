import poplib
import socket
from django.conf import settings
from django.contrib.auth import get_user_model
import django.core.exceptions

class WebmailAuthenticationBackend(object):
    """
    Authenticate against IIT Guwahati Webmail Servers.
    Use the webmail id, password(not saved), IP of login server
    and valid port.
    Default port is set to ``poplib.POP3_SSL_PORT``.
    """

    def get_user(self, user_id):
        """
        Return user object.
        :param user_id: primary key of user object
        :return: user object
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None

    def authenticate(self, request, **credentials):
        """
        Returns user for credentials provided if credentials are valid.
        Returns ``None`` otherwise.
        :param credentials: keyword arguments
        :return: user object
        """
        socket.setdefaulttimeout(5)
        webmail = credentials.get('webmail').split('@')[0]
        password = credentials.get('password')
        mail_server = credentials.get('mail_server')
        port = credentials.get('port', poplib.POP3_SSL_PORT)

        user_model = get_user_model()
        try:
            kw = {user_model.USERNAME_FIELD+'__contains' : webmail} #Need to use contains because of split in line 33
            user = user_model.objects.get(**kw) 
        except user_model.DoesNotExist:
            print "No user for", user_model.USERNAME_FIELD, ":", webmail
            #No raise. Its perfectly fine, as user object wont exist during first time login. The view handling authentication will handle this case.
            return None 
        ### Not Catching FieldError anymore
        ### Because we are no longer using .get(webmail=webmail)
        ### We are using .get(**kw), with kw containing the USERNAME_FIELD
        ### There is no way that USERNAME_FIELD is not a Field of user_model 
        # except django.core.exceptions.FieldError as e:
            # print "\n", "Webmail is not a Field in", user_model, "\n" #Explain what happened
            # raise #Re-Raise the exception

        try:
            conn = poplib.POP3_SSL(host=mail_server, port=port)
            conn.user(webmail)
            if 'OK' in conn.pass_(password):
                conn.quit()
                return user
        except poplib.error_proto:
            print  "\n"
            print "Poplib Error Proto"
            print "There are multiple reasons for this error. Check Poplib documentation for details."
            print "\n"
            raise #Re-Raise the exception
        except socket.error as e:
            s = e.message
            if e.message=="timed out":
                s = "Socket Timed Out."
            print  "\n"
            print s
            print "\n"
            raise #Re-Raise exception
        except (ValueError, TypeError) as e:
            raise e

