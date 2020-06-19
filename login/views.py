#from django.shortcuts import render
import json
from django.views import View
from .models import Users
from django.http import JsonResponse, HttpResponse
import bcrypt
import jwt
from westagram2.settings import SECRET_KEY

class SignUp(View):

    def post(self, request):
        account_data = json.loads(request.body)
        password = account_data['password']
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        decoded_pw = hashed_pw.decode('utf-8')

        try:
            if not Users.objects.filter(account=account_data['account']).exists():
                Users(
                  account = account_data['account'],
                  password = decoded_pw).save()
                return JsonResponse({'message':'welcome!'}, status=200)
            else:
                return JsonResponse({'message':'id already exists'},status=409)
        except KeyError:
            return JsonResponse({'message':"KeyError"}, status=400)


class SignIn(View):
    def post(self, request):
        account_data = json.loads(request.body)
        password = account_data['password']
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        decoded_pw = hashed_pw.decode('utf-8')

        try:
            if Users.objects.filter(account=account_data['account']).exists():
                account1 = Users.objects.get(account=account_data['account'])
                if bcrypt.checkpw(password.encode('utf-8'), account1.password.encode('utf-8'))== True:
                    token = jwt.encode({"user-id":account1.id}, SECRET_KEY, algorithm="HS256")
                    return JsonResponse({'token':token.decode('utf-8')}, status=200)
                else:
                    return JsonResponse({'message': 'password nono'}, status=401)
            
            else:
                return JsonResponse({'message': 'no such id'}, status=400)
        
        except KeyError:
            return JsonResponse({"message":"Keyerror"},status=400)



def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization", None)
        if access_token is not None: 
            try:
                decode_token = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
                user_id = decode_token["user-id"]
                user = Users.objects.get(id=user_id)
                request.user = user
                
                return func(self, request, *args, **kwargs)
            except jwt.DecodeError:
                return JsonResponse({'message' : 'INVALID TOKEN'}, status=400)
            except Users.DoesNotExist:
                return JsonResponse({'message': 'ACCOUNT NOT EXIST'}, status=400)
            except Exception as e:
                return e
        else:
           return JsonResponse({'message':'LOGIN REQUIRED'}, status=401)
    return wrapper
