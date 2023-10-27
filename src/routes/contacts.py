from typing import List

from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ResponseContact
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def create_new_contact(body: ResponseContact, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_new_contact function creates a new contact in the database.
        The function takes in a ResponseContact object, which is defined as follows:
            class ResponseContact(BaseModel):
                name: str = Field(..., title=&quot;The name of the contact&quot;, max_length=100)
                email: EmailStr = Field(..., title=&quot;The email address of the contact&quot;)
    
    :param body: ResponseContact: Get the data from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user who is currently logged in
    :return: A contact object
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.get("/all", response_model=List[ResponseContact], status_code=status.HTTP_200_OK,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def read_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_all_contacts function returns a list of contacts.
        The function takes in an optional skip and limit parameter to paginate the results.
        
    
    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user and pass it to the repository
    :return: A list of contact objects
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ResponseContact, 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def read_contact_by_id(contact_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact_by_id function returns a contact by its id.
        If the user is not logged in, an HTTP 401 Unauthorized error is returned.
        If the user does not have access to this contact, an HTTP 403 Forbidden error is returned.
        If no such contact exists with that id, an HTTP 404 Not Found error is returned.
    
    :param contact_id: int: Identify the contact to be retrieved
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the auth_service
    :return: A contact object
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ResponseContact, 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def update_contact(body: ResponseContact, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ResponseContact object containing the new values for the contact.
            - contact_id: An integer representing the id of an existing Contact object in our database.
            - db (optional): A Session instance that represents a connection to our PostgreSQL database, which is used to query and update data from it. If not provided, one will be created using get_db(). This argument is optional because we can use dependency injection to provide it automatically when needed by FastAPI's built-in Depends() function (see below
    
    :param body: ResponseContact: Pass the data that will be used to update the contact
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A responsecontact object, which is the same as the body
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/remove/{contact_id}", response_model=ResponseContact,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def remove_user(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_user function removes a user from the database.
        Args:
            contact_id (int): The id of the user to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The currently logged in user object. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Specify the contact id of the user to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :return: A contact object
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/find/{query}", response_model=List[ResponseContact], 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def find_contacts(query: str, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contacts function searches for contacts in the database.
        The function takes a query string and returns a list of contacts that match the query.
        If no contact is found, it raises an HTTPException with status code 404.
    
    :param query: str: Search for contacts in the database
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: A list of contacts, but the schema is expecting a single contact
    """
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.get("/birthday/{days}", response_model=List[ResponseContact],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])

async def contacts_birthday(days: int, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The contacts_birthday function returns a list of contacts with upcoming birthdays.
        The number of days is specified in the URL path, and the user ID is obtained from the JWT token.
    
    
    :param days: int: Specify how many days in advance to return the contacts
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A list of contact objects
    """
    contacts = await repository_contacts.get_upcoming_birthdays(days, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts