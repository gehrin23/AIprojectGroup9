The test cases for the UpdateUserInformation class are as follows:
     
     # Test case 1: Test valid user information update
     
     def test_update_user_information(self):
         self.client.force_login(self.admin_user)
         response = self.client.post(
             reverse('admin:core_customuser_change', args=[self.user.id]),
             {
                 'email': 'updated@example.com',
                 'password': 'password123',
                 'first_name': 'Updated',
                 'last_name': 'User',
                 'is_active': True,
                 'role': 'Admin'
             }
         )
         self.assertEqual(response.status_code, 302)
         self.user.refresh_from_db()
         self.assertEqual(self.user.email, 'updated@example.com')
         self.assertTrue(self.user.check_password('password123'))
         self.assertEqual(self.user.first_name, 'Updated')
         self.assertEqual(self.user.last_name, 'User')
     
     # Test case 2: Test invalid user information update
     
     def test_update_user_information(self):
         self.client.force_login(self.admin_user)
         response = self.client.post(
             reverse('admin:core_customuser_change', args=[self.user.id]),
             {
                 'email': '',
                 'password': 'password123',
                 'first_name': 'Updated',
                 'last_name': 'User',
                 'is_active': True,
                 'role': 'Admin'
             }
         )
         self.assertEqual(response.status_code, 302)
         self.user.refresh_from_db()
         self.assertEqual(self.user.email, '')
         self.assertTrue(self.user.check_password('password123'))
         self.assertEqual(self.user.first_name, 'Updated')
         self.assertEqual(self.user.last_name, 'User')
     
     # Test case 3: Test updating user information without change password
     
     def test_update_user_information(self):
         self.client.force_login(self.admin_user)
         response = self.client.post(
             reverse('admin:core_customuser_change', args=[self.user.id]),
             {
                 'email': 'updated@example.com',
                 'password': '',
                 'first_name': 'Updated',
                 'last_name': 'User',
                 'is_active': True,
                 'role': 'Admin'
             }
         )
         self.assertEqual(response.status_code, 302)
         self.user.refresh_from_db()
         self.assertEqual(self.user.email, 'updated@example.com')
         self.assertFalse(self.user.check_password('password123'))
         self.assertEqual(self.user.first_name, 'Updated')
         self.assertEqual(self.user.last_name, 'User')