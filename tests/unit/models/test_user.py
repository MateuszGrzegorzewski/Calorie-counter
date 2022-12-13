from main import create_app
from models.user import UserModel


class TestUser():
    def test_create_user(self):
        user = UserModel(username='testuser', password='testpassword')

        assert user is not None
        assert user.username == 'testuser'
        assert user.password == 'testpassword'
