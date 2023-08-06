from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.signals import register_mail_placeholders
from pretix.control.signals import nav_event

from .models import QuestionPlaceholder
from .placeholder import QuestionMailPlaceholder


def get_placeholders_for_event(event):
    return QuestionPlaceholder.objects.filter(question__event=event)


@receiver(register_mail_placeholders, dispatch_uid="placeholder_custom")
def register_mail_question_placeholders(sender, **kwargs):
    return [
        QuestionMailPlaceholder(placeholder)
        for placeholder in get_placeholders_for_event(sender)
    ]


@receiver(nav_event, dispatch_uid="question_placeholders_nav")
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(
        request.organizer, request.event, "can_change_event_settings"
    ):
        return []
    return [
        {
            "label": _("Email placeholders"),
            "icon": "question-circle-o",
            "url": reverse(
                "plugins:pretix_question_placeholders:list",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_question_placeholders",
        }
    ]
