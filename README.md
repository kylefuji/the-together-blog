# The Together Blog API

This API uses Django to serve requests. It has been made with TDD in mind. Thus, it has unit tests with over 90% code coverage and utilizes static analysis with sonarcloud to keep track of technical debt and security risks/hotspots.

You can find the coverage reports here:

https://app.codecov.io/gh/kylefuji/the-together-blog

You can find the SonarCloud static analysis reports here:

https://sonarcloud.io/dashboard?id=kylefuji_the-together-blog

You can find the deployed url here:

https://main-itq44jw09f2jr4rj-gtw.qovery.io/

## API Endpoints

### Login

#### /api/login/

Accepted methods: POST

Example body:
```
{
  "username":"example",
  "password":"12345"
}
```

Expected Return:
- It will return csrf header information which need to be sent with all subsequent requests to determine the user is logged in.
```
{
  "message": "user logged in"
}
```

Expected errors:
- 401 invalid login attempt, unable to login
- 405 invalid method, sent a method other than POST

### Logout

#### /api/logout/

Accepted Methods: GET, PUT, POST
- You must be logged in by sending a proper csrf token to logout

Expected Return:
```
{
  "message": "user logged out"
}
```

Expected Errors:
- 401 user not logged in, request didn't have csrf information that indicates user is logged in
- 405 invalid method, sent a DELETE request

### Albums

#### /api/album/

Accepted Methods: GET, POST

GET Requests:

Accepted Query Parameters:
- page (int): page number for the request, default is 1
- size (int): page size, default is 10
- search (url encoded string): search values

Example Return:
```
{
  "page": {
    "number": 1, 
    "hasNext": false, 
    "hasPrev": false, 
    "startIndex": 1, 
    "endIndex": 3, 
    "size": 10
  }, 
  "albums": [
    {
      "id": "44e20c35-a614-47d5-b6c3-aa205b8d6c5c", 
      "title": "test curl", 
      "description": "test curl description", 
      "imageURL": null, 
      "created": "2021-05-04T00:23:13.304Z"
    }, 
    {
      "id": "aef99268-85b0-4e86-9d39-3548adb370cd", 
      "title": "test curl album", 
      "description": "test curl album description", 
      "imageURL": null, 
      "created": "2021-05-03T22:37:53.922Z"
    }
  ]
}
```

POST Requests:

Example Body:

Minimum for creating a post:
```
{
  "title": "test post",
  "description": "test post content"
}
```
All possible fields:
```
{
  "title": "test post",
  "description": "test post content",
  "imageURL": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__340.jpg"
}
```
Expected Errors:
- 400, could not create album
- 401, not logged in

#### /api/album/<album_id>/

- album_id is the id for the album
Accepted Methods: GET, PUT, POST, DELETE

GET Requests:

Example Return:
```
{
  "id": "aef99268-85b0-4e86-9d39-3548adb370cd", 
  "title": "test curl album", 
  "description": "test curl album description", 
  "imageURL": null, 
  "created": "2021-05-03T22:37:53.922Z"
}
```

POST Requests:

Example Body:
```
{
  "title": "test curl album", 
  "description": "test curl album description"
}
```

Example Return:
```
{
  "id": "aef99268-85b0-4e86-9d39-3548adb370cd", 
  "title": "test curl album", 
  "description": "test curl album description", 
  "imageURL": null, 
  "created": "2021-05-03T22:37:53.922Z"
}
```

Expected Errors:
- 400, could not create album
- 401, not logged in

PUT Requests:

Example Body:
```
{
  "title": "test curl album"
}
```

Example Return:
```
{
  "id": "aef99268-85b0-4e86-9d39-3548adb370cd", 
  "title": "test curl album", 
  "description": "test curl album description", 
  "imageURL": null, 
  "created": "2021-05-03T22:37:53.922Z"
}
```

Expected Errors:
- 400, could not edit album
- 401, user not logged in

DELETE Requests:

Expected Return:
```
{
  "message": "album deleted"
}
```
Expected Errors:
- 400, could not delete album, album doesn't exist in the first place
- 401, user not logged in

### Posts

#### /api/post/

Accepted Methods: GET, POST

GET Requests:

Accepted Query Parameters:
- page (int): page number for the request, default is 1
- size (int): page size, default is 10
- search (url encoded string): search values

Expected Return:
```
{
  "page": {
    "number": 1, 
    "hasNext": false, 
    "hasPrev": false, 
    "startIndex": 1, 
    "endIndex": 3, 
    "size": 10
  }, 
  "posts": [
    {
      "id": "41e2bb21-de0b-4217-a744-0b03faef0468", 
      "user": "kyle", 
      "title": "test curl", 
      "content": "test curl content", 
      "created": "2021-05-04T00:21:09.218Z", 
      "imageURLs": [], 
      "videoURLs": [], 
      "album": null
    }, 
    {
      "id": "e9d1cb2a-2101-4028-afe3-bfd9eac67b73", 
      "user": "kyle-admin", 
      "title": "test", 
      "content": "test", 
      "created": "2021-05-03T07:20:26.247Z", 
      "imageURLs": [], 
      "videoURLs": [], 
      "album": "aef99268-85b0-4e86-9d39-3548adb370cd"
    }
  ]
}
```

POST Requests:

Example Body:

Minimum for creating a post:
```
{
  "title": "test post",
  "content": "test post content"
}
```
All possible fields:
```
{
  "title": "test post",
  "content": "test post content",
  "imageURLs": [
    "https://image.shutterstock.com/image-photo/mountains-under-mist-morning-amazing-260nw-1725825019.jpg",
    "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__340.jpg"
  ],
  "videoURLs": [
    "https://www.youtube.com/watch?v=bsaAOun-soc",
    "https://www.youtube.com/watch?v=8cyMWK4ZjT8"
  ],
  "album": "aef99268-85b0-4e86-9d39-3548adb370cd"
}
```
Expected Errors:
- 400, could not create post
- 401, not logged in

#### /api/post/<post_id>/

- post_id is the id for the post
- 
Accepted Methods: GET, PUT, POST, DELETE

GET Requests:

Example Return:
```
{
  "id": "41e2bb21-de0b-4217-a744-0b03faef0468", 
  "user": "kyle", 
  "title": "test curl", 
  "content": "test curl content", 
  "created": "2021-05-04T00:21:09.218Z", 
  "imageURLs": [], 
  "videoURLs": [], 
  "album": null
}
```

POST Requests:

Example Body:
```
{
  "title": "test curl post", 
  "content": "test curl post content"
}
```

Example Return:
```
{
  "id": "41e2bb21-de0b-4217-a744-0b03faef0468", 
  "user": "kyle", 
  "title": "test curl", 
  "content": "test curl content", 
  "created": "2021-05-04T00:21:09.218Z", 
  "imageURLs": [], 
  "videoURLs": [], 
  "album": null
}
```

Expected Errors:
- 400, could not create post
- 401, not logged in

PUT Requests:

Example Body:
```
{
  "title": "test curl post"
}
```

Example Return:
```
{
  "id": "41e2bb21-de0b-4217-a744-0b03faef0468", 
  "user": "kyle", 
  "title": "test curl", 
  "content": "test curl content", 
  "created": "2021-05-04T00:21:09.218Z", 
  "imageURLs": [], 
  "videoURLs": [], 
  "album": null
}
```

Expected Errors:
- 400, could not edit post
- 401, user not logged in

DELETE Requests:

Expected Return:
```
{
  "message": "post deleted"
}
```
Expected Errors:
- 400, could not delete album, album doesn't exist in the first place
- 401, user not logged in
