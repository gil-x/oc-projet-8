from django.test import TestCase
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate

class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Appelée une seule fois avant tous les tests. Pour créer de la data, pas des variables.
        """
        username = 'Smith'
        password = 'password'
        email = 'smith@me.org'
        new_user = User.objects.create_user(username='Doe', email='doe@me.org')
        new_user.set_password('password')
        new_user.save()
    
    def setUp(self):
        """
        Appelée avant chaque test.
        """
        self.une_variable = "Salut !"

    def test_user_creation(self):
        username = 'Smith'
        password = 'password'
        email = 'smith@me.org'
        new_user = User.objects.create_user(username)
        new_user.set_password(password)
        new_user.email = email
        new_user.save()
        self.assertEqual(username, new_user.username)
        self.assertEqual(email, new_user.email)
        self.assertTrue(authenticate(username=new_user.username, password=password))

    # def create_url():
    #     mini = MiniURL(url="http://foo.bar", code=generer(6), pseudo="Maxime")
    #     mini.save()
    #     return mini
    
    # class MiniURLTests(TestCase):
    # def test_liste(self):
    #     """ Vérifie si une URL sauvegardée est bien affichée """

    #     mini = creer_url()
    #     reponse = self.client.get(reverse('mini_url.views.liste'))

    #     self.assertEqual(reponse.status_code, 200)
    #     self.assertContains(reponse, mini.url)
    #     self.assertQuerysetEqual(reponse.context['minis'], [repr(mini)])

    def test_hello_display(self):
        # response = self.client.get(reverse('mini_url.views.liste'))
        user_doe = User.objects.get(username='Doe')
        self.assertEqual(user_doe.username, 'Doe')

    