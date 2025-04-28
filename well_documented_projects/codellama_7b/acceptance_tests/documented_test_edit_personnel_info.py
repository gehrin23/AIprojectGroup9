Here is the solution to the problem:
```
class EditUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@example.com', password='123456')
        self.client.force_login(self.user)
    
    # Test case for editing user info
    def test_edit_user(self):
        response = self.client.get('/users/edit/john')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit.html')
        
        # Test case for updating user info
        response = self.client.post('/users/edit/john', {'username': 'jane', 'email': 'jane@example.com', 'password': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit.html')
```
In this test case, we first log in as the user and then test that the edit user view is rendered correctly when we visit the `/users/edit/john` URL. We also test that the `POST` request to update the user's information returns a successful response.

We use the `client.force_login()` method to log in as the user before making the GET and POST requests, which allows us to access the edit user view without being redirected to the login page.

Note that we use the `assertTemplateUsed()` method to check that the correct template is used when rendering the response. This ensures that the correct template is rendered for both the GET and POST requests.