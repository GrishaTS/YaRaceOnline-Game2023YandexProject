from core.exceptions import ValidationError
from users.sign_up.models import users_model


def validate_agreement(agreement, con=None):
    if not agreement:
        raise ValidationError('Confirm Personal Data Processing Policy')
    return True


def validate_login(login, con=None):
    login = login.strip()
    if not login:
        raise ValidationError('Not valid login')
    if login.strip() == 'login':
        raise ValidationError('Such login is prohibited')
    data = users_model.select_user_login(login=login)
    if len(data) > 0:
        raise ValidationError('Such login already exists')
    return login