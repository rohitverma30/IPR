from django.utils.deprecation import MiddlewareMixin
from .models import PageView

class TrackPageViewsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.path
        view, created = PageView.objects.get_or_create(url=url)
        view.count += 1
        view.save()
        request.view_count = view.count
