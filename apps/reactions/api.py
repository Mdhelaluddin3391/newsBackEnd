from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Reaction
from .serializers import ReactionSerializer

class ToggleReactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Agar reaction pehle se hai toh delete (Unlike), nahi toh create (Like)
        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            article=serializer.validated_data["article"],
            type=serializer.validated_data["type"],
        )

        if not created:
            reaction.delete()
            return Response({"detail": f"{reaction.type} removed"}, status=status.HTTP_200_OK)

        return Response({"detail": f"{reaction.type} added"}, status=status.HTTP_201_CREATED)