# Create the managers in this madule
# Managers are for managing how to,
# create the objects from models

from django.contrib.auth.models import BaseUserManager
import unicodedata
from django.utils.encoding import force_text

# Create the Manager for custom User model
class UserManager(BaseUserManager):

    @classmethod
    def normalize_username(self, username):
        """
        Normalizing the username by unicodedata liblary
        """

        return unicodedata.normalize('NFKC', force_text(username))

    def create_user(self, username, user_type, password=None):
        """
        Creates and saves a User with the given username, 
        user_type and password.
        """

        if not username:
            raise ValueError("نام کاربری به صورت صحیح مورد نیاز می باشد")

        user = self.model(
            username=self.normalize_username(username), 
            user_type=user_type
        )

        if user_type is 1:
            user.person == None

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a Superuser with
        the given username and password.
        """

        user = self.create_user(
            username, 
            user_type=5, 
            password=password
        )

        user.is_admin = True

        user.save(using=self._db)

        return user