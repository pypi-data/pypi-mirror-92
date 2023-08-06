from datetime import timedelta

from django.urls import get_script_prefix, resolve
from django.utils.timezone import now
from django_scopes import scopes_disabled

from pretix.base.models import Order, Invoice, Organizer, Event


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(get_script_prefix() + 'control') and request.user.is_authenticated:
            self._log_control_request(request)

        response = self.get_response(request)

        if request.path.startswith(get_script_prefix() + 'api') and request.user.is_authenticated and hasattr(response, 'data'):
            self._log_api_request(request, response)

        return response

    def _log_control_request(self, request):
        try:
            url = resolve(request.path)
        except:
            return

        if hasattr(request, 'event') and 'code' in url.kwargs:
            try:
                order = request.event.orders.get(code__iexact=url.kwargs.get('code'))
            except Order.DoesNotExist:
                return
            self._log_order(order, request.user)

        if hasattr(request, 'event') and 'invoice' in url.kwargs:
            try:
                order = request.event.invoices.get(pk=url.kwargs.get('invoice')).order
            except Invoice.DoesNotExist:
                return
            self._log_order(order, request.user)

        if url.url_name == 'organizer.export.do' and request.method == "POST":
            self._log_export(request.organizer, request.POST, request.user)

        if url.url_name in ('event.orders.export.do', 'event.shredder.export') and request.method == "POST":
            self._log_export(request.event, request.POST, request.user)
            pass

        # todo: question detail

    @scopes_disabled()
    def _log_api_request(self, request, response):
        try:
            url = resolve(request.path)
        except:
            return

        codes = set()

        if 'order-' in url.url_name:
            if 'results' in response.data:
                codes |= {r['code'] for r in response.data['results']}
            if 'code' in response.data:
                codes.add(response.data['code'])

        if 'orderposition-' in url.url_name or 'checkinlistpos' in url.url_name:
            if 'results' in response.data:
                codes |= {r['order'] for r in response.data['results']}
            if 'order' in response.data:
                codes.add(response.data['order'])

        if codes:
            for order in Order.objects.filter(event__slug=url.kwargs['event'], code__in=codes):
                order.log_action('pretix_log_read_access.order.read', user=request.user, auth=request.auth)

        if 'exporters-run' in url.url_name and request.method == 'POST':
            if 'event' in url.kwargs:
                object = Event.objects.get(
                    slug=url.kwargs['event'],
                    organizer__slug=url.kwargs['organizer'],
                )
            else:
                object = Organizer.objects.get(
                    slug=url.kwargs['organizer'],
                )
            object.log_action('pretix_log_read_access.export', data={
                'exporter': url.kwargs.get('pk'),
                'api': True
            }, user=request.user, auth=request.auth)

        pass

    def _log_order(self, order, user=None, auth=None):
        # Do not log again if the same user access the same record within minutes
        if user:
            if not order.all_logentries().filter(
                action_type='pretix_log_read_access.order.read', user=user,
                datetime__gt=now() - timedelta(minutes=10)
            ).exists():
                order.log_action('pretix_log_read_access.order.read', user=user, auth=auth)
        else:
            order.log_action('pretix_log_read_access.order.read', auth=auth)

    def _log_export(self, object, data, user=None, auth=None):
        data = data.copy()
        data.pop("ajax", None)
        data.pop("csrfmiddlewaretoken", None)
        object.log_action('pretix_log_read_access.export', data=data, user=user, auth=auth)