
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from users.models import User
import io
from rest_framework.parsers import JSONParser


# class UserModel:
#     def __init__(self, username, image):
#         self.username = username
#         self.image = image

# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length = 255)
#     image = serializers.CharField()


class UserSerializer(serializers.Serializer):
   first_name = serializers.CharField(max_length = 255, read_only = True)
   last_name = serializers.CharField(read_only = True)
   image = serializers.ImageField(read_only = True)
   username = serializers.CharField()
   email = serializers.CharField(read_only = True)
   
   def create(self, validated_data):
      return User.objects.create(**validated_data) #распаковываем validated_data который приходит с пост запроса

   def update(self, instance, validated_data):  #instance - ссылок на объект women
      instance.first_name = validated_data.get('first_name', instance.first_name)
      instance.last_name = validated_data.get('last_name', instance.last_name)
      instance.image = validated_data.get('image', instance.image)
      instance.username = validated_data.get('username', instance.username)
      instance.email = validated_data.get('email', instance.email)
      instance.save() #сохранить данные в базе данных
      return instance


      




# def encode():
#     model = UserModel('Dmitrii', 'Karl')
#     model_sr = UserSerializer(model) #словарь
#     print(model_sr.data, type(model_sr.data), sep = '\n') #сериализованный данные
#     json = JSONRenderer().render(model_sr.data) #преобразует объект сериализации в байтовую json среду
#     print(json)        


# def decode():
#     stream = io.BytesIO(b'{"username":"Dmitrii","image":"Karl"}')
#     data = JSONParser().parse(stream)
#     serializers = UserSerializer(data = data) # чтобы получить объект сериализации
#     serializers.is_valid()
#     print(serializers.validated_data) #результат декодирования json строки
    