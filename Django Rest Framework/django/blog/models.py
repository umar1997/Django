from django.db import models
# from django.contrib.auth.models import User
# We dont use this because we set up a custom user so dont need this
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    # Create Custom Manager to show only objects posts which are published
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # PROTECT: If someone tries to delete a category it has no effect on the posts
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    # CASCADE: When a User is deleted his posts are also deleted
    author = models.ForeignKey( # User (Which we have commented out cause now we are using the cutom one through settings.AUTH_USER_MODEL)
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    # Related to the Options
    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    # Display in descending order, this published is the feature date
    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
