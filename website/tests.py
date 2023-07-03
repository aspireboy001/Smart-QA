# from django.test import TestCase
# from django.conf import settings
# from .settings import SECRET_KEY 
# import re
# #
# class SecretKeyTestCase(TestCase):
    
#     def test_secret_key_strength_and_validity(self):
#         # Define the regular expression pattern for a valid secret key
#         pattern = r'^[a-zA-Z0-9!@#$%^&*()_+\-=]{6,30}$'
        
#         secret_key = SECRET_KEY 
        
#         # Check if the secret key is valid
#         self.assertTrue(re.match(pattern, secret_key), msg="Secret key is not valid!")
        
#         # Check the strength of the secret key
#         score = 0
#         if any(c.isupper() for c in secret_key):
#             score += 1
#         if any(c.islower() for c in secret_key):
#             score += 1
#         if any(c.isdigit() for c in secret_key):
#             score += 1
#         if any(c in '!@#$%^&*()_+\-=' for c in secret_key):
#             score += 1
        
#         self.assertEqual(score, 4, msg="Secret key is weak!")
