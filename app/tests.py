from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Post


def get_or_create_user1():
    user, _ = User.objects.get_or_create(username="misagh", password="misagh", email="misagh@misagh.com")
    return user


def get_or_create_user2():
    user, _ = User.objects.get_or_create(username="misagh2", password="misagh2", email="misagh2@misagh.com")
    return user


def create_post():
    post = Post.objects.create(title="test", content="test")
    return post


def login_as_user(client, user):
    # Initialize client and force it to use authentication
    client.force_authenticate(user=user)


class PostRatingTests(APITestCase):

    def setUp(self):
        user = get_or_create_user1()
        login_as_user(self.client, user)

    def test_rate_to_a_post_by_one_same_user(self):
        """
        Test that the first rate of a user should be created and the second time the previous rate should become updated.

        1. Creates a post.
        2. Gets the URL for rating a post.
        3. Defines the rating data.
        4. Sends a POST request to rate the post.
        5. Checks that the response status code is 200 OK.
        6. Refreshes the post object from the database.
        7. Checks that the post's average rating is equal to the rate value.
        8. Checks that the post's rating count is 1.
        9. Performs the same operations for a second time, rating by the same user on the same post.
        """
        # Create a post
        post1 = create_post()

        # Get the URL for rating a post
        url = reverse('post-rate', kwargs={'post_id': post1.id})

        # Define the rating data
        data = {"rate": 2}

        # Send a POST request to rate the post
        response = self.client.post(url, data, format='json')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the post object from the database
        post1.refresh_from_db()

        # Check that the post's average rating is equal to the rate value
        self.assertEqual(post1.rating_avg, data['rate'])

        # Check that the post's rating count is 1
        self.assertEqual(post1.rating_count, 1)

        # --------------------------------------------------------------------------
        # second time rating by a same user on same post
        response = self.client.post(url, data, format='json')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the post object from the database
        post1.refresh_from_db()

        # Check that the post's average rating is equal to the rate value
        self.assertEqual(post1.rating_avg, data['rate'])

        # Check that the post's rating count is 1
        self.assertEqual(post1.rating_count, 1)

    def test_rate_to_a_post_by_multi_users(self):
        """
        Test the functionality of rating a post by multiple users.

        This function performs the following steps:

        1. Creates a post.
        2. Retrieves the URL for rating a post.
        3. Defines the rating data.
        4. Sends a POST request to rate the post.
        5. Checks that the response status code is 200 OK.
        6. Refreshes the post object from the database.
        7. Checks that the post's average rating is equal to the rate value.
        8. Checks that the post's rating count is 1.

        Then, it performs the following steps:

        1. Creates a second user.
        2. Logs in as the second user.
        3. Defines the rating data.
        4. Sends a POST request to rate the post.
        5. Checks that the response status code is 200 OK.
        6. Refreshes the post object from the database.
        7. Checks that the post's average rating is equal to the rate value (new average).
        8. Checks that the post's rating count is 2.
        """
        # Create a post
        post1 = create_post()

        # Get the URL for rating a post
        url = reverse('post-rate', kwargs={'post_id': post1.id})

        # Define the rating data
        data = {"rate": 2}

        # Send a POST request to rate the post
        response = self.client.post(url, data, format='json')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the post object from the database
        post1.refresh_from_db()

        # Check that the post's average rating is equal to the rate value
        self.assertEqual(post1.rating_avg, data['rate'])

        # Check that the post's rating count is 1
        self.assertEqual(post1.rating_count, 1)

        # --------------------------------------------------------------------------
        # Second time rating by another user on the same post

        user = get_or_create_user2()
        login_as_user(self.client, user)

        # Define the rating data
        data = {"rate": 4}

        response = self.client.post(url, data, format='json')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the post object from the database
        post1.refresh_from_db()

        # Check that the post's average rating is equal to the rate value
        self.assertEqual(post1.rating_avg, 3)

        # Check that the post's rating count is 2
        self.assertEqual(post1.rating_count, 2)
