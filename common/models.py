from django.db import models

# Create your models here.
class Code(models.Model):
    group_code = models.CharField(max_length=10)
    detail_code = models.CharField(max_length=10)
    detail_code_name = models.CharField(max_length=100)
    reference_value = models.CharField(max_length=50, null=True, blank=True)
    use_flag = models.BooleanField(default=True)
    sort_no = models.IntegerField()
    remark = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = '공통코드'