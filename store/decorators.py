from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('@example.com')