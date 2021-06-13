from django import forms

from api.models import Package


class PackageUploadForm(forms.ModelForm):
    # tarball = forms.FileField()
    class Meta:
        model = Package
        fields = ('package', )
