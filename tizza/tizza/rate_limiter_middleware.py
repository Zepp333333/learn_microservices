import datetime

from django.http import HttpResponse


class RateLimit:
    def __init__(self, get_response):
        self.get_response = get_response
        from .settings import RATE_LIMIT
        self.time_period = datetime.timedelta(seconds=RATE_LIMIT['time_period'])
        self.hits_per_period = RATE_LIMIT['hits_per_period']
        self.ip_adresses: dict[str, list[datetime, int]] = {}

    def process_view(self, request, *args, **kwargs):
        ip = self.get_client_ip(request)
        if not self.is_within_limit(ip):
            print('Limit exceeded', self.ip_adresses)
            return HttpResponse({'Rate Limit exceeded for your IP'})
        print('Limit not exceeded', self.ip_adresses)
        response = self.get_response(request)
        return response


    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_within_limit(self, ip):
        if ip not in self.ip_adresses:
            self.reset_limit(ip)
            return True

        window_start, hits = self.ip_adresses[ip]
        if datetime.datetime.now() - window_start >= self.time_period:
            self.reset_limit(ip)
            return True
        elif hits < self.hits_per_period:
            self.ip_adresses[ip][1] += 1
            return True
        return False

    def reset_limit(self, ip):
        self.ip_adresses[ip] = [datetime.datetime.now(), 1]
