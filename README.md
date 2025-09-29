# Cryptid
A web application with FastAPI

## References
### How to create the JWT secret key
The following Python code snippet creates the JWT secret key for the HS256 algorithm.   
```python
import secrets
SECRET_KEY = secrets.token_urlsafe(32)
print(SECRET_KEY)
```
