import datetime
import logging

from celery import shared_task

from django.contrib.auth.models import User
from django.db.models import Q

from memberaudit.models import Character

from .app_settings import INACTIVITY_DARK_MODE
from .models import InactivityPing, InactivityPingConfig
from .utils import notify_user

logger = logging.getLogger(__name__)


@shared_task
def send_inactivity_ping(user_pk: int, config_pk: int):
    config = InactivityPingConfig.objects.get(pk=config_pk)
    user = User.objects.get(pk=user_pk)
    InactivityPing.objects.create(
        config=config, timestamp=datetime.datetime.utcnow(), user=user
    )
    if not INACTIVITY_DARK_MODE:
        notify_user(user.pk, config.text)


@shared_task
def check_inactivity_for_user(user_pk: int):
    now = datetime.datetime.now(datetime.timezone.utc).date()
    user = User.objects.get(pk=user_pk)
    if (
        user.leaveofabsence_set.filter(
            Q(start__lt=now), Q(end=None) | Q(end__gt=now), ~Q(approver=None)
        ).count()
        == 0
    ):
        last_loa = (
            user.leaveofabsence_set.filter(Q(end__lt=now), ~Q(approver=None))
            .order_by("-end")
            .first()
        )
        for config in InactivityPingConfig.objects.all():
            if config.is_applicable_to(user):
                threshold_date = datetime.datetime.now(
                    datetime.timezone.utc
                ).date() - datetime.timedelta(days=config.days)
                registered = (
                    Character.objects.filter(
                        Q(character_ownership__user__pk=user_pk)
                    ).count()
                    > 0
                )
                active = (
                    Character.objects.filter(
                        Q(character_ownership__user__pk=user_pk),
                        Q(online_status__last_login__gt=threshold_date)
                        | Q(online_status__last_logout__gt=threshold_date),
                    ).count()
                    > 0
                )
                excused = last_loa and (
                    not last_loa.end or threshold_date < last_loa.end
                )
                pinged = (
                    InactivityPing.objects.filter(
                        user__pk=user_pk, config=config
                    ).count()
                    > 0
                )
                if active:
                    InactivityPing.objects.filter(
                        user__pk=user_pk, config=config
                    ).delete()
                if not active and registered and not pinged and not excused:
                    send_inactivity_ping(user_pk, config.pk)


# Inactivity Task
@shared_task
def check_inactivity():
    for user in User.objects.all():
        check_inactivity_for_user(user.pk)
