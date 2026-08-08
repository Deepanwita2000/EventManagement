
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from django.utils import timezone
from datetime import timedelta

from accountapp.authentication import JWTAuthentication, create_access_token, create_refresh_token
from accountapp.models import  User, UserToken

from accountapp.permission import  IsOrganizer , IsOrganizerOrUser
from accountapp.serializers import UserSerializer
  

class RegisterAPIView(APIView):
    permission_classes = [AllowAny] # anyone can access this endpoint
    authentication_classes = [] # JWTAuthentication is not given ,because this is not a protected route,means anyone can register
    
    def post(self, request: Request):
        user = request.data
        print(f'User data received: {user}')
        
        if User.objects.filter(email=user['email']).exists():
            raise exceptions.APIException('Email already exists!')

        if User.objects.filter(username=user['username']).exists():
            raise exceptions.APIException('Username already exists!')

        if user['password'] != user['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny] # anyone can login
    authentication_classes =[] # no authentication required for login -> JWTAuthentication is not given ,because this is not a protected route,means anyone can login

    def post(self, request: Request):
        email = request.data['email']
        password = request.data['password']

        # check if user exist
        user =User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        # Check if password is correct
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid password')
        
        if user.role == 'organizer' and not user.is_approved:
            raise exceptions.AuthenticationFailed('Sorry!, you are not yet approved')  # only for organizer
        
        # Generate access and refresh tokens
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # Save refresh token of a specific user with an expiration date of 7 days
        UserToken.objects.create(
            user=user, 
            token=refresh_token, 
            expired_at = timezone.now() + timedelta(days=7)
        )
        
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return response
    
# Check Authenticated User      
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOrganizerOrUser]  # Ensure only authenticated users who can be a user or admin can access this view

    def get(self, request: Request):
        user = request.user
        print(user)
        # Django models can have built-in permissions which are set in the model's Meta class
        # permissions = request.user.get_all_permissions()
        # "permissions": list(permissions)
        # is_admin = request.auth.get('is_admin', False)

        serializer = UserSerializer(user)
        return Response(
            {
            'user': serializer.data,
            'role': user.role,
            'is_user': user.role == 'user',
            'is_organizer': user.role == 'organizer'
            
            }
        )

# Logout User    
class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request: Request):
        refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token missing'}, status=400)

        UserToken.objects.filter(token=refresh_token).delete()

        response: Response = Response({
            'status': 'success',
            'message': 'Logged out successfully'
        }, status=200)

        response.delete_cookie(key='refresh_token')
        return response


# class ProfileViewSet(ModelViewSet):
#     queryset:QuerySet = MyProfile.objects.all()
#     serializer_class=ProfileSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def perform_create(self ,serializer):
#         user = self.request.user
#         print("Inside perform_create -> ",user.first_name)
#         if user.role != 'organizer':
#             raise PermissionDenied("Only organizers can access profile")
#         # print(serializer.data)
#         # prevent duplicate event title
#         # profile_id = serializer.data.get('gender')
#         # print(f"Creating event with title :{profile_id},{profile_id.id} for user: {user}")

#         if MyProfile.objects.filter(organizer=user).exists():
#             raise exceptions.ValidationError("Account already exists")
        
#         serializer.save(organizer=user)

#     # Edit a course - Only the professor who created it
#     def perform_update(self, serializer):
#         myProfile = self.get_object()      # This will get the course instance being updated from queryset = Course.objects.all() 
#         user = self.request.user

#         print(f'User details: {user}')

#         if user.role != 'organizer' or myProfile.organizer != user:
#             raise PermissionDenied("You can only update your own profile.")
#         serializer.save()

#     @action(detail=False , methods=['get'],url_path='my-profile' , permission_classes=[IsOrganizer])
#     def my_profile(self, request):
#         user = request.user
#         if user.role != 'organizer':
#             raise PermissionDenied("Only you can see your own created events")
#         # org_email = serializer.
#         try:
#              my_profile = MyProfile.objects.get(organizer=user)
#         except MyProfile.DoesNotExist:
#             return Response({"detail": "Profile not found"}, status=404)
#         serializer = self.get_serializer(my_profile)
#         print(serializer)
#         return Response(serializer.data)

    


