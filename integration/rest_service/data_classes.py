from dataclasses import dataclass
from datetime import date
from typing import Dict, List


@dataclass
class CheckData:
    first_name: str
    middle_names: str
    last_name: str
    email: str
    dni: str
    birthdate: date
    social_security_number: str
    zip_code: str
    driver_license_number: str
    driver_license_state: str
    phone: str
    state_code: str
    city_name: str
    city_code: str
    transportation: str
    external_id: str
    start_url: str
    candidate_id: str
    country_code: str
    mothers_name: str = None
    city_of_birth: str = None
    country_of_birth: str = None
    driver_license_category: str = None
    driver_license_expiration_date: date = None
    social_identification_number: str = None


@dataclass
class ErrorDetail:
    code: str
    message: str


@dataclass
class Response:
    status: str = None
    external_id: str = None
    metadata: Dict = None
    error_details: List[ErrorDetail] = None
