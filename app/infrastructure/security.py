from dataclasses import dataclass
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt


@dataclass
class Security:
    SECRET_KEY: str
    ALGORITHM: str

    def pwd_context(self):
        return CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12
        )

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    
    def payload_from_token(self, token: str) -> dict:
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])