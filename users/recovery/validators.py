from core.exceptions import ValidationError
from users.recovery.models import users_model


def validate_login(login, con):
    login = login.strip()
    data = users_model.select_user_login(login=login)
    if len(data) < 1:
        raise ValidationError('Such login doesn\'t exist. You need to sign up')
    assert len(data) == 1, 'Some users have the same login'
    return login
