from django.shortcuts import render
from commodity.models import CommodityInfo


def index_store(request):
    data = CommodityInfo.objects.all()
    return render(request, 'index.html', locals())
