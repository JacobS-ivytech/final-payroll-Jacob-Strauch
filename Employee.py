from dataclasses import dataclass


@dataclass
class Employee:
    
    id: int
    fname: str
    lname: str
    status: str
    department: str
    title: str
    dob: str
    gender: str
    payType: str
    payRate: str
    email: str
    address: str
    zipCode: str
    dependents: int
    admin: int
    password: str
