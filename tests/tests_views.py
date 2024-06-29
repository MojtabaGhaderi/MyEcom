import io
from datetime import timedelta
from unittest.mock import patch

from django.test import Client, TestCase
from django.utils.text import slugify
from rest_framework.permissions import BasePermission
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from Backstore.models import CategoryModel, ProductModel, TagsModel, ProductImage, ProductComment, DiscountCodeModel, \
    NotificationModel
from OrderManagement.models import OrdersModel
from PayManagement.models import InvoiceModel, InvoiceItemModel
from ShoppingCart.models import ShoppingCartModel
from UserManagement.models import UserManageModel, AdminModel

from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile


def user_create():
    user = UserManageModel.objects.create_user(
        username='testuser', password='testpassword', email='testmail@example.com'
    )
    return user


class MockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True

    # #// UserManagement app:
    #
    #
    # class TestUserRegistrationView(TestCase):
    #     def setUp(self):
    #         self.client = APIClient()
    #
    #     def test_user_registration(self):
    #         url = reverse('registration')
    #         data = {
    #             'username': 'testuser',
    #             'email': 'testuser@example.com',
    #             'password': 'testpassword',
    #             'password2': 'testpassword',
    #         }
    #
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #         self.assertEqual(UserManageModel.objects.count(), 1)
    #         user = UserManageModel.objects.first()
    #         self.assertEqual(user.username, 'testuser')
    #         self.assertEqual(user.email, 'testuser@example.com')
    #
    #     def test_user_registration_with_missing_data(self):
    #         url = reverse('registration')
    #         data = {
    #             'username': 'testuser',
    #             'email': 'testuser@example.com',
    #         }
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #         self.assertEqual(UserManageModel.objects.count(), 0)
    #
    #     def test_user_registration_with_password_mismatch(self):
    #         url = reverse('registration')
    #         data = {
    #             'username': 'testuser',
    #             'email': 'testuser@example.com',
    #             'password': 'testpassword',
    #             'password2': 'wrongpassword',
    #         }
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #         self.assertEqual(UserManageModel.objects.count(), 0)
    #
    #
    # class TestUserLoginView(TestCase):
    #     def setUp(self):
    #         self.user = user_create()
    #
    #     def tearDown(self):
    #         self.user.delete()
    #
    #     def test_username_does_not_exist(self):
    #         url = reverse('login')
    #         data = {'username': 'nottestuser1',
    #                 'password': 'testpassword'
    #                 }
    #
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #         self.assertEqual(UserManageModel.objects.count(), 1)
    #
    #     def test_wrong_password(self):
    #         url = reverse('login')
    #         data = {'username': 'testuser',
    #                 'password': 'wrongpassword'
    #                 }
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #     def test_successful_login(self):
    #         url = reverse('login')
    #         data = {'username': 'testuser',
    #                 'password': 'testpassword'
    #                 }
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #
    # class TestUserProfileView(TestCase):
    #
    #     def setUp(self):
    #         self.user = user_create()
    #         self.client = APIClient()
    #         self.client.force_authenticate(user=self.user)
    #
    #     def tearDown(self):
    #         self.user.delete()
    #
    #     def test_get_user_profile(self):
    #         url = reverse('profile')
    #
    #         with patch('UserManagement.views.UserProfileView.permission_classes', [MockPermission]):
    #             response = self.client.get(url)
    #
    #             self.assertEqual(response.status_code, status.HTTP_200_OK)
    #             self.assertEqual(response.data['username'], self.user.username)
    #             self.assertEqual(response.data['email'], self.user.email)
    #             self.assertEqual(response.data['address'], self.user.address)
    #             self.assertEqual(response.data['phone_number'], self.user.phone_number)
    #
    #     def test_update_user_profile(self):
    #         url = reverse('profile')
    #         data = {
    #             'username': 'newtestusername',
    #             'email': 'newtestmail@gmail.com',
    #             'address': 'new test address',
    #             'phone_number': '12345678901',
    #         }
    #
    #         with patch('UserManagement.views.UserProfileView.permission_classes', [MockPermission]):
    #             response = self.client.put(url, data, format='json')
    #             self.assertEqual(response.status_code, status.HTTP_200_OK)
    #             self.user.refresh_from_db()
    #             self.assertEqual(self.user.username, 'newtestusername')
    #             self.assertEqual(self.user.email, 'newtestmail@gmail.com')
    #             self.assertEqual(self.user.address, 'new test address')
    #             self.assertEqual(self.user.phone_number, '12345678901')
    #
    #
    # # // BackStore app:
    #
    #
    # class TestCategoryCreateView(TestCase):
    #     def setUp(self):
    #         self.client = APIClient()
    #         self.user = user_create()
    #         self.client.force_authenticate(user=self.user)
    #
    #     def tearDown(self):
    #         self.client.logout()
    #         CategoryModel.objects.all().delete()
    #         self.user.delete()
    #
    #     def test_category_create(self):
    #         url = reverse('category-create')
    #         data = {
    #             'name': 'testcategory',
    #         }
    #
    #         with patch('Backstore.views.CategoryCreateView.permission_classes', [MockPermission]):
    #             response = self.client.post(url, data, format='json')
    #
    #             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #             self.assertEqual(CategoryModel.objects.count(), 1)
    #             self.assertEqual(CategoryModel.objects.first().name, 'testcategory')
    #             self.assertEqual(CategoryModel.objects.first().parent.count(), 0)

    #
    #     def test_category_without_permission(self):
    #         url = reverse('category-create')
    #         data = {
    #             'name': 'testcategory'
    #         }
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #
    # class TestCategoryEditView(TestCase):
    #
    #     def setUp(self):
    #         self.client = APIClient()
    #         self.user = user_create()
    #         self.client.force_authenticate(user=self.user)
    #
    #         self.category1 = CategoryModel.objects.create(name='test-category')
    #         self.category2 = CategoryModel.objects.create(name='test-category2')
    #         self.category_child = CategoryModel.objects.create(name='test-category-child')
    #         self.category_child_of_child = CategoryModel.objects.create(name='test-category-child-of-child')
    #
    #         self.category_child.parent.add(self.category1)
    #         self.category_child_of_child.parent.add(self.category_child)
    #
    #         self.product1 = ProductModel.objects.create(name='product1', price=100)
    #         self.product2 = ProductModel.objects.create(name='product2', price=100)
    #         self.product3 = ProductModel.objects.create(name='product3', price=100)
    #         self.product4 = ProductModel.objects.create(name='product4', price=100)
    #         self.product1.category.add(self.category1)
    #         self.product2.category.add(self.category2)
    #         self.product3.category.add(self.category_child)
    #         self.product4.category.add(self.category_child_of_child)
    #
    #     def tearDown(self):
    #         self.client.logout()
    #         self.user.delete()
    #         CategoryModel.objects.all().delete()
    #
    #     def test_category_edit(self):
    #
    #         url = reverse('category-edit', args=[self.category1.pk])
    #         data = {
    #             'name': 'first-test-category'
    #         }
    #         with patch('Backstore.views.CategoryEditView.permission_classes', [MockPermission]):
    #             response = self.client.put(url, data, format='json')
    #
    #             self.assertEqual(response.status_code, status.HTTP_200_OK)
    #             self.assertEqual(CategoryModel.objects.first().name, 'first-test-category')
    #             self.assertEqual(CategoryModel.objects.count(), 4)
    #             self.assertEqual(self.category1.children.count(), 1)
    #             self.assertEqual(self.category_child.children.count(), 1)
    #
    #             self.product1.refresh_from_db()
    #             self.product2.refresh_from_db()
    #             self.product3.refresh_from_db()
    #             self.product4.refresh_from_db()
    #
    #             self.assertIn(self.category1, self.product1.category.all())
    #             self.assertIn(self.category2, self.product2.category.all())
    #             self.assertIn(self.category_child, self.product3.category.all())
    #             self.assertIn(self.category_child_of_child, self.product4.category.all())
    #
    #     def test_category_change_parent(self):
    #         url = reverse('category-edit', args=[self.category_child.pk])
    #         data = {
    #             'parent': [self.category2.pk]
    #         }
    #
    #         with patch('Backstore.views.CategoryEditView.permission_classes', [MockPermission]):
    #             response = self.client.patch(url, data, format='json')
    #             self.assertEqual(response.status_code, status.HTTP_200_OK)
    #             self.assertEqual(CategoryModel.objects.count(), 4)
    #             self.assertEqual(self.category1.children.count(), 0)
    #             self.assertEqual(self.category2.children.count(), 1)
    #             self.assertEqual(self.category_child.children.count(), 1)
    #             self.assertEqual(self.category_child_of_child.children.count(), 0)
    #
    #     def test_category_delete(self):
    #         url = reverse('category-edit', args=[self.category_child.pk])
    #
    #         with patch('Backstore.views.CategoryEditView.permission_classes', [MockPermission]):
    #             response = self.client.delete(url)
    #             self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #             self.assertEqual(CategoryModel.objects.count(), 3)
    #             self.assertEqual(self.category1.children.count(), 1)
    #             self.assertEqual(self.category2.children.count(), 0)
    #             self.assertEqual(self.category_child_of_child.children.count(), 0)
    #             self.assertEqual(self.category1.children.first(), self.category_child_of_child)
    #
    #             self.assertIn(self.category1, self.product3.category.all())
    #             self.assertIsNot(self.category_child, self.product3.category.all())
    #             self.assertIn(self.category2, self.product2.category.all())
    #             self.assertIn(self.category_child_of_child, self.product4.category.all())
    #

