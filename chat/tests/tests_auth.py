import base64, json
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from chat.models import Group


PASSWORD = "Test@123!"

def create_user(username='testuser', password=PASSWORD): # new
    return get_user_model().objects.create_user(
        username = username,
        email = 'user@test.com',
        password = password
    )


def create_admin_user(username='user@admin.com', password=PASSWORD): # new
    return get_user_model().objects.create_superuser(
        username = username,
        email = 'user@admin.com',
        password = password
    )

def create_group(admin, name='testgroup'): # new
    return Group.objects.create(
        name = name,
        admin = admin
    )

class AuthenticationTest(APITestCase):
    def test_user_signup_admin(self):
        admin_user = create_admin_user()
        token = RefreshToken.for_user(admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.post(reverse('chat:signup'),
            data ={
                'username' : 'testuser',
                'email' : 'user@test.com',
                'password1' : PASSWORD,
                'password2' : PASSWORD,
            }
        )
        user = get_user_model().objects.all()[1]
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], str(user.id))
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)

    def test_user_signup_normal(self):
        _user = create_user()
        token = RefreshToken.for_user(_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.post(reverse('chat:signup'),
            data ={
                'username' : 'testuser',
                'email' : 'user@test.com',
                'password1' : PASSWORD,
                'password2' : PASSWORD,
            }
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(reverse('chat:login'), data={
            'username': user.username,
            'password': PASSWORD,
        })

        # Parse payload data from access token.
        access = response.data['access']
        header, payload, signature = access.split('.')
        decoded_payload = base64.b64decode(f'{payload}==')
        payload_data = json.loads(decoded_payload)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data['refresh'])
        self.assertEqual(payload_data['user_id'], str(user.id))
        self.assertEqual(payload_data['username'], user.username)
        self.assertEqual(payload_data['email'], user.email)

    def test_users_list(self):
        user = create_user()
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.get(reverse('chat:users-list'))
        assert response.status_code == 200

    def test_search_user(self):
        user = create_user()
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.get(reverse('chat:users-list') + 
        '?search=testuser')
        assert response.status_code == 200

    def test_detail_user(self):
        user = create_user()
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.get(reverse('chat:users-detail', args = (user.id,)))
        print(response.status_code)
        assert response.status_code == 200


class GroupTest(APITestCase):
    def test_group_create(self):
        user = create_user()
        user2 = create_user(username='test2')
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.post(reverse('chat:group-list'), data={
            'name': 'testgroup',
            'members': [f'{user2.id}']
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('testgroup',response.data['name'])
        self.assertEqual(user.id,response.data['admin'])
    
    def test_group_list(self):
        user = create_user()
        token = RefreshToken.for_user(user)
        # grp1 = create_group(admin=user)
        # grp2 = create_group(name='testgroup2', admin=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.get(reverse('chat:group-list'))
        assert response.status_code == 200

    def test_search_group(self):
        user = create_user()
        token = RefreshToken.for_user(user)
        grp1 = create_group(admin=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.get(reverse('chat:group-list') + 
        '?search=testgroup')
        assert response.status_code == 200