import random
import string

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.text import slugify


def unique_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title) if not new_slug else new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug


def make_display_price(price):
    naira = round(price, 3)
    return "$%s%s" % (intcomma(int(naira)), ("%0.2f" % naira)[-3:])