# class TestProductView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category1 = CategoryModel.objects.create(name='category1')
#         self.category2 = CategoryModel.objects.create(name='category2')
#         self.category3 = CategoryModel.objects.create(name='category3')
#         self.category2.parent.add(self.category1)
#         self.category3.parent.add(self.category2)
#
#         self.tags = TagsModel.objects.create(name='test-tags')
#         self.tags2 = TagsModel.objects.create(name='test-tags2')
#
#         self.product0 = ProductModel.objects.create(name='test product 0')
#         self.product0.category.set([self.category1.pk])
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#         TagsModel.objects.all().delete()

    # def test_product_create(self):
    #     url = reverse('product-create')
    #     data = {
    #         'category': [self.category1.pk],
    #         'name': 'test product1',
    #         'quantity': 10,
    #         'description': 'this is a test product',
    #         'tags': [self.tags.pk],
    #         'price': 1000,
    #         'discount': 20.25,
    #         'available': True,
    #         'special_offer': True,
    #         'recently_added': True,
    #         'immediate_delivery': True,
    #     }
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #         test_product1 = ProductModel.objects.all()[1]
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(ProductModel.objects.all().count(), 2)
    #         self.assertIn(self.category1, test_product1.category.all())
    #         self.assertEqual(test_product1.category.all().count(), 1)
    #         self.assertEqual(test_product1.name, 'test product1')
    #         self.assertEqual(test_product1.slug, 'test-product1')
    #         self.assertEqual(test_product1.quantity, 10)
    #         self.assertEqual(test_product1.description, 'this is a test product')
    #         self.assertEqual(test_product1.tags.all().first().pk, self.tags.pk)
    #         self.assertEqual(test_product1.price, 1000)
    #         self.assertEqual(test_product1.discount, 20.25)
    #         self.assertEqual(test_product1.available, True)
    #         self.assertEqual(test_product1.special_offer, True)
    #         self.assertEqual(test_product1.recently_added, True)
    #         self.assertEqual(test_product1.immediate_delivery, True)
    #
    # def test_product_create_with_multiple_tags(self):
    #     url = reverse('product-create')
    #     data = {
    #         'name': 'test product',
    #         'category': [self.category1.pk],
    #         'tags': [self.tags.pk, self.tags2.pk],
    #     }
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(ProductModel.objects.all().count(), 2)
    #
    #         test_product = ProductModel.objects.all()[1]
    #
    #         self.assertEqual(test_product.tags.all().count(), 2)
    #         self.assertIn([self.tags, self.tags2], [list(test_product.tags.all())])
    #
    # def test_missing_data(self):
    #     url = reverse('product-create')
    #     data = {
    #
    #     }
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_invalid_data(self):
    #     url = reverse('product-create')
    #     data = {
    #         'category': 'category1',
    #         'name': True,
    #         'quantity': '10',
    #         'description': True,
    #         'tags': 'self.tags2',
    #         'price': '1000',
    #         'discount': '20.25',
    #         'available': 'fine',
    #         'special_offer': 'yes',
    #         'recently_added': 'yes',
    #         'immediate_delivery': 'yes',
    #     }
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_product_create_with_non_existing_category(self):
    #     url = reverse('product-create')
    #     data = {
    #         'name': 'test product',
    #         'category': [10]
    #     }
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_create_multiple_products_at_once(self):
    #     url = reverse('product-create')
    #     data = [
    #         {
    #             'name': 'Product 1',
    #             'category': [self.category1.pk],
    #             'quantity': 10,
    #             'description': 'This is product 1',
    #             'tags': [self.tags.pk],
    #             'price': 1000,
    #             'discount': 20.25,
    #             'available': True,
    #             'special_offer': True,
    #             'recently_added': True,
    #             'immediate_delivery': True,
    #         },
    #         {
    #             'name': 'Product 2',
    #             'category': [self.category2.pk],
    #             'quantity': 20,
    #             'description': 'This is product 2',
    #             'tags': [self.tags.pk],
    #             'price': 1500,
    #             'discount': 15.75,
    #             'available': False,
    #             'special_offer': False,
    #             'recently_added': False,
    #             'immediate_delivery': False,
    #         },
    #     ]
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(len(response.data), 2)
    #         self.assertEqual(ProductModel.objects.all().count(), 3)
    #
    # def test_create_multiple_products_at_once_with_one_missing_data_for_one_of_them(self):
    #     url = reverse('product-create')
    #     data = [
    #         {
    #             'name': 'Product 1',
    #             'category': [self.category1.pk],
    #             'quantity': 10,
    #             'description': 'This is product 1',
    #             'tags': [self.tags.pk],
    #             'price': 1000,
    #             'discount': 20.25,
    #             'available': True,
    #             'special_offer': True,
    #             'recently_added': True,
    #             'immediate_delivery': True,
    #         },
    #         {
    #             'name': 'Product 2',
    #
    #         },
    #         {
    #             'name': 'Product 3',
    #             'category': 10,
    #
    #         },
    #     ]
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='json')
    #
    #         self.assertEqual(response.status_code, status.HTTP_207_MULTI_STATUS)
    #         self.assertEqual(len(response.data), 2)
    #         self.assertEqual(ProductModel.objects.all().count(), 2)
    #         self.assertEqual(len(response.data[0]), 2)
    #
    # def test_create_product_with_images(self):
    #     url = reverse('product-create')
    #
    #     image_data = b'image_data'
    #     image_file = InMemoryUploadedFile(
    #         file=io.BytesIO(image_data),
    #         field_name='image',
    #         name='test_image.jpg',
    #         content_type='image/jpeg',
    #         size=len(image_data),
    #         charset=None,
    #     )
    #
    #     data = {
    #         'name': "test product with image",
    #         'category': [self.category3.pk],
    #         'images': [
    #             {'image': image_file},
    #         ]
    #     }
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.post(url, data, format='multipart')
    #         print('response content:', response.content)
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(ProductModel.objects.count(), 2)
    #
    #         created_product = ProductModel.objects.get(pk=response.data['id'])
    #         self.assertEqual(created_product.name, 'test product with image')
    #
    #         self.assertEqual(ProductImage.objects.count(), 1)
    #         created_image = ProductImage.objects.get(product=created_product)
    #         self.assertEqual(created_image.alt_text, 'Test image')
    #         self.assertEqual(created_image.image.read(), image_data)

    # def test_product_list(self):
    #     url = reverse('product-list')
    #     test_product = ProductModel.objects.create(name='test product')
    #     test_product.category.set([self.category2.pk])
    #     test_product = ProductModel.objects.create(name='test product3')
    #     test_product.category.set([self.category2.pk])
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.get(url)
    #         print(response.data)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(len(response.data), 3)

    # def test_product_retrieve(self):
    #     url = reverse('product-detail', kwargs={'slug': 'test-product-0'})
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.get(url)
    #
    #     self.assertEqual(ProductModel.objects.all().count(), 1)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'test product 0')
    #     self.assertEqual(response.data['category'], [self.category1.pk])
    #
    # def test_retrieving_not_existing_product(self):
    #     url = reverse('product-detail', kwargs={'slug': 'not-existing-product'})
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_retrieve_product_with_special_characters_in_slug(self):
    #     special_slug = 'product-with-special characters-#$% تست'
    #     special_slug_product = ProductModel.objects.create(name=special_slug)
    #     special_slug_product.category.set([self.category1.pk])
    #
    #     url = reverse('product-detail', kwargs={'slug': slugify(special_slug)})
    #     print(slugify(special_slug))
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.get(url)
    #
    #     self.assertEqual(ProductModel.objects.all().count(), 2)
    #     self.assertEqual(ProductModel.objects.get(name=special_slug), special_slug_product)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_product_partial_update(self):
    #     url = reverse('product-update', kwargs={'slug': 'test-product-0'})
    #
    #     data = {
    #         'quantity': 10,
    #         'category': [self.category1.pk, self.category2.pk],
    #         'tags': [self.tags.pk]
    #     }
    #
    #     self.assertEqual(self.product0.quantity, 1)
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.patch(url, data=data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.product0.refresh_from_db()
    #     self.assertEqual(self.product0.quantity, 10)
    #     self.assertEqual(self.product0.category.count(), 2)
    #     self.assertIn(self.category1, self.product0.category.all())
    #     self.assertIn(self.category2, self.product0.category.all())
    #     self.assertEqual(self.product0.tags.count(), 1)
    #     self.assertIn(self.tags, self.product0.tags.all())
    #
    # def test_product_update(self):
    #     url = reverse('product-update', kwargs={'slug': 'test-product-0'})
    #
    #     data = {
    #         'name': 'test product update',
    #         'quantity': 10,
    #         'category': [self.category1.pk, self.category2.pk],
    #         'tags': [self.tags.pk, self.tags2.pk]
    #     }
    #
    #     self.assertEqual(self.product0.quantity, 1)
    #
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.put(url, data=data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.product0.refresh_from_db()
    #     self.assertEqual(self.product0.name, 'test product update')
    #     self.assertEqual(self.product0.quantity, 10)
    #     self.assertEqual(self.product0.category.count(), 2)
    #     self.assertIn(self.category1, self.product0.category.all())
    #     self.assertIn(self.category2, self.product0.category.all())
    #     self.assertEqual(self.product0.tags.count(), 2)
    #     self.assertIn(self.tags, self.product0.tags.all())
    #     self.assertIn(self.tags2, self.product0.tags.all())

    # def test_product_destroy(self):
    #     url = reverse('product-delete', kwargs={'slug': 'test-product-0'})
    #
    #     self.assertEqual(ProductModel.objects.all().count(), 1)
    #     with patch('Backstore.views.ProductView.permission_classes', [MockPermission]):
    #         response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(ProductModel.objects.all().count(), 0)


# class TestProductCommentDeleteView(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category = CategoryModel.objects.create(name='category')
#         self.product = ProductModel.objects.create(name='test product for delete comment')
#         self.product.category.set([self.category.pk])
#         self.comment = ProductComment.objects.create(comment="guess where is me? I'm on thi ocean antrtaka!",
#                                                      product=self.product, user=self.user)
#
#     def tearDown(self):
#         self.client.logout()
#         ProductComment.objects.all().delete()
#         self.user.delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#
#     def test_product_comment_delete(self):
#         url = reverse('comment-delete', kwargs={'pk': f'{self.comment.pk}'})
#         self.assertEqual(self.product.comment.all().count(), 1)
#         self.assertEqual(self.user.user_comment.all().count(), 1)
#         with patch('Backstore.views.ProductCommentDelete.permission_classes', [MockPermission]):
#             response = self.client.delete(url)
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(ProductComment.objects.count(), 0)
#         self.assertEqual(self.product.comment.all().count(), 0)
#         self.assertEqual(self.user.user_comment.all().count(), 0)
#
#     def test_product_comment_with_no_authority(self):
#         url = reverse('comment-delete', kwargs={'pk': f'{self.comment.pk}'})
#
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class TestProductBatchUpdateView(TestCase):
#
#     def setUp(self):
#
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category1 = CategoryModel.objects.create(name='test-category')
#         self.category2 = CategoryModel.objects.create(name='test-category2')
#
#         self.tag1 = TagsModel.objects.create(name='tag1')
#         self.tag2 = TagsModel.objects.create(name='tag2')
#
#         self.product1 = ProductModel.objects.create(name='product1', price=100)
#         self.product2 = ProductModel.objects.create(name='product2', price=200)
#         self.product3 = ProductModel.objects.create(name='product3', price=300, discount=30, special_offer=True)
#         self.product4 = ProductModel.objects.create(name='product4', price=400, discount=40, special_offer=True)
#
#         self.product1.category.add(self.category1)
#         self.product1.tags.add(self.tag1)
#         self.product2.category.add(self.category1)
#         self.product2.tags.add(self.tag1)
#         self.product3.category.add(self.category2)
#         self.product3.tags.add(self.tag2)
#         self.product4.category.add(self.category2)
#         self.product4.tags.add(self.tag2)
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#         TagsModel.objects.all().delete()
#
#     def test_product_batch_update(self):
#         url = reverse('product-discount-special')
#         data = [
#             {
#                 'id': self.product1.pk,
#                 'special_offer': True,
#                 'discount': 10,
#                 'tags': [self.tag2.pk],
#                 'category': [self.category2.pk],
#                 },
#             {
#                 'id': self.product2.pk,
#                 'special_offer': True,
#                 'discount': 20,
#                 'tags': [self.tag2.pk],
#                 'category': [self.category2.pk],
#                 },
#             {
#                 'id': self.product3.pk,
#                 'special_offer': False,
#                 'discount': 0,
#                 'tags': [self.tag2.pk],
#                 'category': [self.category1.pk],
#                 },
#             {
#                 'id': self.product4.pk,
#                 'special_offer': False,
#                 'discount': 0,
#                 'tags': [self.tag1.pk],
#                 'category': [self.category1.pk],
#                 },
#         ]
#
#         with patch('Backstore.views.ProductBatchUpdateView.permission_classes', [MockPermission]):
#             response = self.client.put(url, data, format='json')
#
#         print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         self.product1.refresh_from_db()
#         self.product2.refresh_from_db()
#         self.product3.refresh_from_db()
#         self.product4.refresh_from_db()
#
#         self.assertEqual(ProductModel.objects.all().count(), 4)
#         self.assertTrue(self.product1.special_offer)
#         self.assertEqual(self.product1.discount, 10)
#         self.assertIn(self.tag2, self.product1.tags.all())
#         self.assertIn(self.category2, self.product1.category.all())
#
#         self.assertTrue(self.product2.special_offer)
#         self.assertFalse(self.product3.special_offer)
#         self.assertFalse(self.product4.special_offer)
#
#     def test_batch_update_with_at_least_one_invalid_data(self):
#         pass
    # I want the update to be successful for the products with correct data.

# class TestUserRelatedViews(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.user2 = UserManageModel.objects.create_user(
#             username='testuser2', password='testpassword2', email='testmail2@example.com'
#         )
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         self.user2.delete()
#
#     def test_user_list(self):
#         url = reverse('user-list')
#
#         with patch('Backstore.views.UserListView.permission_classes', [MockPermission]):
#             response = self.client.get(url)
#
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.assertEqual(len(response.data), 2)
#
#     def test_user_retrieve(self):
#         url = reverse('user-retrieve', kwargs={'pk': f'{self.user.pk}'})
#
#         with patch('Backstore.views.UserRetrieveView.permission_classes', [MockPermission]):
#             response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_retrieve_non_existing_user_retrieve(self):
#         url = reverse('user-retrieve', kwargs={'pk': '1024'})
#
#         with patch('Backstore.views.UserRetrieveView.permission_classes', [MockPermission]):
#             response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class TestDiscountCodeCreate(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#         AdminModel.objects.create(user=self.user, role='regular_admin')
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         AdminModel.objects.all().delete()
#         DiscountCodeModel.objects.all().delete()
#
#     def test_discount_code_create(self):
#
#         url = reverse('discount-code-create')
#         data = {
#             'discount_code': 'test-discount',
#             'percentage': 25.50,
#             'quantity': 10,
#
#         }
#
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(DiscountCodeModel.objects.all().count(), 1)
#
#     def test_discount_code_create_with_invalid_data(self):
#         url = reverse('discount-code-create')
#         data = {
#             'discount_code': 'test-discount',
#             'percentage': 25.50,
#             'quantity': 10,
#             'time_period': -timedelta(hours=1, minutes=30),
#
#         }
#
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(DiscountCodeModel.objects.all(). count(), 0)


# class TestDiscountCodeUpdate(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#         AdminModel.objects.create(user=self.user, role='regular_admin')
#         self.discount = DiscountCodeModel.objects.create(discount_code='test-dis', percentage=20.0, time_period=timedelta(days=7))
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         AdminModel.objects.all().delete()
#         DiscountCodeModel.objects.all().delete()

    # def test_discount_code_edit(self):
    #     url = reverse('discount-code-update', kwargs={'pk': f'{self.discount.pk}'})
    #
    #     data = {
    #         'time_period': timedelta(days=14),
    #         'percentage': 10.55,
    #         'quantity': 100,
    #     }
    #
    #     response = self.client.put(url, data, format='json')
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(DiscountCodeModel.objects.first().time_period, timedelta(days=14))
    #     self.assertEqual(DiscountCodeModel.objects.first().quantity, 100)
    #
    # def test_discount_code_edit_with_invalid_data(self):
    #     url = reverse('discount-code-update', kwargs={'pk': f'{self.discount.pk}'})
    #
    #     data = {
    #         'time_period': timedelta(days=14),
    #         'percentage': -10.55,
    #         'quantity': -100,
    #     }
    #     response = self.client.put(url, data, format='json')
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class TestNotificationViews(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#         AdminModel.objects.create(user=self.user, role='regular_admin')
#         self.notif1 = NotificationModel.objects.create(title='notif1', description='this is the test notif1')
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         AdminModel.objects.all().delete()
#         NotificationModel.objects.all().delete()
#
#     def test_notification_create(self):
#
#         url = reverse('notification-create')
#
#         data = {
#             'title': 'test notif',
#             'description': 'this is a test notif',
#
#         }
#         response = self.client.post(url, data, format='multipart')
#
#         print(response.content)
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(NotificationModel.objects.all().count(), 2)
#
#     def test_notification_update(self):
#         url = reverse('notification-edit', kwargs={'pk': f'{self.notif1.pk}'})
#         data = {
#             'title': 'test notif1 edit',
#             'description': 'test notif1 got updated',
#         }
#
#         response = self.client.put(url, data, format='multipart')
#         self.notif1.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(NotificationModel.objects.all().count(), 1)
#         self.assertEqual(self.notif1.title, 'test notif1 edit')


# // StoreFront app Test //

# class TestNotificationsViews(TestCase):
#     def setUp(self):
#
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#         AdminModel.objects.create(user=self.user, role='regular_admin')
#         self.notif1 = NotificationModel.objects.create(title='notif1', description='this is the test notif1')
#         self.notif2 = NotificationModel.objects.create(title='notif2', description='this is the test notif2')
#         self.notif3 = NotificationModel.objects.create(title='notif3', description='this is the test notif3')
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         AdminModel.objects.all().delete()
#         NotificationModel.objects.all().delete()

    # def test_notification_list_view(self):
    #     url = reverse('notifications')
    #
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 3)

    # def test_notification_detail(self):
    #     url = reverse('notification-detail', kwargs={'pk': f'{self.notif1.pk}'})
    #
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['title'], 'notif1')
    #     self.assertEqual(response.data['description'], 'this is the test notif1')


# class TestProductListView(TestCase):
    # def setUp(self):
    #     self.client = APIClient()
    #     self.user = user_create()
    #     self.client.force_authenticate(user=self.user)
    #
    #     self.category1 = CategoryModel.objects.create(name='category1')
    #     self.category2 = CategoryModel.objects.create(name='category2')
    #     self.category3 = CategoryModel.objects.create(name='category3')
    #     self.category2.parent.add(self.category1)
    #
    #     self.tags10 = TagsModel.objects.create(name='test-tags10')
    #     self.tags20 = TagsModel.objects.create(name='test-tags20')
    #
    #     self.product10 = ProductModel.objects.create(name='test product 10', price=10000)
    #     self.product10.category.set([self.category1.pk])
    #     self.product10.tags.add(self.tags10)
    #
    #     self.product11 = ProductModel.objects.create(name='test product 11', price=11000, discount=20)
    #     self.product11.category.set([self.category1.pk])
    #     self.product11.tags.add(self.tags20)
    #
    #     self.product20 = ProductModel.objects.create(name='test product 20', price=20000, quantity=1)
    #     self.product20.category.set([self.category2.pk])
    #     self.product20.tags.add(self.tags10)
    #
    #     self.product21 = ProductModel.objects.create(name='test product 21', price=21000, quantity=0)
    #     self.product21.category.set([self.category2.pk])
    #     self.product21.tags.add(self.tags20)
    #
    # def tearDown(self):
    #     self.client.logout()
    #     self.user.delete()
    #
    #     CategoryModel.objects.all().delete()
    #     TagsModel.objects.all().delete()
    #     ProductModel.objects.all().delete()

    # def test_simple_product_list_view(self):
    #     url = reverse('home')
    #
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 4)

    # def test_product_list_with_filtering(self):
    #     url = reverse('home')
    #     url += '?filtering&category=category1&tags=test-tags10'
    #
    #     response = self.client.get(url)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0].get('name'), 'test product 10')

    # def test_product_list_view_with_ordering(self):
    #
    #     url = reverse('home')
    #     url += '?sort_by=final_price'
    #
    #     response = self.client.get(url)
    #
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 4)
    #     self.assertEqual(response.data[0].get('name'), 'test product 11')
    #     self.assertEqual(response.data[1].get('name'), 'test product 10')
    #     self.assertEqual(response.data[2].get('name'), 'test product 20')
    #     self.assertEqual(response.data[3].get('name'), 'test product 21')

    # def test_product_list_with_filtering_and_ordering(self):
    #
    #     url = reverse('home')
    #     url += '?sort_by=name&filtering&available=True&recently_added=True'
    #
    #     response = self.client.get(url)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 3)
    #     self.assertEqual(response.data[0].get('name'), 'test product 10')
    #     self.assertEqual(response.data[1].get('name'), 'test product 11')
    #     self.assertEqual(response.data[2].get('name'), 'test product 20')

    # def test_product_list_with_search_field(self):
    #     url = reverse('home')
    #     url += '?search=1'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 3)

    # def test_product_list_with_non_existing_value_for_search(self):
    #     url = reverse('home')
    #     url += '?search=9'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 0)


