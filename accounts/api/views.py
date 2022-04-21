from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import Profile
from yourstudypath.restconf.permissions import AnonPermissionOnly, IsOwnerOrReadOnly
from accounts.api.serializers import UserRegisterSerializer, ProfileSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
    

# Because profile was created on user registration RUD(Read Update Delete APIView)
class ProfileRUDAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = ProfileSerializer
    lookup_field = 'slug'

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def perform_update(self, serializer):
        owner: Profile = Profile.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user.username is not owner.user.username:
            return Response({"detail": "Must be owner"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()

    def perform_destroy(self, instance):
        owner: Profile = Profile.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user.username is not owner.user.username:
            return Response({"detail": "Must be owner"}, status=status.HTTP_401_UNAUTHORIZED)
        super().perform_destroy(instance)