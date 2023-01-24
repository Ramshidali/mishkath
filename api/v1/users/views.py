from api.v1.dashboard.functions import get_student_batch
from api.v1.dashboard.serializers import SubjectWithTopicSerializers
from api.v1.general.functions import decrypt_message, encrypt_message, generate_serializer_errors, get_otp, \
    get_user_token
from api.v1.users.serializers import *
from django.contrib.auth.models import User, Group
from learn.models import GradeBatch, StudentTopic, Subject, Topic
from main.functions import get_auto_id
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from users.models import OtpRecord, Profile, InterviewStatus


# login
@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def login_with_password(request):
    phone = request.data['phone']
    password = request.data['password']
    customer_instance = None
    
    # print(phone)
    # print(password)

    if User.objects.filter(username=phone).exists():
        user = User.objects.get(username=phone)
        if user.check_password(password) :
            # print("hi")
            customer_instance = OtpRecord.objects.get(phone=phone)
            
            response = get_user_token(
                request, customer_instance.phone, decrypt_message(customer_instance.password))
            
            response_data = {
                "StatusCode": 6000,
                "token": response.json(),
                "message": "Login Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        else:
            response_data = {
            "StatusCode": 6001,
            "message": "Password not match"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Username invalid"
        }
        return Response(response_data, status=status.HTTP_200_OK)


# signup
@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def student_details(request):
    response_data = {}

    try:
        phone = request.data['phone']

        serialized = StudentDetailsSerializers(data=request.data)
        instances = TemporaryProfile.objects.filter(phone=phone)

        if not User.objects.filter(username=phone).exists():

            if instances.exists():

                serialized = StudentDetailsSerializers(
                    instances, many=True,
                    context={"request": request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "data": serialized.data,
                    "phone": phone,
                }

            else:

                if serialized.is_valid():
                    name = serialized.validated_data['name']
                    dob = serialized.validated_data['dob']
                    gender = serialized.validated_data['gender']
                    email = serialized.validated_data['email']

                    if name and dob and gender and email:

                        serialized.save(phone=phone)

                        response_data = {
                            "StatusCode": 6000,
                            "message": "Student Details Successfully Saved",
                            "phone": phone,
                        }

                    else:
                        message = "required field"

                        response_data = {
                            "StatusCode": 6001,
                            "message": message,
                        }
                else:
                    message = generate_serializer_errors(serialized.errors)

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }

        else:
            message = "phone number already registered"

            response_data = {
                "StatusCode": 6001,
                "message": message,
            }

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e),
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def personal_details(request):
    response_data = {}

    try:
        phone = request.data['phone']

        serialized = PersonalDetailsSerializers(data=request.data)
        QuerySet = TemporaryProfile.objects.filter(phone=phone, nationality=None, country_of_residense=None,
                                                   permanent_address=None, current_address=None)
        instance = TemporaryProfile.objects.filter(phone=phone)

        if QuerySet.exists():
            if serialized.is_valid():
                nationality = serialized.validated_data['nationality']
                country_of_residense = serialized.validated_data['country_of_residense']
                permanent_address = serialized.validated_data['permanent_address']
                current_address = serialized.validated_data['current_address']

                if nationality and country_of_residense and permanent_address and current_address:
                    TemporaryProfile.objects.filter(phone=phone).update(
                        nationality=nationality, country_of_residense=country_of_residense,
                        permanent_address=permanent_address, current_address=current_address,
                    )

                    response_data = {
                        "StatusCode": 6000,
                        "message": "successfull",
                        "phone": phone,
                    }

                else:
                    message = "field is required"

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }
            else:

                message = generate_serializer_errors(serialized.errors)

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }
        else:
            if not instance.exists():

                message = "phone number not exist"

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }

            else:
                serialized = PersonalDetailsSerializers(
                    instance, many=True,
                    context={"request": request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "data": serialized.data,
                    "phone": phone,
                }

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def parents_details(request):
    response_data = {}

    try:
        phone = request.data['phone']

        serialized = ParentsDetailsSerializers(data=request.data)
        QuerySet = TemporaryProfile.objects.filter(phone=phone, fathers_name=None, fathers_phone=None,
                                                   mothers_name=None, mothers_phone=None)
        instance = TemporaryProfile.objects.filter(phone=phone)

        if QuerySet.exists():
            if serialized.is_valid():
                fathers_name = serialized.validated_data['fathers_name']
                fathers_phone = serialized.validated_data['fathers_phone']
                mothers_name = serialized.validated_data['mothers_name']
                mothers_phone = serialized.validated_data['mothers_phone']

                if fathers_name and fathers_phone and mothers_name and mothers_phone:
                    TemporaryProfile.objects.filter(phone=phone).update(
                        fathers_name=fathers_name,
                        fathers_phone=fathers_phone,
                        mothers_name=mothers_name,
                        mothers_phone=mothers_phone,
                    )

                    response_data = {
                        "StatusCode": 6000,
                        "message": "successfull",
                        "phone": phone,
                    }

                else:
                    message = "field is required"

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }

            else:

                message = generate_serializer_errors(serialized.errors)

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }
        else:
            if not instance.exists():

                message = "phone number not exist"

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }

            else:
                serialized = ParentsDetailsSerializers(
                    instance, many=True,
                    context={"request": request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "data": serialized.data,
                    "phone": phone,
                }


    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def about_mishkath(request):
    response_data = {}

    try:
        phone = request.data['phone']

        serialized = AboutMishkathSerializers(data=request.data)
        QuerySet = TemporaryProfile.objects.filter(phone=phone, mishkath_ad=None, mishkath_ad_message=None)
        instance = TemporaryProfile.objects.filter(phone=phone)

        if QuerySet.exists():
            if serialized.is_valid():
                mishkath_ad = serialized.validated_data['mishkath_ad']
                mishkath_ad_message = request.data['mishkath_ad_message']

                if mishkath_ad:
                    TemporaryProfile.objects.filter(phone=phone).update(
                        mishkath_ad=mishkath_ad,
                        mishkath_ad_message=mishkath_ad_message,
                    )

                    response_data = {
                        "StatusCode": 6000,
                        "message": "successfull",
                        "phone": phone,
                    }

                else:
                    message = "field is required"

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }

            else:

                message = generate_serializer_errors(serialized.errors)

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }
        else:
            if not instance.exists():

                message = "phone number not exist"

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }

            else:
                serialized = AboutMishkathSerializers(
                    instance, many=True,
                    context={"request": request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "data": serialized.data,
                    "phone": phone,
                }

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def course_details(request):
    response_data = {}

    try:
        phone = request.data['phone']

        serialized = CourseDetailsSerializers(data=request.data)
        QuerySet = TemporaryProfile.objects.filter(phone=phone, interested_course=None, prefered_medium=None)
        instance = TemporaryProfile.objects.filter(phone=phone)

        if QuerySet.exists():
            if serialized.is_valid():
                interested_course = serialized.validated_data['interested_course']
                prefered_medium = serialized.validated_data['prefered_medium']

                if interested_course and prefered_medium:
                    TemporaryProfile.objects.filter(phone=phone).update(
                        interested_course=interested_course,
                        prefered_medium=prefered_medium,
                    )

                    response_data = {
                        "StatusCode": 6000,
                        "message": "successfull",
                        "phone": phone,
                    }

                else:
                    message = "field is required"

                    response_data = {
                        "StatusCode": 6001,
                        "message": message,
                    }

            else:

                message = generate_serializer_errors(serialized.errors)

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }
        else:
            if not instance.exists():

                message = "phone number not exist"

                response_data = {
                    "StatusCode": 6001,
                    "message": message,
                }

            else:
                serialized = CourseDetailsSerializers(
                    instance, many=True,
                    context={"request": request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "data": serialized.data,
                    "phone": phone,
                }

    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "message": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def sign_up(request):
    response_data = {}

    try:
        phone = request.data['phone']
        password = request.data['password']

        from_temp_profile = TemporaryProfile.objects.get(phone=phone)

        name = from_temp_profile.name
        dob = from_temp_profile.dob
        gender = from_temp_profile.gender
        email = from_temp_profile.email
        nationality = from_temp_profile.nationality
        country_of_residense = from_temp_profile.country_of_residense
        permanent_address = from_temp_profile.permanent_address
        current_address = from_temp_profile.current_address
        fathers_name = from_temp_profile.fathers_name
        fathers_phone = from_temp_profile.fathers_phone
        mothers_name = from_temp_profile.mothers_name
        mothers_phone = from_temp_profile.mothers_phone
        mishkath_ad = from_temp_profile.mishkath_ad
        mishkath_ad_message = from_temp_profile.mishkath_ad_message
        interested_course = from_temp_profile.interested_course
        prefered_medium = from_temp_profile.prefered_medium

        if phone:

            if OtpRecord.objects.filter(phone=phone).exists():
                OtpRecord.objects.filter(phone=phone).update(password=encrypt_message(password))

            else:
                response_data = {
                    "StatusCode": 6001,
                    "message": "User Not Found"
                }

            if not User.objects.filter(username=phone).exists():

                # for password only
                password_from_otp_model = OtpRecord.objects.get(phone=phone)
                password = decrypt_message(password_from_otp_model.password)
                print ("password ====== ", password)
                otp = get_otp()

                data = User.objects.create_user(
                    username=phone,
                    password=password,
                    is_active=True,
                )

                # adding user groups to determine which role is user has
                if Group.objects.filter(name="student_user").exists():
                    group = Group.objects.get(name="student_user")

                else:
                    group = Group.objects.create(name="student_user")

                data.groups.add(group)

                auto_id = get_auto_id(Profile)

                profile_data = Profile.objects.create(
                    auto_id=auto_id,
                    user=data,
                    creator=data,
                    updater=data,

                    phone=phone,
                    name=name,
                    dob=dob,
                    gender=gender,
                    email=email,
                    nationality=nationality,
                    country_of_residense=country_of_residense,
                    permanent_address=permanent_address,
                    current_address=current_address,
                    fathers_name=fathers_name,
                    fathers_phone=fathers_phone,
                    mothers_name=mothers_name,
                    mothers_phone=mothers_phone,
                    mishkath_ad=mishkath_ad,
                    mishkath_ad_message=mishkath_ad_message,
                    interested_course=interested_course,
                    prefered_medium=prefered_medium,
                )

                TemporaryProfile.objects.filter(phone=phone).delete()

                # for saving interview status

                InterviewStatus.objects.create(
                    auto_id=auto_id,
                    creator=data,
                    updater=data,

                    profile=profile_data,
                    status="pending",

                )

                customer_instance = OtpRecord.objects.get(phone=phone)

                response = get_user_token(
                    request, customer_instance.phone, decrypt_message(customer_instance.password))

                response_data = {
                    "StatusCode": 6000,
                    "token": response.json(),
                    "message": "User Created Sucessfully",
                }

            else:
                messages = "phone number already registered"

                response_data = {
                    "StatusCode": 6001,
                    "message": messages,
                }
        else:
            messages = "please enter phone number"

            response_data = {
                "StatusCode": 6001,
                "message": messages,
            }


    except Exception as e:

        response_data = {
            "StatusCode": 6001,
            "message": str(e),
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def otp_generation(request):
    otp = get_otp()
    phone = request.data['phone']
    
    print("hai its ok!")

    response_data = {}

    data = {}
    if not Profile.objects.filter(phone=phone).exists():
        if OtpRecord.objects.filter(phone=phone).exists():
            messege = str(otp)
            OtpRecord.objects.filter(phone=phone).update(otp=otp)

            data = {
                "phone": phone,
                "otp": messege,
            }

            response_data = {
                "StatusCode": 6000,
                "data": data,
            }

        else:
            OtpRecord.objects.create(
                phone=phone,
                otp=otp,
            )

            data = {
                "phone": phone,
                "otp": otp,
            }

            response_data = {
                "StatusCode": 6000,
                "data": data,
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message" : "phone number already existed,please log in"
        }

    return Response(response_data, status=status.HTTP_200_OK)


# its using for generate otp without checking exicted user from profile
# its mainly using at forgt password section
@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def non_check_otp_generation(request):
    otp = get_otp()
    phone = request.data['phone']

    response_data = {}

    data = {}
    if OtpRecord.objects.filter(phone=phone).exists():
        messege = str(otp)
        OtpRecord.objects.filter(phone=phone).update(otp=otp)

        data = {
            "phone": phone,
            "otp": messege,
        }

        response_data = {
            "StatusCode": 6000,
            "data": data,
        }

    else:
        OtpRecord.objects.create(
            phone=phone,
            otp=otp,
        )

        data = {
            "phone": phone,
            "otp": otp,
        }

        response_data = {
            "StatusCode": 6000,
            "data": data,
        }

    return Response(response_data, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def otp_verify(request):
    response_data = {}

    data = request.data
    phone = data['phone']
    is_new = None

    data = {}

    serialized = OtpGenerationSerializer(data=request.data)
    otp = serialized.verify_otp(request.data)

    if otp == True:
        # for getting username and password for generate token
        otp_record = OtpRecord.objects.get(phone=phone)

        if User.objects.filter(username=phone).exists():

            is_new = False
            # get the values of username and password
            username = phone
            password = decrypt_message(otp_record.password)

            # function for getting user token imported from general.functions
            user_token = get_user_token(request, username, password)

            response_data = {
                "StatusCode": 6000,
                "token": user_token.json(),
                "is_new": is_new,
                "message": "OTP verified"
            }
        else:
            is_new = True

            data = {
                "phone": phone,
                "otp": otp,
            }

            response_data = {
                "StatusCode": 6000,
                "is_new": is_new,
                "data": data,
                "message": "OTP Verified"
            }

    else:

        response_data = {
            "StatusCode": 6001,
            "message": "OTP invalid or timeout"
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def forget_password(request):
    phone = request.data['phone']
    password = request.data['password']
    # c_password = request.data['c_password']

    if User.objects.filter(username=phone).exists():
        if password:
            user = User.objects.get(username=phone)
            user.set_password(password)
            user.save()
            # User.objects.filter(username=phone).update(password=password)
            OtpRecord.objects.filter(phone=phone).update(password=encrypt_message(password))

            response_data = {

                "StatusCode": 6000,
                "message": "Password changed successfull"

            }

            return Response(response_data, status=status.HTTP_200_OK)

        else:

            response_data = {

                "StatusCode": 6000,
                "message": "Enter password"

            }

            return Response(response_data, status=status.HTTP_200_OK)

    else:

        response_data = {

            "StatusCode": 6000,
            "message": "please signup"
        }

        return Response(response_data, status=status.HTTP_200_OK)


# user data getting from profile
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def profile(request):
    instances = Profile.objects.get(user=request.user,is_deleted=False)

    serialized = ProfileSerializer(instances, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def courses_percentage(request):
    
    total_count_of_topic = Topic.objects.filter(is_deleted=False).count()
    count_student_entrolled_topics = StudentTopic.objects.filter(student_id__user=request.user,is_deleted=False).count()
    percentage_of_all_topics = str(float(count_student_entrolled_topics)/float(total_count_of_topic)*100)

    response_data = {
        "StatusCode" : 6000,
        "percentage_of_course" :percentage_of_all_topics,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def courses__in_progress(request):
    batch = get_student_batch(request)
        
    if GradeBatch.objects.filter(batch__pk=batch).exists():
        grade_from_batch = GradeBatch.objects.get(batch__pk=batch)
        instance = Subject.objects.filter(grade=grade_from_batch.grade,is_deleted=False)
        
        serialized = SubjectWithTopicSerializers(
            instance, many=True,
            context={"request": request}
            )
        
        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
            "grade": grade_from_batch.grade.name,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
