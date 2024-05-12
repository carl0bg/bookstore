from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class PostViews(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer