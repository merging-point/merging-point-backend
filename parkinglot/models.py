from django.db import models


class Parkinglot(models.Model):
    idx = models.IntegerField(primary_key=True)
    management_number = models.CharField(max_length=12)
    parkinglot_name = models.CharField(max_length=26)
    classification = models.CharField(max_length=2)
    parkinglot_type = models.CharField(max_length=2)
    road_name_address = models.CharField(max_length=42, blank=True, null=True)
    number_address = models.CharField(max_length=41, blank=True, null=True)
    parking_compartments_cnt = models.IntegerField()
    level_division = models.CharField(max_length=2)
    running_partial_division = models.CharField(max_length=3)
    operating_days = models.CharField(max_length=26)
    weekday_open_time = models.CharField(max_length=5)
    weekday_close_time = models.CharField(max_length=5)
    saturday_open_time = models.CharField(max_length=5)
    saturday_close_time = models.CharField(max_length=5)
    holiday_open_time = models.CharField(max_length=5)
    holiday_close_time = models.CharField(max_length=5)
    fee_info = models.CharField(max_length=2)
    basic_parking_time = models.IntegerField()
    basic_fee = models.IntegerField()
    extra_time_unit = models.DecimalField(max_digits=4,
                                          decimal_places=1,
                                          blank=True,
                                          null=True)
    extra_fee = models.DecimalField(max_digits=6,
                                    decimal_places=1,
                                    blank=True,
                                    null=True)
    day_ticket_available_hours = models.DecimalField(max_digits=6,
                                                     decimal_places=1,
                                                     blank=True,
                                                     null=True)
    day_ticket_fee = models.DecimalField(max_digits=7,
                                         decimal_places=1,
                                         blank=True,
                                         null=True)
    monthly_ticket_fee = models.DecimalField(max_digits=8,
                                             decimal_places=1,
                                             blank=True,
                                             null=True)
    payment_method = models.CharField(max_length=12, blank=True, null=True)
    special_things = models.CharField(max_length=2090, blank=True, null=True)
    management_organization_name = models.CharField(max_length=22)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    latitude = models.DecimalField(max_digits=13,
                                   decimal_places=10,
                                   blank=True,
                                   null=True)
    longtitude = models.DecimalField(max_digits=14,
                                     decimal_places=10,
                                     blank=True,
                                     null=True)
    data_last_updated = models.DateField()

    class Meta:
        managed = True
        db_table = 'parkinglot'
