from django.shortcuts import render


def index_store(request):
    return render(request, 'index.html')
