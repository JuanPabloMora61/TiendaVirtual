from django.test import TestCase

from shop.models import Category, Product

class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name = 'Test Category')
        Product.objects.create(name= 'Test Product', description= 'Test description', price=100, category=Category.objects.get(name= 'Test Category'))
        Product.objects.create(name= 'Test Product 2', description= 'Test description', price=200, category=Category.objects.get(name= 'Test Category'))

    def test_product_category_id(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.category.id, 1)

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'Categoría: {category.name}'
        self.assertEqual(expected_object_name, str(category))

    def  test_objects_count(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.products.count(), 2)

class ProductModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name = 'Test Category')
        Product.objects.create(name='Test Product 1', description='Test description', price=100, category=category)
        Product.objects.create(name='Test Product 2', description='Test description', price=200, category=category)
        Product.objects.create(name='Test Product 3', description='Test description', price=300, category=category)
   
    def test_product_list_view_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_query_list(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['object_list']), 3)

    def test_product_template(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1>Productos</h1>')