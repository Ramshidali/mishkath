from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.v1.general.serializers import CountrySerializers, CoursesSerializers

from main.models import Country, Courses



@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def contry_code(request):
    instances = Country.objects.filter(is_deleted=False)

    serialized = CountrySerializers(instances, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def courses(request):
    instances = Courses.objects.filter(is_deleted=False)

    serialized = CoursesSerializers(instances, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)