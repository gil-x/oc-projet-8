from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import AnonymousUser, User
from .models import Profile
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from .views import add_to_favorites, remove_from_favorites


class ProfileTests(TestCase):
    def setUp(self):
        """
        Appelée une seule fois avant tous les tests. Pour créer de la data, pas des variables.
        """
        username = 'jdoe'
        password = 'password'
        email = 'jdoe@me.org'
        new_user = User.objects.create_user(username='doe', email='jdoe@me.org')
        new_user.set_password('password')
        new_user.save()
        new_profile = Profile()
        new_profile.user = new_user
        new_profile.save()
        self.factory = RequestFactory()
        self.user = new_user
   
    def test_user_creation(self):
        """
        Test new user creation.
        """
        username = 'Smith'
        password = 'password'
        email = 'smith@me.org'
        new_user = User.objects.create_user(username)
        new_user.set_password(password)
        new_user.email = email
        new_user.save()
        new_profile = Profile()
        new_profile.user = new_user
        new_profile.save()
        self.assertEqual(username, new_user.username)
        self.assertEqual(email, new_user.email)
        self.assertTrue(authenticate(username=new_user.username, password=password))

    def test_connexion_view(self):
        """
        Test the Connection page code response.
        """
        c = Client()
        response = c.get('/connexion/')
        self.assertEqual(response.status_code, 200)

    def test_add_to_favorites_user_anonymous(self):
        request = self.factory.get('/mon-espace/add-product/1/')
        request.user = AnonymousUser()
        response = add_to_favorites(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_add_to_favorites_user_authenticated(self):
        request = self.factory.get('/mon-espace/add-product/1/')
        request.user = self.user
        response = add_to_favorites(request, 1)
        self.assertEqual(response.status_code, 200)
    
    def test_remove_from_favorites_user_anonymous(self):
        request = self.factory.get('/mon-espace/add-product/1/')
        request.user = AnonymousUser()
        response = remove_from_favorites(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_remove_from_favorites_user_authenticated(self):
        request = self.factory.get('/mon-espace/remove-product/1/')
        request.user = self.user
        response = remove_from_favorites(request, 1)
        self.assertEqual(response.status_code, 200)


    