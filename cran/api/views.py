import mimetypes
import os

from django.shortcuts import render, redirect
from django.views import generic


from django.http.response import JsonResponse, HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
from api.models import Package
from api.forms import PackageUploadForm


def index(request):
    package_list = Package.objects.all()
    return render(request, 'overview.html', {'package_list': package_list})


def detail(request, package_name):
    try:
        package = Package.objects.get(package_name=package_name)
    except Package.DoesNotExist:
        raise Http404("The package you're looking for does not exist")
    # return render(request, 'polls/detail.html', {'package': package_name})
    # return HttpResponse("You're looking at package %s." % package)
    return render(request, 'detail.html', {'package': package})


def search(request, query_term):
    # response = "You're looking at the results of package %s."
    package_list = Package.objects.filter(title__contains=query_term)
    # print ("Returen size "+len(package_list))
    return render(request, 'overview.html', {'package_list': package_list})


def download(request, package_name):
    package = Package.objects.get(package_name=package_name)
    file_path = package.package.path
    mime_type, _ = mimetypes.guess_type(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def upload(request, package_name):
    return HttpResponse("You're uploading package %s with version xx." % package_name)


def upload_package(request):
    if request.method == 'POST':
        form = PackageUploadForm(request.POST, request.FILES)
        # print("File data : "+form.fields['package'])
        if form.is_valid():

            x = form.save()
            # return redirect('index')
            return HttpResponse("Thank you yor package is saved")
    else:
        form = PackageUploadForm()
    return render(request, 'upload.html', {
        'form': form})

class PackageListView(generic.ListView):
    model = Package
    context_object_name = 'package_list'   # your own name for the list as a template variable
    queryset = Package.objects # Get 5 books containing the title war
    template_name = 'overview.html'  # Specify your own template name/location
