"""yourstudypath URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(('accounts.api.urls', 'api-auth'), namespace='api-auth')),
    path('api/exam/', include(('core.api.urls', 'api-core'), namespace='api-core')),
    path('api/analytics/', include(('analytics.api.urls', 'api-analytics'), namespace='api-analytics')),
    path('api/courses/', include(('courses.api.urls', 'api-courses'), namespace='api-courses')),
]

# authentication urls
urlpatterns += [
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include(('accounts.urls', 'account-url'), namespace='account-url')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)