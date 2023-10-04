import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.db.models import F
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from posts.models import Post, Subscription

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def sending_new_posts():
    logger.debug(f'Run sending at: {datetime.datetime.now()}')

    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    last_week = today - datetime.timedelta(days=7)

    last_sending_obj = DjangoJobExecution.objects.filter(
        job_id='sending_new_posts',
        status='Executed'
    ).order_by('-run_time').first()

    last_sending = last_sending_obj.run_time if last_sending_obj else last_week

    last_posts = Post.objects \
        .filter(
            visible=True,
            created_at__gt=last_sending
        ).order_by('-created_at')

    emails = Subscription.objects\
        .filter(category__post__in=last_posts)\
        .values_list('category__post', 'user__email')\
        .distinct().order_by('user__email')

    sending_dict = dict()
    for post_id, email in emails:
        post = Post.objects.get(id=post_id)
        if email in sending_dict:
            sending_dict[email].append(post)
        else:
            sending_dict[email] = [post]

    subject = f'Новые посты с {last_sending.strftime("%x")}'
    text_content = (
        'Новые посты на портале:\n'
    )
    html_content = (
        'Новые посты на портале:<br>'
    )
    for mail, posts in sending_dict.items():
        msg = EmailMultiAlternatives(
            subject,
            text_content + '\n'.join([f'http://127.0.0.1{i.get_absolute_url()}' for i in posts]),
            None,
            [mail]
        )

        msg.attach_alternative(
            html_content + '<br>'.join([f'<a href="http://127.0.0.1{i.get_absolute_url()}">{i.header}</a>' for i in posts]),
            "text/html"
        )
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            sending_new_posts,
            trigger=CronTrigger(hour='18', day_of_week=5),
            id="sending_new_posts",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
