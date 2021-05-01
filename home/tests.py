from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from home.models import Post, Album
import uuid

CONTENT_JSON = "application/json"
TITLE = "test title"
CONTENT = "test content"
DESCRIPTION = "test description"

class TestLogin(TestCase):
    def setUp(self):
        self.adminPassword = '12345'
        self.test_admin = User.objects.create_superuser('test', password=self.adminPassword)
        self.c = Client()

    def testLoginNotAuthenticated(self):
        body = {
            "username": '',
            "password": ''
        }
        response = self.c.post(reverse('login'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testLoginAuthenticated(self):
        body = {
            "username": self.test_admin.username,
            "password": self.adminPassword
        }
        response = self.c.post(reverse('login'), body, content_type=CONTENT_JSON)
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

    def testGetPosts(self):
        response = self.c.get(reverse('api_post'))
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedNewPost(self):
        body = {
            "title": TITLE,
            "content": CONTENT
        }
        response = self.c.post(reverse('api_post'), body)
        self.assertEquals(response.status_code, 401)


    def testAuthenticatedInvalidNewPost(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {}
        response = self.c.post(reverse('api_post'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)
    
    def testAuthenticatedNewPost(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "content": CONTENT
        }
        response = self.c.post(reverse('api_post'), body, content_type=CONTENT_JSON)
        self.testPost = response.json()
        self.assertEquals(response.status_code, 201)

    def testGetAlbums(self):
        response = self.c.get(reverse('api_album'))
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedNewAlbum(self):
        body = {
            "title": TITLE,
            "description": DESCRIPTION
        }
        response = self.c.post(reverse('api_album'), body)
        self.assertEquals(response.status_code, 401)


    def testAuthenticatedInvalidNewAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {}
        response = self.c.post(reverse('api_album'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 400)
    
    def testAuthenticatedNewAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": TITLE,
            "description": DESCRIPTION
        }
        response = self.c.post(reverse('api_album'), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201)
    
    def testGetInvalidPostById(self):
        kwargs = {
            "post_id": "1"
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
            "title": TITLE
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedEditPostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": TITLE
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})

    def testUnauthenticatedCreatePostById(self):
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedCreatePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201)
        self.assertNotEquals(response.json(), {})

    def testAuthenticatedCreateDuplicatePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": TITLE,
            "content": CONTENT
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

    def testGetInvalidAlbumById(self):
        kwargs = {
            "album_id": "1"
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
            "title": TITLE
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedEditAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": self.test_album.id
        }
        body = {
            "title": TITLE
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})

    def testUnauthenticatedCreateAlbumById(self):
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedCreateAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type=CONTENT_JSON)
        self.assertEquals(response.status_code, 201)
        self.assertNotEquals(response.json(), {})

    def testAuthenticatedCreateDuplicateAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": TITLE,
            "description": DESCRIPTION
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
            "album_id": "2"
        }
        response = self.c.delete(reverse('api_album_id', kwargs=kwargs))
        self.assertEquals(response.status_code, 400)

