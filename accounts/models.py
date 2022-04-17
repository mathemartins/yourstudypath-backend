import os
import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import date
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from yourstudypath.utils import unique_key_generator, unique_slug_generator_by_email, random_string_generator


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self, DEFAULT_ACTIVATION_DAYS=7):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(activated=False, forced_expired=False).filter(timestamp__gt=start_range,
                                                                         timestamp__lte=end_range)


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(activated=False)


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)  # 7 Days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()  # 1 object
        return bool(qs.exists())

    def activate(self):
        if self.can_activate():
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        return self.key is not None

    def send_activation(self):
        if not self.activated and not self.forced_expired and self.key:
            base_url = getattr(settings, 'BASE_URL', 'https://api.yourstudypath.com')
            key_path = reverse("account-url:email-activate", kwargs={'key': self.key})  # use reverse
            path = "{base}{path}".format(base=base_url, path=key_path)
            context = {
                'path': path,
                'email': self.email
            }
            html_ = get_template("registration/emails/verify.html").render(context)
            subject = 'YSP Email Verification'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [self.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = True
            # message.send()
        return False


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Profile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nin = models.CharField(max_length=255, blank=True, null=True, unique=True,
                           help_text="National Identification Number")
    gender = models.CharField(max_length=20, choices=GENDER, default='Male', blank=True, null=True)
    photo = models.ImageField(upload_image_path, null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.nin

    def get_absolute_url(self):
        return reverse('account:profile-detail', kwargs={'slug': self.slug})

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="%s" width="100" height="100" />' % self.photo.url)

    image_tag.short_description = 'Profile Image'
    image_tag.allow_tags = True

    @property
    def get_image(self):
        if not self.photo:
            return "https://img.icons8.com/officel/2x/user.png"
        return self.photo.url

    def get_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return 0


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired and not instance.key:
        instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()
        Profile.objects.create(
            user=instance,
            slug=unique_slug_generator_by_email(instance),
            uuid=random_string_generator(12),
        )


post_save.connect(post_save_user_create_reciever, sender=User)


class Address(models.Model):
    STATE = (
        ('Lagos', 'Lagos'),
        ('Abuja', 'Abuja'),
        ('Kano', 'Kano'),
        ('Enugu', 'Enugu')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    street = models.CharField(max_length=300, blank=True, null=True, help_text='Block 32, Arizona Street')
    locale = models.CharField(max_length=300)
    state = models.CharField(max_length=255, choices=STATE, blank=True, null=True, help_text='Province/State')
    zip_code = models.CharField(max_length=300, blank=True, null=True)
    country = CountryField(default='NG')

    class Meta:
        db_table = "address"
        verbose_name = "address"
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.name

    def get_address(self):
        return "{address}, {lga} {state} {country}".format(address=self.street, lga=self.locale, state=self.state,
                                                           country=self.country)
