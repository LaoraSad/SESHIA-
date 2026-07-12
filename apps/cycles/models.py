from datetime import date, timedelta
from django.db import models


class Phase(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'phase'

    def __str__(self):
        return self.name


class EnergyLevel(models.Model):
    label = models.CharField(max_length=50)
    value = models.IntegerField(unique=True)

    class Meta:
        db_table = 'energy_level'

    def __str__(self):
        return f'{self.label} ({self.value})'


class Mood(models.Model):
    name = models.CharField(max_length=80)
    icon = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'mood'

    def __str__(self):
        return self.name


class Cycle(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    expected_length = models.IntegerField(default=28)
    notes = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'cycle'
        indexes = [
            models.Index(fields=['user', '-start_date']),
        ]

    def __str__(self):
        return f'Cycle {self.user} - {self.start_date}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self._generate_phases()

    def _generate_phases(self):
        percentages = [0.18, 0.29, 0.08, 0.45]
        phases = Phase.objects.all().order_by('sort_order')
        current = self.start_date

        for i, phase in enumerate(phases):
            days = max(1, round(self.expected_length * percentages[i]))
            end = current + timedelta(days=days - 1)
            CyclePhase.objects.create(
                cycle=self,
                phase=phase,
                start_date=current,
                end_date=end
            )
            current = end + timedelta(days=1)

    def get_phase_for_date(self, target_date):
        cp = self.phases.filter(
            start_date__lte=target_date, end_date__gte=target_date
        ).first()
        return cp.phase if cp else None

    @property
    def current_phase(self):
        return self.get_phase_for_date(date.today())

    @property
    def day_number(self):
        return (date.today() - self.start_date).days + 1

    @property
    def progress_pct(self):
        return min(100, round((self.day_number / self.expected_length) * 100))


class CyclePhase(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='phases')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'cycle_phase'
        indexes = [
            models.Index(fields=['cycle', 'start_date', 'end_date']),
        ]

    def __str__(self):
        return f'{self.phase.name} ({self.start_date} - {self.end_date})'


class DailyLog(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    energy = models.ForeignKey(EnergyLevel, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    symptoms = models.JSONField(default=list)
    notes = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'daily_log'
        unique_together = ['cycle', 'date']

    def __str__(self):
        return f'Log {self.date} - Cycle {self.cycle_id}'