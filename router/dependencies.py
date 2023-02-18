from fastapi import APIRouter, Depends
from fastapi.requests import Request
from custom_log import log


router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies=[Depends(log)]
)


def convert_headers(request: Request, seperator: str = "--"):
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} -- {value}")
    return out_headers


@router.get('')
def get_items(headers=Depends(convert_headers)):
    return {
        'items': ['a', 'b', 'c'],
        'headers': headers
    }


class Account:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


@router.post('/user')
def create_user(name: str, email: str, password: str, account: Account = Depends()):
    return {
        'name': account.name,
        'email': account.email
    }
