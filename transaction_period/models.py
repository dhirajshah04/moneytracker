from django.db import models

from users.models import User


class TransactionPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'transaction_period'

    def __str__(self):
        return self.name
