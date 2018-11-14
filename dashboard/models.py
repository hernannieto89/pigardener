from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class MetaTimer(models.Model):
    start_time = models.IntegerField(validators=[MaxValueValidator(23), MinValueValidator(0)])
    end_time = models.IntegerField(validators=[MaxValueValidator(23), MinValueValidator(0)])
    work_time = models.IntegerField(validators=[MinValueValidator(0)])
    sleep_time = models.IntegerField(validators=[MinValueValidator(0)])
    data_pin = models.IntegerField()

    class Meta:
        abstract = True


class SimpleTimer(MetaTimer):
    name = models.CharField(max_length=200, unique=True)
    process_id = models.IntegerField(unique=True)
    activated = models.BooleanField(default=False)


class ClimateTimer(MetaTimer):
    name = models.CharField(max_length=200, unique=True)
    process_id = models.IntegerField(unique=True)
    activated = models.BooleanField(default=False)
    sensor_name = models.CharField(max_length=200, unique=True)
    mode = models.CharField(max_length=2, choices=['h', 't'])
    limit_type = models.CharField(max_length=2, choices=['lt', 'gt'])
    limit_value = models.IntegerField()


class SimpleSensor(models.Model):
    name = models.CharField(max_length=200, unique=True)
    data_pin = models.IntegerField()
    boss_name = models.ForeignKey(ClimateTimer, on_delete=models.SET_NULL, null=True)