# class TestProductRetrieveView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category1 = CategoryModel.objects.create(name='category1')
#
#         self.product0 = ProductModel.objects.create(name='test product 0')
#         self.product0.category.set([self.category1.pk])
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()

    # def test_product_simple_retrieve(self):
    #     url = reverse('product', kwargs={'slug': 'test-product-0'})
    #
    #     response = self.client.get(url)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'test product 0')

    # def test_product_with_non_existing_slug(self):
    #     url = reverse('product', kwargs={'slug': 'non-existing-product'})
    #
    #     response = self.client.get(url)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class TestProductCommentListView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category1 = CategoryModel.objects.create(name='category1')
#
#         self.product0 = ProductModel.objects.create(name='test product 0')
#         self.product0.category.set([self.category1.pk])
#
#         self.product_comment = ProductComment.objects.create(product=self.product0, user=self.user,
#                                                              comment='this is a test comment')
#         self.product_comment = ProductComment.objects.create(product=self.product0, user=self.user,
#                                                              comment='this is the second test comment')
#
#     def tearDown(self):
#         self.client.logout()
#
#         ProductComment.objects.all().delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#         self.user.delete()
#
#     def test_product_comment_view(self):
#         url = reverse('product_comments', kwargs={'product_id': f'{self.product0.id}'})
#
#         response = self.client.get(url)
#         print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#         self.assertEqual(response.data[0].get('comment'), 'this is a test comment')


