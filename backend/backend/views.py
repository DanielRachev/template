from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ReactAppView(TemplateView):
    template_name = "index.html"
