from django.urls import path

from images.views import GetImageAPIView, UploadImageAPIView

urlpatterns = [
    path('get/', GetImageAPIView.as_view(), name='get-image'),
    path('upload/', UploadImageAPIView.as_view(), name='upload-image'),
]
