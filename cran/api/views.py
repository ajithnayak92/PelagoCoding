from django.shortcuts import render

from django.http.response import JsonResponse, HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the repo index.")


def detail(request, package_name):
    return HttpResponse("You're looking at package %s." % package_name)


def search(request, query_term):
    response = "You're looking at the results of package %s."
    return HttpResponse(response % query_term)


def download(request, package_name):
    return HttpResponse("You're downloading package %s with version xx." % package_name)
