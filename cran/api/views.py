import mimetypes
import os

from django.shortcuts import render, redirect

from django.http.response import JsonResponse, HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
from api.models import Package
from api.forms import PackageUploadForm


def index(request):
    return HttpResponse("Hello, world. You're at the repo index.")


def detail(request, package_name):
    try:
        package = Package.objects.get(package_name=package_name)
    except Package.DoesNotExist:
        raise Http404("The package you're looking for does not exist")
    # return render(request, 'polls/detail.html', {'package': package_name})
    return HttpResponse("You're looking at package %s." % package)


def search(request, query_term):
    response = "You're looking at the results of package %s."
    return HttpResponse(response % query_term)


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


def process_tarball(package_file):
    pass


def upload_package(request):
    if request.method == 'POST':
        form = PackageUploadForm(request.POST, request.FILES)
        # print("File data : "+form.fields['package'])
        if form.is_valid():

            x = form.save()
            process_tarball(x.package)
            # return redirect('index')
            return HttpResponse("Thank you yor package is saved")
    else:
        form = PackageUploadForm()
    return render(request, 'model_form_upload.html', {
        'form': form})
