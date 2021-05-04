from django.db import models
from django.db.models.deletion import SET_NULL
from django.template.defaultfilters import slugify
from django.urls import reverse
from user.models import User


class MainTitle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user',blank=True,null=True)
    title = models.CharField(max_length=250,blank=True,null=True)
    slug = models.SlugField(unique=True,blank=True,null=True)
    image = models.ImageField(upload_to='maintitle',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("maintitle", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            print(self.slug)
        super().save(*args, **kwargs)


class SubTitle(models.Model):
    maintitle = models.ForeignKey(MainTitle, on_delete=models.CASCADE,related_name='subtitle')
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True,blank=True,null=True)
    image = models.ImageField(upload_to='subtitle',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    available_on = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


    def get_absolute_url(self):
        return reverse("subtitle", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(SubTitle, self).save(*args, **kwargs)
