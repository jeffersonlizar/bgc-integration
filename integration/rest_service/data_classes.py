from dataclasses import dataclass
from datetime import date
from typing import Dict, List


@dataclass
class CheckData:
    first_name: str
    middle_names: str
    no_middle_name: bool
    last_name: str
    email: str
    birthdate: date
    social_security_number: str
    zip_code: str
    driver_license_number: str
    driver_license_state: str
    phone: str
    state_code: str
    city_name: str
    transportation: str
    external_id: str
    start_url: str
    candidate_id: str


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
