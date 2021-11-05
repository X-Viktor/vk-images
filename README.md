# VK Images

### Адрес сервера
https://vk-images.herokuapp.com/

| Метод | Параметры |
| :------------- | :-----|
| GET `/api/get/` | `id` - идентификатор изображения |
| POST `/api/upload/` | `file` - файл изображения |

### Скрипт для тестирования
Запуск скрипта
```shell
$ python tests/test.py
```
Параметры для запуска (необязательные)
```shell
-u | --url - Адрес сервера
-p | --port - Порт сервера
```

### Запуск приложения
```shell
$ docker-compose up
```
