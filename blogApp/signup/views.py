
from django.db import IntegrityError 
import random
from django.conf import settings
from djoser.compat import get_user_email
from djoser import utils
from django.contrib.sites.models import Site
from djoser.email import ActivationEmail
from django.utils import timezone
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import User
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication  
from .serializers import CustomUserSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from rest_framework import status
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


@authentication_classes([TokenAuthentication])  
@permission_classes([AllowAny])
class CustomUserViewSet(DjoserUserViewSet):
    serializer_class = CustomUserSerializer 
    lookup_field = 'email'
    lookup_url_kwarg = 'email'
    @action(['POST'], detail=False)
    def register_user(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            user = serializer.instance
            user.set_password(request.data['password'])
            user.generate_new_code()
            user.save()

            # Print the generated code to the console (server logs)
            print(f"Generated Code: {user.code}")

            headers = self.get_success_headers(serializer.data)
            return Response({'detail': 'User registered successfully. Code sent for verification.', 'generated_code': user.code}, status=201, headers=headers)
        except IntegrityError as e:
            return Response({'detail': 'Error creating user. IntegrityError: {}'.format(str(e))}, status=500)
        except Exception as e:
            return Response({'detail': 'An unexpected error occurred: {}'.format(str(e))}, status=500)
        
    @action(['POST'], detail=True)
    def verify_code(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            code = request.data.get('code', None)

            if user.is_code_expired():
                return Response({'detail': 'Code has expired.'}, status=400)

            if user.code == code:
                user.is_active = True
                user.code = None
                user.code_expiry = None
                user.save()
                return Response({'detail': 'Code verified successfully.'})

            user.code_attempts += 1
            user.save()

            return Response({'detail': 'Invalid code.'}, status=400)
        except ValidationError as e:
            return Response({'detail': f'Validation error: {str(e)}'}, status=400)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {str(e)}'}, status=500)

    # @action(['POST'], detail=False)
    # def sign_in(self, request, *args, **kwargs):
    #     try:
    #         email = request.data.get('email')
    #         password = request.data.get('password')
    #         user = authenticate(request, email=email, password=password)
            
    #         if user:
    #             # Use the following lines to generate or get an existing token
    #             token, created = Token.objects.get_or_create(user=user)
                
    #             # You can also use the user.auth_token attribute if you have a custom user model
    #             # token = user.auth_token
                
    #             return Response({'detail': 'Sign-in successful.', 'token': token.key})
    #         else:
    #             return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    #     except IntegrityError as e:
    #         return Response({'detail': 'Error signing in. IntegrityError: {}'.format(str(e))}, status=500)
    #     except ValidationError as e:
    #         return Response({'detail': f'Validation error: {str(e)}'}, status=400)
    #     except Exception as e:
    #         return Response({'detail': f'An unexpected error occurred: {str(e)}'}, status=500)
        
    @action(['POST'], detail=False)
    def sign_in(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, email=email, password=password)

            if user:
                # Use the following lines to generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'detail': 'Sign-in successful.', 'access_token': access_token})
            else:
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        except IntegrityError as e:
            return Response({'detail': 'Error signing in. IntegrityError: {}'.format(str(e))}, status=500)
        except ValidationError as e:
            return Response({'detail': f'Validation error: {str(e)}'}, status=400)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {str(e)}'}, status=500)
    