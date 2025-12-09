from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')  # Make sure the URL is named
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class NotesApiTests(APITestCase):
    def test_crud_flow(self):
        # Create
        create_resp = self.client.post('/api/notes/', {"title": "First", "content": "Hello"}, format='json')
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        note_id = create_resp.data["id"]

        # Retrieve detail
        detail_resp = self.client.get(f'/api/notes/{note_id}/')
        self.assertEqual(detail_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_resp.data["title"], "First")

        # Update
        update_resp = self.client.put(f'/api/notes/{note_id}/', {"title": "Updated", "content": "World"}, format='json')
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(update_resp.data["title"], "Updated")

        # Partial update
        patch_resp = self.client.patch(f'/api/notes/{note_id}/', {"content": "Patched"}, format='json')
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_resp.data["content"], "Patched")

        # List with pagination
        list_resp = self.client.get('/api/notes/?page=1&page_size=10')
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertIn("results", list_resp.data)

        # Search by title
        search_resp = self.client.get('/api/notes/?search=Upd')
        self.assertEqual(search_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(search_resp.data.get("count", 0), 1)

        # Delete
        delete_resp = self.client.delete(f'/api/notes/{note_id}/')
        self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)
