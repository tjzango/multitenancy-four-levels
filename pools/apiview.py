from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth import authenticate

from .models import Pool, Choice
from .serializer import (
    PoolSerializer,
    ChoiceSerializer,
    VoteSerializer,
    UserSerializer,
)
from tenants.utils import tenant_from_request


class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer

    def get_queryset(self):
        tenant = tenant_from_request(self.request)
        return super().get_queryset().filter(tenant=tenant)

    def destroy(self, request, *args, **kwargs):
        pool = Pool.objects.get(pk=self.kwargs["pk"])
        if not request.user == pool.created_by:
            raise PermissionDenied("You can not delete this pool.")
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(pool_id=self.kwargs["pk"])
        return queryset

    def post(self, request, *args, **kwargs):
        pool = Pool.objects.get(pk=self.kwargs["pk"])
        if not request.user == pool.created_by:
            raise PermissionDenied("You can not create choice for this pool.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {"choice": choice_pk, "pool": pk, "voted_by": voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
