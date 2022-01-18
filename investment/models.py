from django.db import models

class Account(models.Model):
    brokerage = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.brokerage + ' - ' + self.nickname + ' ( 계좌번호 : ' + self.number + ' ) '

    class Meta:
        verbose_name_plural = 'Account'

class Market(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' ( 상태 : ' + self.status + ' )'

    class Meta:
        verbose_name_plural = 'Market'

class Stock(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=50)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.account.nickname + ' - ' + self.market.name + '.' + self.ticker + ' ( ' + str(self.quantity) + ' / ' + str(self.price) + ' / ' + str(self.quantity * self.price) + ' )'

    class Meta:
        verbose_name_plural = 'Stock'

