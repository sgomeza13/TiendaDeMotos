import factory 

from .models import Product 

 

class ProductFactory(factory.django.DjangoModelFactory): 
    class Meta: 
        model = Product 

    name = factory.Faker('sentence', nb_words=3, variable_nb_words=True, ext_word_list=None)
    price = factory.Faker('random_int', min=20, max=9000)
    brand =  factory.Faker('sentence', nb_words=3, variable_nb_words=True, ext_word_list=None)
    reference = factory.Faker('zipcode')
    stock = factory.Faker('random_int', min=10, max=100)