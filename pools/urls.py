from django.urls import path

from pools.apiview import PoolViewSet, ChoiceList, CreateVote, UserCreate, LoginView


from rest_framework.routers import DefaultRouter

from rest_framework.documentation import include_docs_urls




urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("pools/<int:pk>/choices/", ChoiceList.as_view(), name="pools_list"),
    path(
        "pools/<int:pk>/choices/<int:choice_pk>/vote/",
        CreateVote.as_view(),
        name="pools_list",
    ),
]

