from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from src.database.models import Contact, User
from src.schemas import ContactModel
from datetime import timedelta, datetime

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.
    
    :param skip: int: Skip a certain number of contacts
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of contacts
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            contact_id (int): The id of the contact to retrieve.
            user (User): The user who owns the requested Contact.
            db (Session): A database session object for querying and updating data in our database.
    
    :param contact_id: int: Get the contact from the database
    :param user: User: Get the user_id of the user that is logged in
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Pass the contact data to the function
    :param user: User: Get the user id of the logged in user
    :param db: Session: Access the database
    :return: A contact object
    """
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user.
            user (User): The current logged-in user, used to determine if they have access to this resource.
            db (Session): A connection with our database, used for querying and updating data.
    
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactModel: Pass in the json data from the request
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: The contact object
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.user_id = user.id
        db.commit()
    return contact

async def remove_contact(contact_id: int, user: User, db: Session)  -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts being removed.
            db (Session): A connection to our database, used for querying and deleting data.
    
    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database
    :return: A contact object
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def search_contacts(query: str, user: User, db: Session):
    """
    The search_contacts function searches the database for contacts that match a given query.
        Args:
            query (str): The search term to look for in the database.
            user (User): The user who is making this request.
            db (Session): A connection to the database, which will be used to make queries and commit changes.
    
    :param query: str: Search for contacts in the database
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    contacts = (
        db.query(Contact)
        .filter(
            or_(
                Contact.first_name.contains(query),
                Contact.last_name.contains(query),
                Contact.email.contains(query)
            ),
            Contact.user_id == user.id
        )
        .all()
    )
    return contacts

async def get_upcoming_birthdays(days: int, user: User, db: Session):
    """
    The get_upcoming_birthdays function returns a list of contacts whose birthdays are within the next 'days' days.
        
    
    :param days: int: Specify how many days in advance the user wants to be notified of upcoming birthdays
    :param user: User: Get the user's id and then use it to filter all contacts in the database that belong to this user
    :param db: Session: Access the database
    :return: A list of contact objects
    """
    request = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in all_contacts:
        if timedelta(0) <= ((contact.birthday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            request.append(contact)

    return request