from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.authentication.models import State


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access this app"),
            ("manage_leave", "Can manage leave of absence requests"),
        )


class InactivityPingConfig(models.Model):
    name = models.CharField(
        max_length=48,
        unique=True,
        help_text=_("Internal name for the ping config. Must be unique."),
    )
    days = models.PositiveIntegerField(
        help_text=_("The number of days the user must be inactive.")
    )
    text = models.TextField(
        help_text=_("The text of the message or notification sent to the end user.")
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=_(
            "Groups subject to the inactivity ping. If empty, applies to all groups."
        ),
        related_name="+",
    )

    states = models.ManyToManyField(
        State,
        blank=True,
        help_text=_(
            "States subject to the inactivity ping. If empty, applies to all states."
        ),
        related_name="+",
    )

    class Meta:
        default_permissions = ()

    def __str__(self):
        return _("ping config: %(name)s") % {"name": self.name}

    def is_applicable_to(self, user: User) -> bool:
        is_applicable = True
        if self.groups.count() > 0:
            is_applicable &= self.groups.filter(user=user).count() > 0
        if self.states.count() > 0:
            is_applicable &= self.states.filter(userprofile=user.profile).count() > 0
        return is_applicable


class InactivityPing(models.Model):
    config = models.ForeignKey(InactivityPingConfig, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return _("ping [config='%(config_name)s' user='%(user_name)s']") % {
            "config_name": self.config.name,
            "user_name": self.user.profile.main_character.character_name,
        }


class LeaveOfAbsence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approver = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    start = models.DateField(help_text=_("The start of the leave of absence."))
    end = models.DateField(
        blank=True,
        null=True,
        help_text=_(
            "The end of the leave of absence. Leave blank for an indefinite leave."
        ),
    )
    notes = models.TextField(blank=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return _("%(user_name)s's leave starting %(start)s") % {
            "start": self.start,
            "user_name": self.user.profile.main_character.character_name,
        }

    def clean(self):
        if self.end and self.end < self.start:
            raise ValidationError(_("End date must be after start date."))
