from django.db import models

class ResultData(models.Model):
    user_agent = models.CharField(max_length=100)
    target_url = models.CharField(max_length=100)
    soup_data = models.TextField()
    result_data = models.TextField()
    receipt_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = '수신데이터'