from django.shortcuts import render


def index_store(request):
    render(request, 'index.html')
