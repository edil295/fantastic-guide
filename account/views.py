from rest_framework.generics import CreateAPIView


from .models import User, Author
from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            Author.objects.create(user=user)