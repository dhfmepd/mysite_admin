from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=18)
    message = models.CharField(max_length=1000)
    create_date = models.DateTimeField()

    def __str__(self):
        return '( ' + self.name + ' / ' + self.email + ' / ' + self.phone + ' / ' + str(self.create_date) + ' ) :: ' + self.message

    class Meta:
        verbose_name_plural = 'Contact'