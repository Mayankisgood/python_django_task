from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import transaction
from .serializers import *
from django.conf import settings
from app.udf import *

# Create your views here.


# CRUD of user
@csrf_exempt
def user(request):
    try:
        with transaction.atomic():
            user_data = JSONParser().parse(request)
            if request.method == "POST": 
                user_email = user_data["email"]
                if not check_user_exist(user_email)[0]:     
                    user_register = user_serializer(data=user_data)
                    if user_register.is_valid():
                        user_data = user_register.save()
                        session_token = user_session_create(user_data.id,"added")
                        return JsonResponse({
                            "status": "Success",
                            "message": "User_detail saved Successfully",
                            "user_id": user_data.id,
                            "user_token": session_token,
                        })
                    return JsonResponse({
                        "status": "Failed",
                        "error_code": settings.ERROR_INVALID_DATA,
                        "message": user_register.errors
                    })   
                return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_ERROR_EXIST,
                    "message": "Email is already registered"
                })     
            if request.method == "GET":   
                user_id = user_data["user_id"]         
                user_ = user_info.objects.filter(id=user_id)
                if user_.exists():
                        list=[]  
                        for p in user_:                                              
                            data_ = {}
                            data_["user_id"] = p.id
                            data_["name"] = p.name   
                            data_["email"] = p.email                       
                            list.append(data_) 
                        return JsonResponse({
                            "status":"Success",
                            "data":{
                                "data": list                            
                            }                                
                        })
                return JsonResponse({
                        "status":"Failed",
                        "message": "No data found with given crediential.",
                        "error_code": settings.ERROR_NOT_EXIST ,
                    })       
            if request.method == "PUT":   
                user_id = user_data["user_id"]         
                profile_data = user_info.objects.get(id=user_id)
                serializer = user_serializer(profile_data, data=user_data, partial=True)
                if serializer.is_valid():
                        serializer.save()      
                        return JsonResponse({
                            "status": "Success",
                            "message": "User updated Successfully"
                        })
                return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_INVALID_DATA,
                    "message": serializer.errors
                })        
            if request.method == "DELETE":   
                user_id = user_data["user_id"]         
                user_ = user_info.objects.filter(id=user_id)
                if user_.exists():               
                    user_.delete()      
                    return JsonResponse({
                        "status": "Success",
                        "message": "User deleted Successfully"
                    })
                return JsonResponse({
                        "status":"Failed",
                        "message": "No data found with given crediential.",
                        "error_code": settings.ERROR_NOT_EXIST ,
                    })        
            return JsonResponse({
                "status":"Failed",                
                "error_code":settings.ERROR_INVALID_REQUEST,                
                "message":f"Not a valid request {request.method}"                
            })
    except Exception as e:
        return JsonResponse({
            "status": "Failed",
            "error_code": settings.ERROR_ERROR_UNKNOWN,
            "message": f"Unknown Error - {e}"
        })



# CRUD of Post/blog

