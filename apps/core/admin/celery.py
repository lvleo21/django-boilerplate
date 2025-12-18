from django.contrib import admin

from django_celery_beat.models import (
    PeriodicTask,
    CrontabSchedule,
    ClockedSchedule,
    IntervalSchedule,
    SolarSchedule,
)
from django_celery_beat.admin import (
    PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    CrontabScheduleAdmin as BaseCrontabScheduleAdmin
)

from apps.core.sites import admin_site


admin_site.unregister(PeriodicTask)
admin_site.unregister(CrontabSchedule)
admin_site.unregister(ClockedSchedule)
admin_site.unregister(IntervalSchedule)
admin_site.unregister(SolarSchedule)


@admin.register(PeriodicTask, site=admin_site)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, admin.ModelAdmin):
    ...


@admin.register(CrontabSchedule, site=admin_site)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, admin.ModelAdmin):
    ...
