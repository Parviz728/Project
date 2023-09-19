from fastapi.testclient import TestClient
from app.app import app
from app.auth import Auth
from unittest import TestCase
from unittest.mock import patch
from app.user import User

auth = Auth

client = TestClient(app)

class TestApp(TestCase):
    @patch("auth.get_user")
    @patch("auth.authenticate_user")
    def test_get_and_authenticate_user(self, mock_get_data, mock_authenticate_data):
        # то что вернет поддельная функция auth.get_user
        mock_response = User("user1", "user_pass_1")
        mock_get_data.return_value = mock_response

        # то что должна вернуть auth.authenticate_user
        mock_authenticated_response = True
        mock_authenticate_data.return_value = mock_authenticated_response

        ans = {"access_token": "access_token", "token_type": "bearer"}

        response = client.post('/signin')

        mock_authenticate_data.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ans)