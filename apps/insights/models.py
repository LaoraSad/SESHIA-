from django.db import models


class Insight(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.TextField()
    source = models.CharField(max_length=10)  # 'ia' / 'manual'
    generated_at = models.DateTimeField(auto_now_add=True)
    transaction_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'insight'
        indexes = [
            models.Index(fields=['user', '-generated_at']),
        ]

    def __str__(self):
        return f'Insight {self.source} - {self.generated_at.date()}'