from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


'''This is the model for the posts'''
class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True, max_length=500)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    post_image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username,
                                               'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.message_html = self.message

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


'''This is the model to add extra images to the above Post model'''
class Prep (models.Model): #(Images)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_prep')
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    image_title = models.CharField(max_length=100, default='')
    image_description = models.CharField(max_length=250, default='')
    sequence = models.SmallIntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])

    class Meta:
        unique_together = (('post', 'sequence'),)
        ordering = ['sequence']

    def __str__(self):
        return str(self.image_title) + " " + str(self.post.title)


