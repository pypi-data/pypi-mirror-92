from unittest import TestCase

from auth_util import JwtManager


class TestJwt(TestCase):
    jwt = JwtManager()

    def test_password_gen(self):
        username, user_id = '李雷', 3
        t = self.jwt.gen_jwt(username=username, user_id=user_id)
        res = self.jwt.decode_jwt(t)
        self.assertEqual(res['username'], username)
        self.assertEqual(res['user_id'], user_id)
