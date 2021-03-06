from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:package_name>', views.detail, name='detail'),
    path('search/<str:query_term>', views.search, name='search'),
    path('download/<str:package_name>', views.download, name='download'),
    path('upload/<str:package_name>', views.upload, name='upload'),
    path('handle', views.upload_package, name='upload_file'),
    path('new_search', views.PackageListView.as_view(), name='upload_file'),
]
