from django.db import models
from django.contrib.auth.models import User


class Reports(models.Model):
    company = models.CharField(max_length=100, null=False, default='New Company')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} {self.user} - {self.company}'


class StatementOfFinancialPosition(models.Model):
    report = models.OneToOneField(Reports, on_delete=models.CASCADE)
    a = models.FloatField(default=0.00001)
    b = models.FloatField(default=0.00001)
    c = models.FloatField(default=0.00001)
    d = models.FloatField(default=0.00001)
    e = models.FloatField(default=0.00001)
    f = models.FloatField(default=0.00001)
    g = models.FloatField(default=0.00001)
    h = models.FloatField(default=0.00001)
    i = models.FloatField(default=0.00001)
    k = models.FloatField(default=0.00001)
    l = models.FloatField(default=0.00001)
    m = models.FloatField(default=0.00001)
    n = models.FloatField(default=0.00001)
    o = models.FloatField(default=0.00001)
    p = models.FloatField(default=0.00001)
    q = models.FloatField(default=0.00001)
    r = models.FloatField(default=0.00001)


class StatementOfComprehensive(models.Model):
    report = models.OneToOneField(Reports, on_delete=models.CASCADE)
    a = models.FloatField(default=0.00001)
    b = models.FloatField(default=0.00001)
    c = models.FloatField(default=0.00001)
    d = models.FloatField(default=0.00001)
    e = models.FloatField(default=0.00001)
    f = models.FloatField(default=0.00001)
    g = models.FloatField(default=0.00001)
