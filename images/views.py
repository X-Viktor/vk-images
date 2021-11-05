from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from images.models import Image
from images.serializer import ImageSerializer

from images.services.image import (
    get_image_hashing, get_image_dimensions, scale_image)


class ImageAPIView(APIView):
    serializer_class = ImageSerializer


class GetImageAPIView(ImageAPIView):
    def get(self, request, *args, **kwargs):
        data = request.GET

        # Получаем id изображения из запроса
        image_id = data.get('id')

        if image_id:
            try:
                # Получаем изображение с базы по id
                image = get_object_or_404(Image, id=image_id)
            # Если изображение не найдено в базе
            except Http404:
                return Response({
                    'message': 'Изображение не найдено.',
                }, status=404)
            # Если id указан неверно
            except ValidationError:
                return Response({
                    'message': 'Неверно указан идентификатор.',
                }, status=400)

            if data.get('scale'):
                image = scale_image(image.image, float(data['scale']))
            else:
                image = image.image

            return HttpResponse(image, content_type="image/png")
        # Если id не указан в запросе
        else:
            return Response({
                'message': 'Идентификатор изображения не указан.',
            }, status=400)


class UploadImageAPIView(ImageAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        # Указано ли изображение
        if serializer.is_valid():
            uploaded_image = request.data['image']
            # Получаем hash изображения
            image_hash = get_image_hashing(uploaded_image)
            # Получаем размеры изображения
            image_dimensions = get_image_dimensions(uploaded_image)
            # Высчитываем пропорции изображения
            image_proportion = image_dimensions[0] / image_dimensions[1]

            # Ищем изображение в базе
            image = Image.objects.filter(
                hash=image_hash, proportions=image_proportion)
            # Если изображение не найдено, сохраняем в базу
            if not image.exists():
                image = Image.objects.create(
                    hash=image_hash, image=uploaded_image,
                    proportions=image_proportion)
                return Response({
                    'message': 'Изображение было успешно загружено.',
                    'id': image.id,
                }, status=200)
            # Если hash изображения с похожими пропорциями уже есть в базе
            else:
                image = image.first()
                # Если размеры изображения больше тех, что есть в базе
                if image_dimensions[0] > image.image.width:
                    image.image = uploaded_image
                    image.hash = image_hash
                    image.proportions = image_proportion
                    image.save()
                    return Response({
                        'message': 'Изображение было успешно обновлено.',
                        'id': image.id,
                    }, status=200)
                else:
                    return Response({
                        'message': 'Похожее изображение уже есть в базе.',
                        'id': image.id,
                    }, status=200)
        # Если изображение не указано в запросе
        else:
            return Response({
                'message': 'Изображение не указано.',
            }, status=400)
