from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _

from pretix.base.signals import logentry_display


@receiver(signal=logentry_display, dispatch_uid="log_read_access_logdisplay")
def cert_logentry_display(sender, logentry, **kwargs):
    if not logentry.action_type.startswith('pretix_log_read_access'):
        return

    plains = {
        'pretix_log_read_access.export': _('Export performed: {settings}.').format(settings=logentry.data),
        'pretix_log_read_access.order.read': _('Order details viewed.'),
    }

    if logentry.action_type in plains:
        return plains[logentry.action_type]
