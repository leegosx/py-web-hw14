import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import datetime
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.schemas import ContactModel, ResponseContact
from src.database.models import Contact, User
from src.repository.contacts import (
    get_contact,
    get_contacts,
    create_contact,
    update_contact,
    remove_contact,
    search_contacts,
    get_upcoming_birthdays
)

class TestAsync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = ContactModel(
            id=1,
            first_name='John',
            last_name='Doe',
            email='johndoe@gmail.com',
            phone='+38055011222',
            birthday=datetime.date(year=1990, month=1, day=1)
        )
        
    async def test_get_contact(self):
        expected_contact = Contact()
        self.session.query().filter().first.return_value = expected_contact
        result = await get_contact(self.user.id, self.user, self.session)
        self.assertEqual(result, expected_contact)
        
    async def test_get_contact_not_found(self):
        expected_contacts = None
        self.session.query().filter().first.return_value = expected_contacts
        result = await get_contact(self.user.id, self.user, self.session)
        self.assertEqual(result, expected_contacts)
        
    async def test_get_contacts(self):
        excepted_contacts = [Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = excepted_contacts
        result = await get_contacts(skip=0, limit=3, db=self.session, user=self.user)
        self.assertEqual(result, excepted_contacts)
        
    async def test_create_contact(self):
        result = await create_contact(self.body, self.user, self.session)
        self.assertEqual(result.first_name, self.body.first_name)
        self.assertEqual(result.last_name, self.body.last_name)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.phone, self.body.phone)
        self.assertEqual(result.birthday, self.body.birthday)
        
    async def test_update_contact(self):
        body = ResponseContact(
            id=1,
            first_name="Bob",
            last_name="Willyams",
            email="test@gmail.com",
            phone="+38066911123",
            birthday=datetime.date(year=2000, month=2, day=2)
        )
        self.session.query().filter().first.return_value = self.body
        result = await update_contact(body.id, body, self.user, self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    async def test_remove_contact(self):
        expected_contacts = Contact()
        self.session.query().filter().first.return_value = expected_contacts
        result = await remove_contact(self.user.id, self.user, self.session)
        self.assertEqual(result, expected_contacts)
    
    async def test_search_contacts(self):
        expected_contacts = []
        self.session.query().filter().all.return_value = expected_contacts
        result = await search_contacts(query="test@test.com", user=self.user, db=self.session)
        self.assertEqual(result, expected_contacts)
    
    async def test_get_upcoming_birthdays(self):
        user = MagicMock()
        user.id = 1
        
        contact = Contact(birthday=datetime.date.today() + datetime.timedelta(days=1))
        db = MagicMock(spec=Session)
        db.query().filter().all.return_value = [contact]
        
        result = await get_upcoming_birthdays(2, user, db)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].birthday, contact.birthday)
        
if __name__ == '__main__':
    print(TestAsync.setUp)
    unittest.main()