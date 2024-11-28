from django.shortcuts import render
# 'static' non...functional views for non-logged users


def about(request):
    return render(request, 'common/about.html')


def what_we_do(request):
    return render(request, 'common/mission.html')


def contacts(request):
    return render(request, 'common/contact.html')


def index(request):
    return render(request, 'common/index.html')
