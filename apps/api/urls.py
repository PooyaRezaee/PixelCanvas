from django.urls import path, include


urlpatterns = [
    path("account/", include(("apps.account.urls", "account"))),
    path("sample/", include(("apps.sample.urls", "sample"))),
]
