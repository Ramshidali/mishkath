from rest_framework.response import Response
from rest_framework import status



def return_with_status_code(response_data):

    if response_data['StatusCode'] == 6000:
        return Response(response_data,status=status.HTTP_200_OK)
    elif response_data['StatusCode'] == 6001:
        return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
    elif response_data['StatusCode'] == 6002:
        return Response(response_data,status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(response_data,status=status.HTTP_202_ACCEPTED)