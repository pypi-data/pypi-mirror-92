from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.signals import event_copy_data, register_mail_placeholders
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


@receiver(event_copy_data, dispatch_uid="question_placeholders_clone")
def copy_event_placeholders(sender, other, question_map, **kwargs):
    for placeholder in QuestionPlaceholder.objects.filter(question__event=other):
        rules = list(placeholder.rules.all())
        placeholder.pk = None
        placeholder.question = question_map[placeholder.question_id]
        placeholder.save()

        for rule in rules:
            rule.pk = None
            rule.placeholder = placeholder
            rule.save()


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
