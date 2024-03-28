from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_note')
    type_choices = (('MM', 'Memo'), ('TD', 'Trade'))
    state_choices = (('SL', 'SELL'), ('BY', 'BUY'))
    record_date = models.CharField(max_length=10)
    type = models.CharField(max_length=2, choices=type_choices)  # 유형 : 단순메모 / 거래기록
    state = models.CharField(max_length=2, choices=state_choices, null=True, blank=True)
    ticker = models.CharField(max_length=10, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    stock_data = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = '투자노트'