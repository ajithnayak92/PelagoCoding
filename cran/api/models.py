# import the standard Django Model
from django.db import models
from datetime import datetime

import tarfile


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    package_name = models.CharField(max_length=100, primary_key=True)
    version = models.CharField(max_length=10)
    authors = models.ForeignKey(Author, on_delete=models.DO_NOTHING, null=True, related_name='author')
    maintainers = models.ForeignKey(Author, on_delete=models.DO_NOTHING, null=True, related_name='maintainer')
    date_or_publication = models.DateTimeField(null=True)
    package = models.FileField(upload_to='package_files', null=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Override the base class implementation to populate the remaining of package details"""
        content = self.get_desc_string()
        desc_values = convert_desc_to_dict(content=content.decode("utf-8"))
        self.populate_package_from_desc_dict(desc_values)
        self.save_base(force_insert, force_update, using,
                       update_fields)

    def get_desc_string(self):
        tar_temp_path = self.package._file.file.name
        tar = tarfile.open(tar_temp_path, "r:gz")
        desc = tar.getmember('ShapeChange/DESCRIPTION')
        extracted = tar.extractfile(desc)
        content = extracted.read()
        return content

    def populate_package_from_desc_dict(self, desc_values):
        self.title = desc_values.get('Title', "")
        self.description = desc_values.get('Description', '')
        self.package_name = desc_values.get('Package', '')
        self.version = desc_values.get('Version', '')
        # for author in desc_values.get('Author').split(' and '):
        #     auth = Author.objects.get(
        #         name=author
        #     )
        #     self.authors = auth
        # for author in desc_values.get('Maintainer').split(' and '):
        #     author_name = author.split(' <')[0].strip()
        #     author_email = author(' <')[0].replace('>').strip()
        #     auth = Author.objects.get(
        #         name=author_name,
        #         email=author_email
        #     )
        #     self.maintainers = auth
        try:
            self.date_or_publication = datetime.strptime(desc_values.get('Date/Publication', ''), '%Y-%m-%d %H:%M:%S')
        except:
            self.date_or_publication = datetime.now()

    def __str__(self):
        return self.title


def convert_desc_to_dict(content):
    content_dict = {}
    splits = [line.split(':', 1) for line in str(content).split('\n')]
    for split in splits:
        if len(split) > 1:
            content_dict[split[0]] = split[1].strip()
    return content_dict
