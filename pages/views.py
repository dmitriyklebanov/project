from django.shortcuts import render

from django.conf import settings

tracing = settings.OPENTRACING_TRACING

@tracing.trace()
def about(request):
    return render(request, 'pages/about.html')