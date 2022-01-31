from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #Aynı tarih için aynı sümüklü böcek ile birden fazla gönderi oluşturmayı önlemek için unique_for_date seçeneğini kullanıyoruz.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # user modeli üstünden postlarımızla ters ilişki kurmak için related_name özelliğini kullanıyoruz.
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
    
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
        """django.urls altında yaşayan reverse fonksiyonu yardımı ile named view bulunur gerekli url parametreleri geçirilir ve mutlak url oluşturulur. Bu modelden türetilen her nesne artık bir mutlak url sahibidir."""