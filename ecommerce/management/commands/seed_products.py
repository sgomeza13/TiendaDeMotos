from django.core.management.base import BaseCommand 

from ecommerce.factories import ProductFactory 

 

class Command(BaseCommand): 

    help = 'Seed the database with products' 

    def handle(self, *args, **kwargs): 
        ProductFactory.create_batch(12) 
        self.stdout.write(self.style.SUCCESS('Successfully seeded products')) 
