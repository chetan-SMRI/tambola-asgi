from django.conf.urls import url
from game.consumers import GetLastValues

websocket_urlpatterns = [
    url(r'^getlastvalues/(?P<room_code>\d+)/$', GetLastValues.as_asgi())
]