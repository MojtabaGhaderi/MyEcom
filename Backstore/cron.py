from django.db.models import F
from django.utils import timezone
from django_cron import CronJobBase, Schedule
from datetime import timedelta
from .models import ProductModel, DiscountCodeModel

recent_days = 14  # determines how many days we are defining as recent days.


# // runs periodically, change the recently_added field to False, for products which has been added more that
# 'recent_days' ago. //
class RecentlyAddedCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7  # run every 7 days.
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ProductModel.recently_added_cron_job'

    def do(self):
        ProductModel.objects.filter(recently_added=True,
                                    date_added__lt=(timezone.now()
                                                    - timedelta(days=recent_days))).update(recently_added=False)


class TimePeriodOfADiscountCode(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 1  # run everyday.
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'DiscountCodeModel.time_period_cron_job'

    def do(self):
        now = timezone.now()
        DiscountCodeModel.objects.filter(available=True,
                                         time_period__lte=(now - F('date_added'))).update(available=False)



