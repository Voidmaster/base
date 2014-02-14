import datetime
import os.path

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from tagging.fields import TagField

from markdown import markdown

class Record(models.Model):
    """
    Represents a record from an artist. One artist may have many records.
    """
    title = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/categories/%s" % self.slug
    
class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (1, 'Live'),
        (2, 'Draft'),
        (3, 'Hidden'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='pub_date')
    excerpt = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    image = models.ImageField(upload_to='media')

    video = models.CharField(max_length=250)

    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)

    categories = models.ManyToManyField(Category)
    tags = TagField()

    class Meta:
        verbose_name_plural = "Entries"

    def save(self):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save()

    def get_absolute_url(self):
        return "/weblog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)

    def __unicode__(self):
        return self.title    

class Gender(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(max_length=150)

    class Meta:
        verbose_name_plural = "Genders"

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to='media')
    gender = models.ManyToManyField(Genero)

    class Meta:
        verbose_name_plural = "Artists"
    
    def __unicode__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=100)
    mp3 = models.FileField(upload_to='media', blank=True)
    artist = models.ForeignKey(Artist)

    class Meta:
        verbose_name_plural = "Songs"	
    
    def __unicode__(self):
        return self.title

class Poll(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField()
    pub_date = models.DateField()
    
    def __unicode__(self):
       return self.title

class PollChoice(models.Model):
    choice = models.CharField(max_length=100)
    poll = models.ForeignKey(Encuesta)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice


