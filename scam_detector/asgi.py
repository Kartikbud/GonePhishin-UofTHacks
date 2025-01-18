"""
File: asgi.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: May 15, 2023
Version: 1.0.0

This file contains the configurations for the ASGI (Asynchronous Server Gateway Interface)
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from detector.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scam_detector.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
