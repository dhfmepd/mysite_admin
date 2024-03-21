from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_note')
    type_options = (('MM', 'Memo'), ('TD', 'Trade'))
    type = models.CharField(max_length=10, choices=type_options)  # 유형 : 단순메모 / 거래기록
    stock_data = models.CharField(max_length=200, null=True, blank=True) # JSON 형태 데이터 : 티커 + 거래유형 + 수량 + 가격 등
    subject = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = '투자노트'