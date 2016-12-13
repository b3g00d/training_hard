Upload Service
==============
Upload/Select/List/Rename/Delete picture voi username

- Thiet ke voi Flask va RAML

API Reference
-------------
### Paging
Params: ''

Request:
```
curl -X GET http://localhost:5000/images
```

Response sccuess:
```json
{
	"result": {
		
	}
}

```

### Select
Params: '?name=name&user=admin'

### Get a picture

Request:
```
curl -X GET -G 'http://localhost:5000/select' -d 'user=admin' -d 'name=name'
```

Response success:
```json
{
	{"name":
		{
			"path": "path"
			"size": "size"
			"fullname": "fullname"
		}
	}
}
```

### Rename a picture

Request:
```
curl -H 'Content-Type: application/json' -X PUT -d '{"name": "anar", "user": "admin", "rename": "hello"}' http://localhost:5000/images/rename
```

Response success:
```
Done!!
```

### Delete a picture

Request:
```
curl -H 'Content-Type: application/json' -X PUT -d '{"name": "anar", "user": "admin"}' http://localhost:5000/images/delete
```

Response success:
```
Done!!!
```

Init DB:
--------

- python3 my_db db init
- python3 my_db db migrate
- python3 init_db

Test Upload service:
--------------------

- cd test
- python3 service_test.py
