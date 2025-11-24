# Cryptid
A web application with FastAPI

## Runtime Environment
### Create Virtual Environment
To create a virtual environment and install dependent packages, run the following command in the project root directory.
```sh
$ poetry install
```

### Create Configuration File
Create the `.env` file with the following content in the project root directory.
```text
CRYPTID_JWT_ALGORITHM=HS256
# 15: expires in 15 minutes, -1: not expires
CRYPTID_JWT_EXPIRES_IN_MINUTES=15
CRYPTID_JWT_SECRET_KEY=<jwt secret key>
```

To create the JWT secret key for the HS256 algorithm, run the following Python script.   
```python
import secrets
SECRET_KEY = secrets.token_urlsafe(32)
print(SECRET_KEY)
```