@csrf_exempt
def post(request):
    try:
        with transaction.atomic():
            user_data = JSONParser().parse(request)
            if request.method == "POST":
                post_register = post_serializer(data=user_data)
                if post_register.is_valid():
                    user_data = post_register.save()
                    return JsonResponse({
                            "status": "Success",
                            "message": "Post_detail saved Successfully",
                        })
                return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_INVALID_DATA,
                    "message": post_register.errors
                })   
            if request.method == "GET":   
                post_id = user_data["post_id"]         
                post_ = post_info.objects.filter(id=post_id)
                if post_.exists():
                        list=[]  
                        for p in post_:                                              
                            data_ = {}
                            data_["post_id"] = p.id
                            data_["title"] = p.title   
                            data_["discription"] = p.discription                       
                            data_["content"] = p.content                       
                            list.append(data_) 
                        return JsonResponse({
                            "status":"Success",
                            "data":{
                                "data": list                            
                            }                                
                        })
                return JsonResponse({
                        "status":"Failed",
                        "message": "No data found with given crediential.",
                        "error_code": settings.ERROR_NOT_EXIST ,
                    }) 
            if request.method == "PUT":   
                user_id = user_data['user_id']
                user_token = user_data['user_token']
                if authenticate_user(user_id, user_token):
                    post_id = user_data["post_id"]         
                    post_data = post_info.objects.get(id=post_id)
                    serializer = post_serializer(post_data, data=user_data, partial=True)
                    if serializer.is_valid():
                            serializer.save()      
                            return JsonResponse({
                                "status": "Success",
                                "message": "User updated Successfully"
                            })
                    return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_INVALID_DATA,
                    "message": serializer.errors
                }) 
                return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_USER_NOT_AUTHENTICATED,
                    "message": "Not authenticated"
                })
            if request.method == "DELETE":   
                user_id = user_data['user_id']
                user_token = user_data['user_token']
                if authenticate_user(user_id, user_token):
                    post_id = user_data["post_id"]         
                    post_ = post_info.objects.filter(id=post_id)
                    if post_.exists():               
                        post_.delete()      
                        return JsonResponse({
                            "status": "Success",
                            "message": "Post deleted Successfully"
                        })
                    return JsonResponse({
                            "status":"Failed",
                            "message": "No data found with given crediential.",
                            "error_code": settings.ERROR_NOT_EXIST ,
                        })  
                return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_USER_NOT_AUTHENTICATED,
                    "message": "Not authenticated"
                })
            return JsonResponse({
                "status":"Failed",                
                "error_code":settings.ERROR_INVALID_REQUEST,                
                "message":f"Not a valid request {request.method}"                
            })
    except Exception as e:
        return JsonResponse({
            "status": "Failed",
            "error_code": settings.ERROR_ERROR_UNKNOWN,
            "message": f"Unknown Error - {e}"
        })

# CRUD of like data
@csrf_exempt
def liked_saved_user(request):
    try:
        with transaction.atomic():
            data = JSONParser().parse(request)
            user_id = data["user_id"]
            user_token = data["user_token"]
            if authenticate_user(user_id, user_token):            
                if request.method == "POST":   
                    post_id = data["post_id"]                                                
                    data_ = like_serializer(data=data)
                    if data_.is_valid():
                        data_.save(user_id=user_id, post_id=post_id)
                        return JsonResponse({
                                    "status": "Success",
                                    "message": "like data added successfullly"
                                })
                    return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_INVALID_DATA,
                    "message": data_.errors
                })                    
                if request.method == "GET":   
                    like_id = data["like_id"]     
                    like_ = Liked_Saved.objects.filter(id=like_id)
                    if like_.exists():
                            list=[]  
                            for p in like_:                                              
                                data_ = {}
                                data_["id"] = p.id
                                data_["post_id"] = p.post_id
                                data_["user_id"] = p.user_id   
                                data_["user_name"] = f"{p.user.name}" 
                                data_["is_liked"] = p.is_liked                                           
                                list.append(data_) 
                            return JsonResponse({
                                "status":"Success",
                                "data":{
                                    "data": list                            
                                }                                
                            })
                    return JsonResponse({
                            "status":"Failed",
                            "message": "No data found with given crediential.",
                            "error_code": settings.ERROR_NOT_EXIST ,
                        }) 
                if request.method == "PUT":   
                    like_id = data["like_id"]         
                    post_data = Liked_Saved.objects.get(id=like_id)
                    serializer = like_serializer(post_data, data=data, partial=True)
                    if serializer.is_valid():
                            serializer.save()      
                            return JsonResponse({
                                "status": "Success",
                                "message": "Like data updated Successfully"
                            })
                    return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_INVALID_DATA,
                    "message": serializer.errors  })
                if request.method == "DELETE":   
                        like_id = data["like_id"]         
                        like_ = Liked_Saved.objects.filter(id=like_id)
                        if like_.exists():               
                            like_.delete()      
                            return JsonResponse({
                                "status": "Success",
                                "message": "like data deleted Successfully"
                            })
                        return JsonResponse({
                                "status":"Failed",
                                "message": "No data found with given crediential.",
                                "error_code": settings.ERROR_NOT_EXIST ,
                            })  
                return JsonResponse({
                "status":"Failed",                
                "error_code":settings.ERROR_INVALID_REQUEST,                
                "message":f"Not a valid request {request.method}"                
            })
            return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_USER_NOT_AUTHENTICATED,
                    "message": "Not authenticated"
                })
    except Exception as e:
        return JsonResponse({
            "status": "Failed",
            "error_code": settings.ERROR_ERROR_UNKNOWN,
            "message": f"Unknown Error - {e}"
        })
                    

