import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your token here.
class UserActivationTokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email)
        ) 
user_activation_token = UserActivationTokenGenerator()
