from django.db import models

class ResultData(models.Model):
    user_agent = models.CharField(max_length=200)
    target_url = models.CharField(max_length=200)
    func_name = models.CharField(max_length=50)
    key_name = models.CharField(max_length=50)
    base_data = models.TextField(null=True, blank=True)
    result_data = models.TextField()
    receipt_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = '수신데이터'