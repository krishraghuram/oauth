from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, webmail, mail_server, **extra_fields):
        """
        Creates and saves a User with the given webmail and password.
        """
        if not webmail:
            raise ValueError('The given webmail must be set')
        webmail = self.normalize_email(webmail)
        user = self.model(webmail=webmail, mail_server=mail_server, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, webmail, mail_server, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(webmail, mail_server, **extra_fields)

    def create_superuser(self, webmail, mail_server, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(webmail, mail_server, **extra_fields)
