from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """
    Work with new User model
    """
    def create_user(self, email, password=None, **extra_fields):
        " create new user "
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        " create superuser "
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # check extra_fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """ User model """
    email = models.EmailField(unique=True,
                              db_index=True,
                              verbose_name='Email')
    username = models.CharField(max_length=150,
                                blank=True,
                                null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    """
    Profiles for user
    """
    user = models.ForeignKey(User,
                             related_name='profile',
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,
                             blank=True,
                             null=True,
                             validators=[
                                 RegexValidator(
                                     regex=r'^\+?1?\d{9,15}$',
                                     message="Phone number must be in format: '+999999999'.\
                                     Up to 15 digits allowed."
                                 )
                             ],
                             verbose_name='Phone number')
    city = models.CharField(max_length=30,
                            blank=True,
                            null=True)
    address = models.CharField(max_length=150, blank=True, null= True)
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'',
                message="Your index isn't valid. Input correct index"
                )
            ],
             verbose_name='Postal code'
    )