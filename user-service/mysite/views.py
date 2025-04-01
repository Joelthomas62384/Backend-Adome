
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from app.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import requests 
from django.contrib.auth import get_user_model
from dotenv import dotenv_values
from django.shortcuts import redirect
import urllib.parse
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q





class LoginDataView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data =data)
        if serializer.is_valid():

            print(serializer.data)
            data = serializer.validated_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                print("error here")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            refresh  = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            access_token = AccessToken(access)
            expiration_timestamp = access_token['exp']

            response = Response( status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh) , httponly=True , samesite="None", domain='.localhost' , secure=True)
            response.set_cookie(key='access_token',  value = access, secure=True , httponly=True , samesite= "None")
            response.set_cookie(key='expiry', value=expiration_timestamp, secure=True, httponly=False, samesite="None", domain='.localhost')
            return response
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



User = get_user_model()



class LoginView(APIView):
    
    permission_classes = []
    authentication_classes = []
    def get(self,request):
        google_client_id = dotenv_values(".env")["GOOGLE_CLIENT_ID"]    
        frontend = dotenv_values(".env")["FRONTEND_URL"]
        redirect_uri = f"{frontend}/auth/callback"
        scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
        if hasattr(request , 'tenant'):
            state = request.tenant.subdomain
        else:
            state = ""
        # state = secrets.token_urlsafe(16)
        params = {
            'client_id': google_client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            "scope": scope,
            'state': state,
            'access_type':'offline',
            # "prompt":"select_account"
        }
        # print(redirect_uri)
        # print(google_client_id)
        user_email = request.COOKIES.get('user_email')
        if user_email:
            params["login_hint"] = user_email
        else:
            params['prompt'] = 'select_account'
       
        url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return redirect(url)




    def post(self,request, *args,**kwargs):
        print(request.path_info)
        try:
            code = request.data.get('code')
            state = request.data.get('state')
            error = request.data.get('error')
            if request.user.is_authenticated:
                return Response({"app" : request.tenant.subdomain})
            # print(code , state)
            if error:
                print("error")
                return Response({'error': 'Authentication failed!'}, status=status.HTTP_400_BAD_REQUEST)
            frontend = dotenv_values(".env")["FRONTEND_URL"]
            redirect_uri = f"{frontend}/auth/callback"
            print(redirect_uri)
            if error or not state :
                print("error or not state")
                return Response({'error': 'Authentication failed!'}, status=status.HTTP_400_BAD_REQUEST)
            token_url = "https://oauth2.googleapis.com/token"
            env = dotenv_values(".env")

            token_data = {
                "code": code,
                "client_id": env["GOOGLE_CLIENT_ID"],
                "client_secret": env["GOOGLE_CLIENT_SECRET"],
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }
            print(code)
            print(error)
            if error:
                return Response({'error': 'Authentication failed!'}, status=status.HTTP_400_BAD_REQUEST)
            token_response = requests.post(token_url,data=token_data)
            token_json = token_response.json()
            access_token = token_json.get('access_token')
           

        
        

            user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            user_info_params ={"access_token":access_token}
            user_info_response = requests.get(user_info_url,params=user_info_params)
            user_info = user_info_response.json()
            print(user_info)
            if user_info.get('error'):
                return Response({'error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


            email = str(user_info.get('email'))
            full_name = user_info.get('name')
            print(email)
            # print(email)
            picture = user_info.get('picture')
            
            username = email.split('@')[0]
            if not username:
                return Response({'error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


            user, created = User.objects.get_or_create(email=email, defaults={
                'username': username,
                'full_name': full_name,
                "profile_pic": picture

            })
            print(user , created)
            if created:
                user.set_unusable_password()
                user.save()

            print(user, " is user ")
            if user is None:
                return Response({'error': 'Error logging in try again'}, status=status.HTTP_400_BAD_REQUEST)

        
            app = request.tenant
        
            if state == 'public':

                tenantuser = TenantUsers.objects.filter(user=user, is_admin=True)
                if tenantuser.exists():
                    tenantuser = tenantuser.first()
                    app = tenantuser.tenant
                else:
                    if user: 
                        tenantuser, created = TenantUsers.objects.get_or_create(user=user, tenant=request.tenant)
            else:
                if user:
                    tenant = request.tenant
                    tenantuser, created = TenantUsers.objects.get_or_create(user=user, tenant=tenant)



            # print(app)
            refresh = RefreshToken.for_user(user)
            refresh['is_superuser'] = user.is_superuser
            refresh['is_staff'] = tenantuser.is_staff
            refresh['is_admin'] = tenantuser.is_admin
            refresh['banned'] = tenantuser.banned
            refresh['blocked'] = tenantuser.blocked
            if app:
                refresh['tenant'] = app.subdomain

            access = str(refresh.access_token)
            access_token = AccessToken(access)
            expiration_timestamp = access_token['exp']
            

            response = Response({'app':app.subdomain if app else "public" ,'refresh' : str(refresh) , 'access' :access , 'expiry' : expiration_timestamp}, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh) , httponly=True , samesite="None", domain='.localhost' , secure=True)
            response.set_cookie(key='access_token',  value = access, secure=True , httponly=True , samesite= "None")
            response.set_cookie(key='expiry', value=expiration_timestamp, secure=True, httponly=False, samesite="None", domain='.localhost')
            response.set_cookie(key='user_email', value=user.email, secure=True, httponly=True, samesite="None", domain='.localhost')
            print("cookies are set")
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            return Response({'error': f'External request error: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.COOKIES.get('refresh_token')
        old_access_token = request.COOKIES.get('access_token')
        
        if not token or not old_access_token:
            return Response({'error': 'Tokens missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            old_access_token = AccessToken(old_access_token)
            old_access_token.check_exp()
            return Response({'error': 'Access token is still valid'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass  

        try:
            refresh = RefreshToken(token)
            user = User.objects.get(id=refresh['user_id'])
            tenantuser = TenantUsers.objects.get(user=user, tenant=request.tenant)  
            
            refresh['is_superuser'] = user.is_superuser
            refresh['is_staff'] = tenantuser.is_staff
            refresh['is_admin'] = tenantuser.is_admin
            refresh['banned'] = tenantuser.banned
            refresh['blocked'] = tenantuser.blocked
            refresh['tenant'] = tenantuser.tenant.subdomain

            access = str(refresh.access_token)
            access_token = AccessToken(access)
            expiration_timestamp = access_token['exp']

            response = Response({'refresh' : str(refresh) , 'access' :access , 'expiry' : expiration_timestamp},status=status.HTTP_200_OK)
            response.set_cookie(key='refresh_token', value=str(refresh), secure=True, httponly=True, samesite="None", domain='.localhost')
            response.set_cookie(key='access_token', value=access, secure=True, httponly=True, samesite="None", domain='.localhost')
            response.set_cookie(key='expiry', value= expiration_timestamp   , secure=True, httponly=False, samesite="None", domain='.localhost')
            return response
        except Exception as e:
            response = Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('refresh_token', domain=None)
            response.delete_cookie('access_token', domain=None)
            response.delete_cookie('expiry', domain=None)
            return response
    

class GetUserView(APIView):
    # authentication_classes = [CustomJwtAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_authenticated:
            print(f"User: {request.user}")
            print(f"Is Authenticated: {request.user.is_authenticated}")

            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)    
class LogoutView(APIView):
    permission_classes = []
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token', domain=None)
        response.delete_cookie('access_token', domain=None)
        response.delete_cookie('expiry', domain=None)
        return response
    

    

class GetTenantUsersView(APIView):
    def get(self, request):
        try:
            paginator = PageNumberPagination()
            paginator.page_size = 12
            search = request.query_params.get('search',None)
            if search:
                tenantusers = TenantUsers.objects.filter(Q(user__email__icontains=search) | Q(user__full_name__icontains=search) | Q(user__username__icontains=search),tenant=request.tenant).order_by('id')
                paged_data = paginator.paginate_queryset(tenantusers, request)
                serializer = TenantUsersSerializer(tenantusers, many=True)
                return paginator.get_paginated_response(serializer.data)
            staffOnly:str = request.query_params.get('staffOnly','false')
            tenant = request.tenant
            tenantusers = TenantUsers.objects.filter(Q(is_staff=True if staffOnly.lower() == 'true' else False) | Q(is_admin =True if staffOnly.lower() == 'true' else False ),tenant=tenant,).order_by('id')
            paged_data = paginator.paginate_queryset(tenantusers, request)

            serializer = TenantUsersSerializer(paged_data, many=True)
            return paginator.get_paginated_response(serializer.data)
            # print(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class GetTenantUserView(APIView):
    def get(self, request):
        try:
            print(request.user)
            print(request.tenantuser)
            user = request.tenantuser
            print(user)
            serializer = TenantUsersSerializer(user, context={'request':request})
            print(serializer.data)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BanUserView(APIView):
    def post(self, request , username):
        try:
            print("Ban user")
            if not(request.tenantuser.is_admin or request.tenantuser.hasStaffPermission):

                return Response({'data':"Unauthorized access"} , status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(username=username)
            tenantuser = TenantUsers.objects.get(user=user, tenant=request.tenant)
            tenantuser.banned = not tenantuser.banned
            tenantuser.save()
            serializer = TenantUsersSerializer(tenantuser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class BlockUserView(APIView):
    def post(self, request , username):
        try:
            
            if not(request.tenantuser.is_admin or request.tenantuser.hasStaffPermission):

                return Response({'data':"Unauthorized access"} , status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(username=username)
            tenantuser = TenantUsers.objects.get(user=user, tenant=request.tenant)
            tenantuser.blocked = not tenantuser.blocked
            tenantuser.save()
            serializer = TenantUsersSerializer(tenantuser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TenantUserView(APIView):
    def get(self, request , username):
        try:
            user = User.objects.get(username=username)
            tenantuser = TenantUsers.objects.get(user=user, tenant=request.tenant)
            serializer = TenantUsersSerializer(tenantuser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self ,request, username):
        try:
            print(request.data)
            user = User.objects.get(username=username)
            tenantuser = TenantUsers.objects.get(user=user, tenant=request.tenant)
            serializer = TenantUsersSerializer(tenantuser, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)