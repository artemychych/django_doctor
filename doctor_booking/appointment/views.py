from pydoc import doc
from unicodedata import category
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets
from .models import *
from .serializers import GroupSerializer, UserSerializer
from django.conf import settings
from django.urls import reverse

# Create your views here.

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.all()
    categories_json = []
    
    for category in categories:
        icon_url = request.build_absolute_uri(category.icon.url)
        
        categories_json.append({
            'id': category.id, # type: ignore
            'name': category.name,
            'icon': icon_url
        })
    return Response({"categories": categories_json})

@api_view(['GET'])
def getCategoryById(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    icon_url = request.build_absolute_uri(category.icon.url)
    return Response(
        {
            'id': category.id, # type: ignore
            'name': category.name,
            'icon': icon_url
        }
    )
    
@api_view(['GET'])
def getSliders(request):
    sliders = Slider.objects.all()
    sliders_json = []
    for slider in sliders:
        image_url = request.build_absolute_uri(slider.image.url)
        sliders_json.append({
            'id': slider.id, # type: ignore
            'name': slider.name,
            'image': image_url
        })
    return Response({"sliders": sliders_json})

@api_view(['GET'])
def getSliderById(request, slider_id):
    slider = get_object_or_404(Slider, id=slider_id)
    image_url = request.build_absolute_uri(slider.image.url)
    return Response(
        {
            'id': slider.id, # type: ignore
            'name': slider.name,
            'image': image_url
        }
    )
    
@api_view(['GET'])
def getHospitals(request):
    hospitals = Hospital.objects.all()
    hospitals_json = []
    for hospital in hospitals:
        categories = hospital.categories.all()  # Получаем все связанные категории
        hospital_data = {
            'id': hospital.id, # type: ignore
            'name': hospital.name,
            'address': hospital.address,
            'image': request.build_absolute_uri(hospital.image.url),
            'email': hospital.email,
            'phone': hospital.phone,
            'website': hospital.website,
            'description': hospital.description,
            'opening_hours': hospital.opening_hours,
            'categories': [{'id': category.id, 'name': category.name, 'icon': request.build_absolute_uri(category.icon.url)} for category in categories]
        }
        hospitals_json.append(hospital_data)
        
    return Response({"hospitals": hospitals_json})

@api_view(['GET'])
def getHospitalById(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    image_url = request.build_absolute_uri(hospital.image.url)
    categories = hospital.categories.all()
    return Response(
        {
            'id': hospital.id, # type: ignore
            'name': hospital.name,
            'address': hospital.address,
            'image': request.build_absolute_uri(hospital.image.url),
            'email': hospital.email,
            'phone': hospital.phone,
            'website': hospital.website,
            'description': hospital.description,
            'opening_hours': hospital.opening_hours,
            'categories': [{'id': category.id, 'name': category.name, 'icon': request.build_absolute_uri(category.icon.url)} for category in categories]
        }
    )
    
@api_view(['GET'])
def getDoctors(request):
    doctors = Doctor.objects.all()
    doctors_json = []
    for doctor in doctors:
        image_url = request.build_absolute_uri(doctor.image.url)
        doctors_json.append({
            'id': doctor.id, # type: ignore
            'name': doctor.name,
            'image': image_url,
            'address': doctor.address,
            'experience': doctor.experience,
            'phone': doctor.phone,
            'email': doctor.email,
            'category': {
                'id': doctor.category.id, # type: ignore
                'name': doctor.category.name,  # type: ignore
                'icon': request.build_absolute_uri(doctor.category.icon.url) # type: ignore
            },
            'hospital': {
                'id': doctor.hospital.id, # type: ignore
                'name': doctor.hospital.name
            }
            
        })    
    return Response({"doctors": doctors_json})

@api_view(['GET'])
def getDoctorById(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    image_url = request.build_absolute_uri(doctor.image.url)
    return Response({'id': doctor.id, # type: ignore
            'name': doctor.name,
            'image': image_url,
            'address': doctor.address,
            'experience': doctor.experience,
            'phone': doctor.phone,
            'email': doctor.email,
            'category': {
                'id': doctor.category.id, # type: ignore
                'name': doctor.category.name,  # type: ignore
                'icon': request.build_absolute_uri(doctor.category.icon.url) # type: ignore
            },
            'hospital': {
                'id': doctor.hospital.id, # type: ignore
                'name': doctor.hospital.name
            }})
    
@api_view(['GET'])
def getHospitalDoctors(request, hospital_id):
    try:
        # Проверка, существует ли госпиталь с данным id
        hospital = Hospital.objects.get(id=hospital_id)
        
        # Фильтрация докторов по hospital_id
        doctors = Doctor.objects.filter(hospital=hospital)
        
        # Формируем список с информацией о докторах
        doctors_json = []
        for doctor in doctors:
            doctors_json.append({
                'id': doctor.id, # type: ignore
                'name': doctor.name,
                'address': doctor.address,
                'experience': doctor.experience,
                'about': doctor.about,
                'phone': doctor.phone,
                'image': doctor.image.url if doctor.image else None,
                'email': doctor.email,
                'category': {
                    'id': doctor.category.id, # type: ignore
                    'name': doctor.category.name,  # type: ignore
                    'icon': request.build_absolute_uri(doctor.category.icon.url) # type: ignore
                },
                'hospital': {
                    'id': doctor.hospital.id, # type: ignore
                    'name': doctor.hospital.name
                }
            })
        
        return Response({"doctors": doctors_json})
    
    except Hospital.DoesNotExist:
        return Response({"error": "Hospital not found"}, status=404)



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createAppointment(request):
    data = request.data
    
    # Получаем необходимые данные из запроса
    user_id = data.get("userId")
    hospital_id = data.get("hospitalId")
    doctor_id = data.get("doctorId")
    visit_date = data.get("visitDate")
    time = data.get("time")
    note = data.get("note")

    try:
        # Получаем объекты User, Hospital и Doctor по их id
        user = User.objects.get(id=user_id)
        hospital = Hospital.objects.get(id=hospital_id)
        doctor = Doctor.objects.get(id=doctor_id)

        # Создаем новый объект Appointment
        appointment = Appointment.objects.create(
            user=user,
            visit_date=visit_date,
            time=time,
            hospital=hospital,
            doctor=doctor,
            note=note
        )

        # Возвращаем ответ с информацией о созданной записи
        return Response({
            "message": "Appointment created successfully",
            "appointment": {
                "id": appointment.id, # type: ignore
                "user": appointment.user.first_name,
                "doctor": appointment.doctor.name,
                "hospital": appointment.hospital.name,
                "visit_date": appointment.visit_date,
                "time": appointment.time,
                "note": appointment.note
            }
        }, status=201)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Hospital.DoesNotExist:
        return Response({"error": "Hospital not found"}, status=404)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserAppointments(request, user_id):
    try:
        # Получаем все записи для данного пользователя
        appointments = Appointment.objects.filter(user_id=user_id)
        
        # Проверка, есть ли записи
        if not appointments.exists():
            return Response({"message": "No appointments found for this user"}, status=404)
        
        # Формируем список из appointment данных
        appointments_list = [
            {
                "id": appointment.id, # type: ignore
                "doctor": appointment.doctor.name,
                "hospital": appointment.hospital.name,
                "visit_date": appointment.visit_date,
                "time": appointment.time,
                "note": appointment.note,
            }
            for appointment in appointments
        ]

        # Возвращаем список всех записей
        return Response({"appointments": appointments_list}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def getDoctorsByCategory(request, category_id):
    try:
        # Получаем всех докторов, относящихся к указанной категории
        doctors = Doctor.objects.filter(category_id=category_id)

        # Проверка, есть ли доктора в этой категории
        if not doctors.exists():
            return Response({"message": "No doctors found for this category"}, status=404)

        # Формируем список из данных о докторах
        doctors_list = [
            {
                "id": doctor.id, # type: ignore
                "name": doctor.name,
                "address": doctor.address,
                "experience": doctor.experience,
                "about": doctor.about,
                "phone": doctor.phone,
                "email": doctor.email,
                "image": str(doctor.image),  # если необходимо, можно добавить полный URL
            }
            for doctor in doctors
        ]

        # Возвращаем список всех докторов
        return Response({"doctors": doctors_list}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)