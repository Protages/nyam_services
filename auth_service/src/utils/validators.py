import re
from typing import Union, Literal


_PasswordValidateRules = Union[bool, Literal[
    'min_length',
    'at_least_one_capital_letter',
    'at_least_one_number',
    'allowed_characters'
]]


def validate_password(
    password: str,
    exclude_rule: list[_PasswordValidateRules] | None = None
) -> None | list[str]:
    '''
    Validate password by some rules:
        min_length: Password must be at least 5 characters long.
        at_least_one_capital_letter: Password must contain at least one capital letter.
        at_least_one_number: Password must contain at least one number.
        allowed_characters: Password cannot contain such characters 
        (^[a-zA-Z\d!@#$%^&*()_+={}\[\]|\\:;'\'<>,.?\/]+$).

    :param exclude_rule: List of excluded rules for password validation.
    '''
    # Full regular expression
    # regex = '^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()_+={}\[\]|\\:;'\'<>,.?\/]{6,}$'
    errors = []

    def min_length(password: str):
        if len(password) < 5:
            errors.append('Password must be at least 5 characters long.')

    def at_least_one_capital_letter(password: str):
        regex = '^.*[A-Z]+.*$'
        if re.fullmatch(regex, password) is None:
            errors.append('Password must contain at least one capital letter.')

    def at_least_one_number(password: str):
        regex = '^.*[\d]+.*$'
        if re.fullmatch(regex, password) is None:
            errors.append('Password must contain at least one number.')

    def allowed_characters(password: str):
        regex = '^[a-zA-Z\d!@#$%^&*()_+={}\[\]|\\:;"\'<>,.?\/]+$'
        if re.fullmatch(regex, password) is None:
            errors.append('Password cannot contain such characters.')

    all_rules = [
        min_length,
        at_least_one_capital_letter,
        at_least_one_number,
        allowed_characters
    ]

    password_validators = [
        func
        for func in all_rules
        if func.__name__ not in exclude_rule
    ] if exclude_rule else all_rules

    for validator in password_validators:
        validator(password)

    return errors if errors else None
