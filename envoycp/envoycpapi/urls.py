from django.urls import include, path

from rest_framework import routers

from envoycpapi.views import *

router = routers.DefaultRouter()

urlpatterns = [
   path('', include(router.urls)),
   path('discovery:endpoints', endpoint_discovery, name='endpoint_discovery'),
   path('discovery:clusters', cluster_discovery, name='cluster_discovery'),
   path('discovery:listeners', listener_discovery, name='listener_discovery'),
   path('increment_eds_version', increment_eds_version, name='increment_eds_version'),
   path('increment_cds_version', increment_cds_version, name='increment_cds_version'),
   path('increment_lds_version', increment_lds_version, name='increment_lds_version'),
   path('start_envoy', start_envoy, name='start_envoy'),
   path('stop_envoy', stop_envoy, name='stop_envoy'),
]