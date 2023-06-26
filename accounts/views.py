from rest_framework.decorators import api_view
from rest_framework.response import Response 


@api_view(['POST',])
def user_registration(request):
    return Response({"message": 'Hello World'})