from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


def hash(password: str):
    #pw_bytes= password.encode('utf-8')
    #SHA_256 = hashlib.sha256(pw_bytes).digest()
    hashed_pw = pwd_context.hash(password)
    return hashed_pw


def verify(password:str, hashed_pw:str) -> bool:
    #pw_bytes= password.encode('utf-8')
    #SHA_256 = hashlib.sha256(pw_bytes).digest()
    
    return pwd_context.verify(password, hashed_pw)


#pip install passlib[argon2]


