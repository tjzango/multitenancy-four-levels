from django.shortcuts import render
from rest_framework import viewsets
from tenants.utils import tenant_from_request
from pools.models import Pool
from pools.serializer import PoolSerializer
#  Create your views here


class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer

    def get_queryset(self):
        tenant = tenant_from_request(self.request)
        return super().get_queryset().filter(tenant=tenant)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Pool


def pools_list(request):
    MAX_OBJECTS = 20
    pools = Pool.objects.all()[:20]
    data = {
        "results": list(
            pools.values("pk", "question", "created_by__username", "pub_date")
        )
    }
    return JsonResponse(data)


def pools_detail(request, pk):
    pool = get_object_or_404(Pool, pk=pk)
    data = {
        "results": {
            "question": pool.question,
            "created_by": pool.created_by.username,
            "pub_date": pool.pub_date,
        }
    }
    return JsonResponse(data)
