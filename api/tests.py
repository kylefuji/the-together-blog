from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from api.models import Post, Album
import uuid

CONTENT_JSON = "application/json"
TITLE = "test title"
CONTENT = "test content"
DESCRIPTION = "test description"
IMAGEURLS = ["https://images.all-free-download.com/images/graphicthumb/river_dane_563933.jpg", 
"https://thumbs.dreamstime.com/b/sad-panorama-neutral-tones-trees-brushes-near-stones-close-up-go-to-fog-to-incognito-nice-scene-some-space-173431211.jpg"]
VIDEOURLS = ["https://www.youtube.com/watch?v=UOZpCJhxv-w", "https://www.youtube.com/watch?v=ZOMiENsrhPU"]
IMAGEURL = "https://images.all-free-download.com/images/graphicthumb/river_dane_563933.jpg"

class TestLogin(TestCase):
    def setUp(self):
        self.adminPassword = '12345'
        self.test_admin = User.objects.create_superuser('test', password=self.adminPassword)
        self.c = Client()

    # Login tests
    def testInvalidLoginInfo(self):
        body = {
            "username": '',
            "password": ''
        }
        response = self.c.post(reverse('login'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testInvalidLoginContentType(self):
        body = {
            "username": '',
            "password": ''
        }
        response = self.c.post(reverse('login'), body)
        self.assertEquals(response.status_code, 401)

    def testLogin(self):
        body = {
            "username": self.test_admin.username,
            "password": self.adminPassword
        }
        response = self.c.post(reverse('login'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)

    def testWrongMethodLogin(self):
        response = self.c.get(reverse('login'))
        self.assertEquals(response.status_code, 405)

    # Logout tests
    def testLogoutNotAuthenticated(self):
        response = self.c.get(reverse('logout'))
        self.assertEquals(response.status_code, 401)

    def testWrongMethodLogout(self):
        body = {
            "username": self.test_admin.username,
            "password": self.adminPassword
        }
        self.c.post(reverse('login'), body, content_type=CONTENT_JSON)
        response = self.c.delete(reverse('logout'))
        self.assertEquals(response.status_code, 405)

    def testLogout(self):
        body = {
            "username": self.test_admin.username,
            "password": self.adminPassword
        }
        self.c.post(reverse('login'), body, content_type=CONTENT_JSON)
        response = self.c.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)



class TestApi(TestCase):
    def setUp(self):
        self.adminPassword = '12345'
        self.test_admin = User.objects.create_superuser('test', password=self.adminPassword)
        self.c = Client()
        self.test_post = Post.objects.create(id=str(uuid.uuid4()),
            title=TITLE,
            content=CONTENT,
            user=self.test_admin)
        
        self.test_album = Album.objects.create(id=str(uuid.uuid4()),
            title=TITLE,
            description=DESCRIPTION)

    # Posts api tests
    def testGetPosts(self):
        response = self.c.get(reverse('api_post'))
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedNewPost(self):
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.post(reverse('api_post'), body)
        self.assertEquals(response.status_code, 401)


    def testAuthenticatedInvalidEmptyNewPost(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {}
        response = self.c.post(reverse('api_post'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedInvalidPostType(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.post(reverse('api_post'), body)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedNewPostInvalidAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": "invalid id"
        }
        response = self.c.post(reverse('api_post'), body, content_type=CONTENT_JSON)
        self.testPost = response.json()
        self.assertEquals(response.status_code, 201)
    
    def testAuthenticatedNewPost(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.post(reverse('api_post'), body, content_type=CONTENT_JSON)
        self.testPost = response.json()
        self.assertEquals(response.status_code, 201)

    def testInvalidPostMethod(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.put(reverse('api_post'), body, content_type=CONTENT_JSON)
        self.testPost = response.json()
        self.assertEquals(response.status_code, 405)

    # Albums api tests
    def testGetAlbums(self):
        response = self.c.get(reverse('api_album'))
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedNewAlbum(self):
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.post(reverse('api_album'), body)
        self.assertEquals(response.status_code, 401)


    def testAuthenticatedInvalidEmptyNewAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {}
        response = self.c.post(reverse('api_album'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedInvalidAlbumType(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.post(reverse('api_album'), body)
        self.assertEquals(response.status_code, 400)
    
    def testAuthenticatedNewAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.post(reverse('api_album'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201)

    def testInvalidAlbumMethod(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.put(reverse('api_album'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 405)
    

    # Post by ID tests
    def testGetInvalidPostById(self):
        kwargs = {
            "post_id": "invalid id"
        }
        response = self.c.get(reverse('api_post_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {})

    def testGetPostById(self):
        kwargs = {
            "post_id": self.test_post.id
        }
        response = self.c.get(reverse('api_post_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})

    def testUnauthenticatedEditPostById(self):
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedEditPostByIdInvalidId(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "invalid id"
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedEditPostByIdInvalidAttribute(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id,
            "invalid parameter": "invalid value"
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedEditPostByIdInvalidType(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedEditPostByIdEmpty(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {}
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)

    def testAuthenticatedEditPostByIdInvalidAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": "invalid id"
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)

    def testAuthenticatedEditPostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedCreatePostById(self):
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedCreatePostByIdInvalidType(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedCreatePostByIdEmpty(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {}
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedCreatePostByIdInvalidAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": "invalid id"
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201)

    def testAuthenticatedCreatePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201) 

    def testAuthenticatedCreateDuplicatePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT,
            "imageURLs": IMAGEURLS,
            "videoURLs": VIDEOURLS,
            "album": self.test_album.id
        }
        self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testUnauthenticatedDeletePostById(self):
        kwargs = {
            "post_id": self.test_post.id
        }
        response = self.c.delete(reverse('api_post_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedDeletePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        response = self.c.delete(reverse('api_post_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

    def testAuthenticatedDeleteInvalidPostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "2"
        }
        response = self.c.delete(reverse('api_post_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 400)


    # Album by id tests
    def testGetInvalidAlbumById(self):
        kwargs = {
            "album_id": "invalid id"
        }
        response = self.c.get(reverse('api_album_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {})

    def testGetAlbumById(self):
        kwargs = {
            "album_id": self.test_album.id
        }
        response = self.c.get(reverse('api_album_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})

    def testUnauthenticatedEditAlbumById(self):
        kwargs = {
            "album_id": self.test_album.id
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedEditAlbumByIdInvalidParameter(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": self.test_album.id
        }
        body = {
           "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL,
            "invalid entry": "invalid value"
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedEditAlbumByIdEmpty(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": self.test_album.id
        }
        body = {}
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)

    def testAuthenticatedEditAlbumByIdInvalidId(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "invalid id"
        }
        body = {
           "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedEditAlbumByIdInvalidType(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "invalid id"
        }
        body = {
           "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedEditAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": self.test_album.id
        }
        body = {
           "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedCreateAlbumById(self):
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedCreateAlbumByIdEmpty(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {}
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)
    
    def testAuthenticatedCreateAlbumByIdInvalidType(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body)
        self.assertEquals(response.status_code, 400)

    def testAuthenticatedCreateAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201)

    def testAuthenticatedCreateDuplicateAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION,
            "imageURL": IMAGEURL
        }
        self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)

    def testUnauthenticatedDeleteAlbumById(self):
        kwargs = {
            "album_id": self.test_post.id
        }
        response = self.c.delete(reverse('api_album_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedDeleteAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": self.test_album.id
        }
        response = self.c.delete(reverse('api_album_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

    def testAuthenticatedDeleteInvalidAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "invalid id"
        }
        response = self.c.delete(reverse('api_album_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 400)

