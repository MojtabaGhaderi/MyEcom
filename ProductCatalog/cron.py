from django.utils import timezone
from django_cron import CronJobBase, Schedule
from datetime import timedelta
from .models import ProductModel


class RecentlyAddedCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7  # run every 7 days.
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ProductModel.recently_added_cron_job'

    def do(self):
        ProductModel.objects.filter(recently_added=True,
                                    date_added__lt=(timezone.now()
                                                    - timedelta(days=30))).update(recently_added=False)