# class TestSpecialOfferListView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category1 = CategoryModel.objects.create(name='category1')
#         self.category2 = CategoryModel.objects.create(name='category2')
#         self.category3 = CategoryModel.objects.create(name='category3')
#
#         self.tags10 = TagsModel.objects.create(name='test-tags10')
#
#         self.product10 = ProductModel.objects.create(name='test product 10',
#                                                      price=10000,discount=30, special_offer=True)
#         self.product10.category.set([self.category1.pk])
#
#         self.product11 = ProductModel.objects.create(name='test product 11',price=11000,
#                                                      discount=20, special_offer=True)
#         self.product11.category.set([self.category1.pk])
#
#         self.product20 = ProductModel.objects.create(name='test product 20', price=20000, quantity=1)
#         self.product20.category.set([self.category2.pk])
#
#         self.product21 = ProductModel.objects.create(name='test product 21', price=21000, quantity=0)
#         self.product21.category.set([self.category2.pk])
#
#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#
#     def test_special_offer_view(self):
#         url = reverse('special_offer')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#
#     def test_last_products_view(self):
#         url = reverse('recent-products')
#
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 4)

# ShoppingCart test views:///////////////

# class TestAddProductToCartView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.category1 = CategoryModel.objects.create(name='category1')
#
#         self.product1 = ProductModel.objects.create(name='test product 1',
#                                                     price=10000, discount=30, quantity=4)
#         self.product1.category.set([self.category1.pk])
#
#     def tearDown(self):
#         self.client.logout()
#         ShoppingCartModel.objects.all().delete()
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#         self.user.delete()
#
#     def test_add_product_to_cart_by_authenticated_user(self):
#         url = reverse('add-to-cart')
#
#         data = {
#             'product_id': self.product1.pk,
#             'quantity': 3,
#         }
#
#         response = self.client.post(url, data, format='json')
#         print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)



















# OrderManagement test views: ////////////////////////
# class TestOrderListView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = user_create()
#         self.client.force_authenticate(user=self.user)
#
#         self.order_user = UserManageModel.objects.create(username='order-user', password='password',
#                                                          email='order-user@gmail.com')
#         self.test_product = ProductModel.objects.create(name='test-product', immediate_delivery=False)
#         # invoice_products = InvoiceItemModel.objects.create()
#
#         self.invoice = InvoiceModel.objects.create(user=self.order_user, amount=100000)
#         self.order = OrdersModel.objects.create(user=self.order_user, invoice=self.invoice)
#
#     def tearDown(self):
#         self.client.logout()
#         ProductModel.objects.all().delete()
#         OrdersModel.objects.all().delete()
#         InvoiceModel.objects.all().delete()
#         UserManageModel.objects.all().delete()
#
#     def test_order_list_view(self):
#         url = reverse('orders')
#
#         with patch('OrderManagement.views.OrderListView.permission_classes', [MockPermission]):
#             response = self.client.get(url)
#
#         print(response.content)
#         print(OrdersModel.objects.get(id=response.data[0].get('id')).invoice.invoice_number)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)









