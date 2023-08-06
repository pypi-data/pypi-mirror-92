from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Optional

import jwt


@dataclass
class JwtManager(object):
    JWT_ISSUER: str = 'company'
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRE: timedelta = timedelta(hours=24)
    JWT_KEY: str = 'SECRET'
    JWT_AUTH_HEADER_PREFIX: str = 'JWT'

    def gen_jwt(self, username: str, user_id: int):
        """生成 jwt"""
        payload = {
            'username': username, 'user_id': user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + self.JWT_EXPIRE,
            "iss": self.JWT_ISSUER
        }
        token = jwt.encode(
            payload=payload,
            key=self.JWT_KEY,
            algorithm=self.JWT_ALGORITHM
        )

        return f"{self.JWT_AUTH_HEADER_PREFIX}{token}"

    def decode_jwt(self, token: str, key: Optional[str] = None,
                   algorithms: Optional[str] = ''):
        if not key:
            key = self.JWT_KEY
        if not algorithms:
            algorithms = self.JWT_ALGORITHM
        if self.JWT_AUTH_HEADER_PREFIX:
            token = token.replace(self.JWT_AUTH_HEADER_PREFIX, '')
        return jwt.decode(token, key, algorithms)
