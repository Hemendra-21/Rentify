from dataclasses import dataclass
from typing import Optional
from enum import Enum

# from app.main.models.user import UserRole


# class UserRole(str, Enum):
#     tenant = "tenant"
#     landlord = "landlord"


@dataclass
class UserRegisterDto:
    first_name:str 
    last_name:str 
    email:str 
    phone:str 
    password : str 
    # role= UserRole.tenant


@dataclass
class UserOutputDTO:
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    # role: UserRole
    is_active: bool
    identity_verified: bool
    profile_image: Optional[str]