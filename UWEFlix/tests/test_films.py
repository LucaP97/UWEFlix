# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import status
from UWEFlix.models import *
import pytest
from django.conf import settings
from model_bakery import baker

# bad request -> 400
# unauthorised -> 401
# forbidden -> 403
# correct user & invalid data -> 400
# correct user & valid data -> 200

##### FIXTURES #####

User = get_user_model()

@pytest.fixture
def get_film(api_client):
    def do_get_film():
        return api_client.get('/uweflix/films/')
    return do_get_film

@pytest.fixture
def create_film(api_client):
    def do_create_film(data):
        return api_client.post('/uweflix/films/', data)
    return do_create_film

@pytest.fixture
def update_film(api_client):
    def do_update_film(data):
        return api_client.put('/uweflix/films/', data)
    return do_update_film

@pytest.fixture
def delete_film(api_client):
    def do_delete_film(data):
        return api_client.delete('/uweflix/films/', data)
    return do_delete_film


##### TESTS #####


# here also need to check if films exist or not

# GET FILMS
@pytest.mark.django_db
class TestGetFilm:

    def test_if_user_is_anonymous_returns_200(self, get_film):
        response = get_film()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticated_returns_200(self, authenticate, get_film):
        authenticate()

        response = get_film()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_staff_returns_200(self, authenticate, get_film):
        authenticate(is_staff=True)

        response = get_film()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_cinema_manager_returns_200(self, api_client, get_film):
        user = User.objects.create_user(username='cinema_manager', password='test_password')
        cinema_manager = CinemaManager.objects.create(user=user)
        api_client.force_authenticate(user=user)

        response = get_film()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_employee_returns_200(self, api_client, get_film):
        user = User.objects.create_user(username='employee', password='test_password')
        employee = Employee.objects.create(user=user)
        api_client.force_authenticate(user=user)

        response = get_film()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_student_returns_200(self, api_client, get_film):
        user = User.objects.create_user(username='student', password='test_password')
        student = Student.objects.create(user=user)
        api_client.force_authenticate(user=user)

        response = get_film()

        assert response.status_code == status.HTTP_200_OK



# POST FILM
valid_post_data = {
    'title': 'test_title',
    'age_rating': 18,
    'duration': 120.20,
    'short_trailer_description': 'test_description',
    }

invalid_post_data = {
    'title': 1,
    'age_rating': '18',
    'duration': '120.20',
    # 'short_trailer_description': 5,
}

@pytest.mark.django_db
class TestPostFilm:
    def test_if_user_is_anonymous_returns_401(self, create_film):
        response = create_film(valid_post_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_403(self, api_client, create_film):
        api_client.force_authenticate(user={})

        response = create_film(valid_post_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_cinema_manager_returns_201(self, api_client, create_film):
        user = User.objects.create_user(username='cinema_manager', password='test_password')
        cinema_manager = CinemaManager.objects.create(user=user)

        api_client.force_authenticate(user=user)

        response = create_film(valid_post_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_cinema_manager_bad_request_returns_400(self, api_client, create_film):
        user = User.objects.create_user(username='cinema_manager', password='test_password')
        cinema_manager = CinemaManager.objects.create(user=user)

        api_client.force_authenticate(user=user)

        response = create_film(invalid_post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_employee_returns_403(self, api_client, create_film):
        user = User.objects.create_user(username='employee', password='test_password')
        employee = Employee.objects.create(user=user)

        api_client.force_authenticate(user=user)

        response = create_film(valid_post_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_student_returns_403(self, api_client, create_film):
        user = User.objects.create_user(username='student', password='test_password')
        student = Student.objects.create(user=user)

        api_client.force_authenticate(user=user)

        response = create_film(valid_post_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


# PUT FILM
# @pytest.mark.django_db
# class TestPutFilm:
#     def test_if_user_is_anonymous_returns_401(self, api_client):
#         response = api_client.put('/uweflix/films/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_if_user_is_authenticated_returns_403(self, api_client):
#         api_client.force_authenticate(user={})

#         response = api_client.post('/uweflix/films/')

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_if_user_is_cinema_manager_returns_201(self, api_client):
#         user = User.objects.create_user(username='cinema_manager', password='test_password')
#         cinema_manager = CinemaManager.objects.create(user=user)
#         data = {
#             'title': 'test_title',
#             'age_rating': 18,
#             'duration': 120.20,
#             'short_trailer_description': 'test_description',
#         }

#         api_client.force_authenticate(user=user)

#         response = api_client.post('/uweflix/films/', data=data)
#         assert response.status_code == status.HTTP_201_CREATED

#     def test_if_user_is_cinema_manager_bad_request_returns_400(self, api_client):
#         user = User.objects.create_user(username='cinema_manager', password='test_password')
#         cinema_manager = CinemaManager.objects.create(user=user)
#         data = {
#             'title': 1,
#             'age_rating': '18',
#             'duration': '120.20',
#             # 'short_trailer_description': 5,
#         }

#         api_client.force_authenticate(user=user)

#         response = api_client.post('/uweflix/films/', data=data)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_if_user_is_employee_returns_403(self, api_client):
#         user = User.objects.create_user(username='employee', password='test_password')
#         employee = Employee.objects.create(user=user)

#         api_client.force_authenticate(user=user)

#         response = api_client.post('/uweflix/films/')
#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_if_user_is_student_returns_403(self, api_client):
#         user = User.objects.create_user(username='student', password='test_password')
#         student = Student.objects.create(user=user)

#         api_client.force_authenticate(user=user)

#         response = api_client.post('/uweflix/films/')
#         assert response.status_code == status.HTTP_403_FORBIDDEN

# # DELETE FILM
# @pytest.mark.django_db
# class TestDeleteFilm:

