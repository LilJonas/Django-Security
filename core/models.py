from django.db import models

class Core(models.Model):
    title = models.CharField(max_length=60)
    permalink = models.CharField(max_length=12, unique=True)
    update_date = models.DateTimeField(verbose_name='Last Updated')
    bodytext = models.TextField('Core Content', blank=True)

    def __str__(self):
        return self.title

class Guestbook(models.Model):
    first_name = models.CharField(max_length=100)
    user_message = models.CharField(max_length = 300)
    pub_date = models.DateField()