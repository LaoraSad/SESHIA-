from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=20)  # 'income' / 'expense'
    icon = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    light_color = models.CharField(max_length=7, null=True, blank=True)
    is_default = models.BooleanField(default=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'category'
        indexes = [
            models.Index(fields=['user', 'type']),
        ]

    def __str__(self):
        return f'{self.name} ({self.type})'


class Transaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20)  # 'income' / 'expense'
    date = models.DateField()
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction'
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'date', 'type']),
        ]

    def __str__(self):
        return f'{self.type} ${self.amount} - {self.date}'

    @property
    def cycle_phase(self):
        from cycles.models import Cycle, CyclePhase
        cycle = Cycle.objects.filter(
            user=self.user,
            start_date__lte=self.date,
            end_date__gte=self.date
        ).first()
        if not cycle:
            return None
        cp = CyclePhase.objects.filter(
            cycle=cycle,
            start_date__lte=self.date,
            end_date__gte=self.date
        ).first()
        return cp.phase if cp else None