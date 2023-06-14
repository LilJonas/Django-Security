from django.db import models

class Core(models.Model):
    title = models.CharField(max_length=60)
    permalink = models.CharField(max_length=12, unique=True)
    update_date = models.DateTimeField(verbose_name='Last Updated')
    bodytext = models.TextField('Core Content', blank=True)

    def __str__(self):
        return self.title

# class Guestbook(models.Model):
#     book_name = models.CharField(max_length = 300)
#     author_name = models.CharField(max_length=100)
#     pub_date = models.DateField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.username
