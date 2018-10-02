from django.test import TestCase
from .models import Product

class ProductTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Appelée une seule fois avant tous les tests. Pour créer de la data, pas des variables.
        """
        # username = 'Smith'
        # password = 'password'
        # email = 'smith@me.org'
        # new_user = User.objects.create_user(username='Doe', email='doe@me.org')
        # new_user.set_password('password')
        # new_user.save()
        pass
    
    def setUp(self):
        """
        Appelée avant chaque test.
        """
        # self.une_variable = "Salut !"
        pass
