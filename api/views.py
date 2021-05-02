from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Album
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import uuid

NOT_AUTH = "not authenticated"
POST_CREATE_DENY = "could not create post"
ALBUM_CREATE_DENY = "could not create album"
POST_UPDATE_DENY = "could not update post"
ALBUM_UPDATE_DENY = "could not update album"

@csrf_exempt
def handle_login(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            response = {
                "message": "invalid login attempt"
            }
            return JsonResponse(response, status=401)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = {
                "message": "user logged in"
            }
            return JsonResponse(response, status=200)
        response = {
            "message": "invalid login attempt"
        }
        return JsonResponse(response, status=401)
    response = {
        "message": "invalid method"
    }
    return JsonResponse(response, status=405)

@csrf_exempt
def handle_logout(request):
    if not check_login(request):
        response = {
            "message": "user not logged in"
        }
        return JsonResponse(response, status=401)
    if request.method != "DELETE":
        logout(request)
        response = {
            "message": "user logged out"
        }
        return JsonResponse(response, status=200)
    response = {
        "message": "invalid method"
    }
    return JsonResponse(response, status=405)

def check_staff(request):
    try:
        current_user = request.user
        User.objects.get(username=current_user, is_staff=True) 
        return True
    except ObjectDoesNotExist:
        return False

def check_login(request):
    try:
        current_user = request.user
        User.objects.get(username=current_user) 
        return True
    except ObjectDoesNotExist:
        return False

def handle_post(request):
    if request.method == "GET":
        try:
            all_posts = Post.objects.all().order_by('-created')
            response = {"posts": []}
            for post in all_posts:
                post_dict = {
                    "id": post.id,
                    "user": str(post.user),
                    "title": post.title,
                    "content": post.content,
                    "created": post.created,
                    "imageURLs": post.imageURLs,
                    "videoURLs": post.videoURLs,
                }
                try:
                    post_dict["album"] = post.album.id
                except AttributeError:
                    post_dict["album"] = None
                response["posts"].append(post_dict)
            return JsonResponse(response, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=200)
    elif request.method == "POST":
        if not check_staff(request):
            return JsonResponse({"message":NOT_AUTH}, status=401)
        try:
            body = json.loads(request.body)
            current_user = request.user
            user = User.objects.get(username=current_user) 
            post = Post.objects.create(id=str(uuid.uuid4()), title=body["title"], \
                content=body["content"], user=user)
            
            if "imageURLs" in body:
                post.imageURLs = body["imageURLs"]
                post.save()
            if "videoURLs" in body:
                post.videoURLs = body["videoURLs"]
                post.save()
            
            if "album" in body:
                try:
                    album = Album.objects.get(id=body["album"])
                    post.album = album
                    post.save()
                except ObjectDoesNotExist:
                    None

            response = {
                "id": post.id,
                "user": str(post.user),
                "title": post.title,
                "content": post.content,
                "created": post.created,
                "imageURLs": post.imageURLs,
                "videoURLs": post.videoURLs,
            }
            try:
                response["album"] = post.album.id
            except AttributeError:
                response["album"] = None
            return JsonResponse(response, status=201)
        except IntegrityError:
            return JsonResponse({"message":POST_CREATE_DENY}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":POST_CREATE_DENY}, status=400)
        except KeyError:
            return JsonResponse({"message":POST_CREATE_DENY}, status=400)
    else:
        return JsonResponse({"message":"method not allowed"}, status=405)

def handle_album(request):
    if request.method == "GET":
        try:
            all_albums = Album.objects.all().order_by('-created')
            response = {"albums": []}
            for album in all_albums:
                response["albums"].append({
                    "id": album.id,
                    "title": album.title,
                    "description": album.description,
                    "imageURL": album.imageURL,
                    "created": album.created
                })
            return JsonResponse(response, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=200)
    elif request.method == "POST":
        if not check_staff(request):
            return JsonResponse({"message":NOT_AUTH}, status=401)
        try:
            body = json.loads(request.body)
            album = Album.objects.create(id=str(uuid.uuid4()), title=body["title"], \
                description=body["description"])
            if "imageURL" in body:
                album.imageURL = body["imageURL"]
                album.save()
            response = {
                "id": album.id,
                "title": album.title,
                "description": album.description,
                "imageURL": album.imageURL,
                "created": album.created
            }
            return JsonResponse(response, status=201)
        except IntegrityError:
            return JsonResponse({"message":ALBUM_CREATE_DENY}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":ALBUM_CREATE_DENY}, status=400)
        except KeyError:
            return JsonResponse({"message":ALBUM_CREATE_DENY}, status=400)
    else:
        return JsonResponse({"message":"method not allowed"}, status=405)

def handle_album_by_id(request, album_id):
    if request.method == "GET":
        try:
            album = Album.objects.get(id=album_id)
            response = {
                "id": album.id,
                "title": album.title,
                "description": album.description,
                "imageURL": album.imageURL,
                "created": album.created
            }
            return JsonResponse(response, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=200)

    elif request.method == "PUT" and check_staff(request):
        try:
            body = json.loads(request.body)
            album = Album.objects.get(id=album_id)
            for key in body:
                if key == "title":
                    album.title = body[key]
                elif key == "description":
                    album.description = body[key]
                elif key == "imageURL":
                    album.imageURL = body[key]
                else:
                    return JsonResponse({"message":ALBUM_UPDATE_DENY}, status=400)
            album.save()
            response = {
                "id": album.id,
                "title": album.title,
                "description": album.description,
                "imageURL": album.imageURL,
                "created": album.created
            }
            return JsonResponse(response, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"message":ALBUM_UPDATE_DENY}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":ALBUM_UPDATE_DENY}, status=400)

    elif request.method == "POST" and check_staff(request):
        try:
            body = json.loads(request.body)
            album = Album.objects.create(id=album_id, title=body["title"], \
                description=body["description"])
            if "imageURL" in body:
                album.imageURL = body["imageURL"]
                album.save()
            response = {
                "id": album.id,
                "title": album.title,
                "description": album.description,
                "imageURL": album.imageURL,
                "created": album.created
            }
            return JsonResponse(response, status=201)
        except IntegrityError:
            return JsonResponse({"message":ALBUM_CREATE_DENY}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":ALBUM_CREATE_DENY}, status=400)
        except KeyError:
            return JsonResponse({"message":ALBUM_CREATE_DENY}, status=400)
    
    elif request.method == "DELETE" and check_staff(request):
        try:
            album = Album.objects.get(id=album_id)
            album.delete()
            return JsonResponse({"message":"album deleted"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"message":"could not delete album"}, status=400)
    return JsonResponse({"message":NOT_AUTH}, status=401)

def handle_post_by_id(request, post_id):
    if request.method == "GET":
        try:
            post = Post.objects.get(id=post_id)
            response = {
                "id": post.id,
                "user": str(post.user),
                "title": post.title,
                "content": post.content,
                "created": post.created,
                "imageURLs": post.imageURLs,
                "videoURLs": post.videoURLs,
            }
            try:
                response["album"] = post.album.id
            except AttributeError:
                response["album"] = None
            return JsonResponse(response)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=200)
    elif request.method == "PUT" and check_staff(request):
        try:
            body = json.loads(request.body)
            post = Post.objects.get(id=post_id)
            for key in body:
                if key == "title":
                    post.title = body[key]
                elif key == "content":
                    post.content = body[key]
                elif key == "imageURLs":
                    post.imageURLs = body[key]
                elif key == "videoURLs":
                    post.videoURLs = body[key]
                elif key == "album":
                    try:
                        album = Album.objects.get(id=body[key])
                        post.album = album
                    except ObjectDoesNotExist:
                        None
                else:
                    return JsonResponse({"message":POST_UPDATE_DENY}, status=400)
            post.save()
            response = {
                "id": post.id,
                "user": str(post.user),
                "title": post.title,
                "content": post.content,
                "created": post.created,
                "imageURLs": post.imageURLs,
                "videoURLs": post.videoURLs,
            }
            try:
                response["album"] = post.album.id
            except AttributeError:
                response["album"] = None
            return JsonResponse(response, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"message":POST_UPDATE_DENY}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":POST_UPDATE_DENY}, status=400)

    elif request.method == "POST" and check_staff(request):
        try:
            current_user = request.user
            body = json.loads(request.body)
            post = Post.objects.create(id=post_id, user=current_user, title=body["title"], \
                content=body["content"])

            if "imageURLs" in body:
                post.imageURLs = body["imageURLs"]
                post.save()
            if "videoURLs" in body:
                post.videoURLs = body["videoURLs"]
                post.save()
            if "album" in body:
                try:
                    album = Album.objects.get(id=body["album"])
                    post.album = album
                    post.save()
                except ObjectDoesNotExist:
                    None
            response = {
                "id": post.id,
                "user": str(post.user),
                "title": post.title,
                "content": post.content,
                "created": post.created,
                "imageURLs": post.imageURLs,
                "videoURLs": post.videoURLs,
            }
            try:
                response["album"] = post.album.id
            except AttributeError:
                response["album"] = None
            return JsonResponse(response, status=201)
        except IntegrityError:
            return JsonResponse({"message":POST_CREATE_DENY}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":POST_CREATE_DENY}, status=400)
        except KeyError:
            return JsonResponse({"message":POST_CREATE_DENY}, status=400)

    elif request.method == "DELETE" and check_staff(request):
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({"message":"post deleted"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"message":"could not delete post"}, status=400)
    return JsonResponse({"message":NOT_AUTH}, status=401)