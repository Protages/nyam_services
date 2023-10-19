import httpx

from src.schemas.login import TokenSchema, TokenPayloadOutputSchema
from src.core.config import settings
from src.core.exceptions import AnotherServiceException
 

def get_hashed_password(password: str) -> str:
    '''Make request on `AUTH_SERIVICE` and return generated hashed password.'''

    url = f'{settings.AUTH_SERIVICE_URL}api/v1/password/get_hashed_password/'
    data = {'row_password': password}
    response: httpx.Response = httpx.post(url, json=data)
    if response.status_code >= 400:
        raise AnotherServiceException(response)
    return response.json().get('hashed_password')


def verify_password_and_get_token(
    user_id: int, row_password: str, hashed_password: str
) -> TokenSchema:
    '''
    Make request on `AUTH_SERIVICE` for verify passed row_password with 
    hashed_password and generate `token` if row_password verify.
    '''

    url = f'{settings.AUTH_SERIVICE_URL}api/v1/token/verify_password_and_get_token/'
    data = {
        'user_id': user_id, 
        'user_type': 'courier',
        'row_password': row_password,
        'hashed_password': hashed_password
    }
    response: httpx.Response = httpx.post(url, json=data)
    if response.status_code >= 400:
        raise AnotherServiceException(response)

    token_schema = TokenSchema(
        token=response.json().get('token'),
        token_type=response.json().get('token_type')
    )
    return token_schema


def verify_token_and_get_payload(token: str) -> TokenPayloadOutputSchema:
    '''
    Make request on `AUTH_SERIVICE` for `verify` passed token 
    and return `payload` in this token.
    '''

    url = f'{settings.AUTH_SERIVICE_URL}api/v1/token/verify_token/'
    data = {'token': token}
    response: httpx.Response = httpx.post(url, json=data)
    if response.status_code >= 400:
        raise AnotherServiceException(response)
    
    payload = TokenPayloadOutputSchema.model_validate(response.json())
    return payload
