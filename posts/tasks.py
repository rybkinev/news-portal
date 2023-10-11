import logging

from celery import shared_task
import time

from posts.models import Post

logger = logging.getLogger(__name__)


@shared_task
def send_mail(post_id):
    logger.info('run task send mail')
    Post.sending_mail(post_id)


@shared_task
def sending_last_posts():
    logger.info('run task sending last posts')
    Post.sending_new_posts()
