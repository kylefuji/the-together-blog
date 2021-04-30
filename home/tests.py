from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from home.models import Post, Album
import uuid

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
        response = self.c.post(reverse('login'), body)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/login.html')

    def testLoginAuthenticated(self):
        body = {
            "username": self.test_admin.username,
            "password": self.adminPassword
        }
        response = self.c.post(reverse('login'), body)
        self.assertRedirects(response, expected_url=reverse('home'), status_code=302, target_status_code=200)


class TestApi(TestCase):
    def setUp(self):
        self.adminPassword = '12345'
        self.test_admin = User.objects.create_superuser('test', password=self.adminPassword)
        self.c = Client()
        self.test_post = Post.objects.create(id=str(uuid.uuid4()),
            title="test post",
            content="123456615323",
            user=self.test_admin)
        
        self.test_album = Album.objects.create(id=str(uuid.uuid4()),
            title="test album",
            description="test descr")

    def testGetPosts(self):
        response = self.c.get(reverse('api_post'))
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedNewPost(self):
        body = {
            "title": "test",
            "content": "test content"
        }
        response = self.c.post(reverse('api_post'), body)
        self.assertEquals(response.status_code, 401)


    def testAuthenticatedInvalidNewPost(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {}
        response = self.c.post(reverse('api_post'), body, content_type="application/json")
        self.assertEquals(response.status_code, 400)
    
    def testAuthenticatedNewPost(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": "test",
            "content": "test content"
        }
        response = self.c.post(reverse('api_post'), body, content_type="application/json")
        self.testPost = response.json()
        self.assertEquals(response.status_code, 201)

    def testGetAlbums(self):
        response = self.c.get(reverse('api_album'))
        self.assertEquals(response.status_code, 200)

    def testUnauthenticatedNewAlbum(self):
        body = {
            "title": "test",
            "description": "test description"
        }
        response = self.c.post(reverse('api_album'), body)
        self.assertEquals(response.status_code, 401)


    def testAuthenticatedInvalidNewAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {}
        response = self.c.post(reverse('api_album'), body, content_type="application/json")
        self.assertEquals(response.status_code, 400)
    
    def testAuthenticatedNewAlbum(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        body = {
            "title": "test",
            "description": "test description"
        }
        response = self.c.post(reverse('api_album'), body, content_type="application/json")
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
            "title": "edited post"
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedEditPostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": self.test_post.id
        }
        body = {
            "title": "edited post"
        }
        response = self.c.put(reverse('api_post_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})

    def testUnauthenticatedCreatePostById(self):
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": "new post",
            "content": "Hello"
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedCreatePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": "new post",
            "content": "Hello"
        }
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertNotEquals(response.json(), {})

    def testAuthenticatedCreateDuplicatePostById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "post_id": "1"
        }
        body = {
            "title": "new post",
            "content": "Hello"
        }
        self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type="application/json")
        response = self.c.post(reverse('api_post_id', kwargs=kwargs), body, content_type="application/json")
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
            "title": "edited post"
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedEditAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": self.test_album.id
        }
        body = {
            "title": "edited post"
        }
        response = self.c.put(reverse('api_album_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})

    def testUnauthenticatedCreateAlbumById(self):
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": "new post",
            "description": "Hello"
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 401)

    def testAuthenticatedCreateAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": "new post",
            "description": "Hello"
        }
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        self.assertNotEquals(response.json(), {})

    def testAuthenticatedCreateDuplicateAlbumById(self):
        self.client = self.c.login(username=self.test_admin.username, password=self.adminPassword)
        kwargs = {
            "album_id": "1"
        }
        body = {
            "title": "new post",
            "description": "Hello"
        }
        self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type="application/json")
        response = self.c.post(reverse('api_album_id', kwargs=kwargs), body, content_type="application/json")
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

