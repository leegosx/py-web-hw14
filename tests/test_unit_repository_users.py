import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import datetime
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.schemas import UserModel, ResponseUser
from src.database.models import User
from src.repository.users import (
    create_user,
    get_user_by_email,
    update_avatar,
    update_token,
    confirmed_email,
)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = UserModel(
            username = "JonikDoe",
            email = "tes2t@gmail.com",
            password = "5672348Q"
        )
        
    async def test_get_user_by_email(self):
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, self.user)


    async def test_create_user(self):
        result = await create_user(body=self.body, db=self.session)
        self.assertEqual(result.username, self.body.username)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.password, self.body.password)


    async def test_update_token(self):
        self.session.query().filter().first.return_value = self.user
        token = "testtoken"
        await update_token(user=self.user, token=token, db=self.session)
        self.assertTrue(self.user.refresh_token)
        self.assertEqual(self.user.refresh_token, token)


    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        await confirmed_email(email=self.user.email, db=self.session)
        self.assertTrue(self.user.confirmed)


    async def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user
        url = "http://localhost.jpeg"
        result = await update_avatar(email=self.user.email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)

    async def test_get_user_by_email_not_succes(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()