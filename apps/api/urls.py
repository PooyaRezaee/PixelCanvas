from django.urls import path, include


urlpatterns = [
    path("account/", include(("apps.account.urls", "account"))),
    path("canvas/", include(("apps.canvas.urls", "canvas"))),
]
