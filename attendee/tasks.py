from __future__ import absolute_import

import requests

from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from attendee.models import Attendee

logger = get_task_logger(__name__)


@periodic_task(run_every=crontab(),
               name='check_payments',
               ignore_result=True)
def check_payments():
    attendees = Attendee.objects.exclude(moip_payment_id=None)
    for attendee in attendees:
        return check_payment.delay(attendee)


@task(name='check_payment')
def check_payment(attendee):
    if not attendee.moip_payment_id:
        return

    logger.info('#{} -> {}'.format(
        attendee.pk,
        attendee.moip_payment_status))

    headers = {
        'Content-Type': 'application/json',
        'Authorization': (
            'Basic MEVSVkROMzg2V0UzUlpSSTRZWUc2UUNETE1KNTdMQlI6U1J'
            'aR0hSWFlPVDBQVkRMUkIzWUU4WFFXTE5MQTBKUlhUS09JRFZEUQ=='
        )
    }
    url = 'https://sandbox.moip.com.br/v2/payments/{}'.format(
        attendee.moip_payment_id)
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        attendee.moip_payment_status = data.get('status')
        attendee.save()

    logger.info('#{} -> {}'.format(
        attendee.pk,
        attendee.moip_payment_status))
