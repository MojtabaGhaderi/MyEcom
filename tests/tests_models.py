import os
from datetime import timedelta
from decimal import Decimal
from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from Backstore.models import CategoryModel, TagsModel, ProductModel, ProductImage, ProductComment, DiscountCodeModel, \
    NotificationModel
from OrderManagement.models import OrdersModel
from PayManagement.models import InvoiceModel, InvoiceItemModel
from ShoppingCart.models import CartItemModel, ShoppingCartModel
from UserManagement.models import UserManageModel, AdminModel


# UserManagement Models:

# class TestUserManageModel(TestCase):
#     def setUp(self):
#         self.user = UserManageModel.objects.create(
#             username='testuser',
#             email='testmail@example.com',
#             address='test street',
#             phone_number='1234567890'
#         )
#
#     def tearDown(self):
#         self.user.delete()
#
#     def test_user_creation(self):
#
#         self.assertEqual(UserManageModel.objects.all().count(),1)
#         self.assertEqual(self.user.username, 'testuser')
#         self.assertEqual(self.user.email, 'testmail@example.com')
#         self.assertEqual(self.user.address, 'test street')
#         self.assertEqual(self.user.phone_number, '1234567890')
#
#     def test_user_str_representation(self):
#
#         self.assertEqual(str(self.user), 'testuser')
#
#
# class TestAdminModel(TestCase):
#     def setUp(self):
#         self.user = UserManageModel.objects.create(username='testuser')
#
#         self.admin = AdminModel.objects.create(
#             user=self.user,
#             role='super_admin'
#         )
#
#     def tearDown(self):
#         AdminModel.objects.all().delete()
#         UserManageModel.objects.all().delete()
#
#     def test_admin_creation(self):
#         self.assertEqual(AdminModel.objects.all().count(), 1)
#         self.assertEqual(self.admin.user, self.user)
#         self.assertEqual(self.admin.role, 'super_admin')
#         self.assertIsNotNone(self.admin.created_at)
#
#     def test_admin_str_representation(self):
#         self.assertEqual(str(self.admin), 'testuser super_admin')


# BackStore Models:

# class TestCategoryModel(TestCase):
#     def setUp(self):
#         self.parent_category = CategoryModel.objects.create(name='parent_category')
#         self.child_category = CategoryModel.objects.create(name='child_category')
#         self.child_category.parent.add(self.parent_category)
#
#     def tearDown(self):
#         CategoryModel.objects.all().delete()
#
#     def test_category_creation(self):
#         # Verify the categories were created correctly
#         self.assertEqual(CategoryModel.objects.count(), 2)
#         self.assertEqual(self.parent_category.name, 'parent_category')
#         self.assertEqual(self.child_category.name, 'child_category')
#
#     def test_category_parent_child_relationship(self):
#         self.assertIn(self.parent_category, self.child_category.parent.all())
#         self.assertIn(self.child_category, self.parent_category.children.all())
#
#     def test_category_str_representation(self):
#         self.assertEqual(str(self.parent_category), 'parent_category')
#         self.assertEqual(str(self.child_category), 'child_category')


# class TestTagsModel(TestCase):
#     def setUp(self):
#         self.Tag = TagsModel.objects.create(name='test_tag')
#
#     def tearDown(self):
#         TagsModel.objects.all().delete()
#
#     def test_tag_create(self):
#         self.assertEqual(TagsModel.objects.all().count(), 1)
#         self.assertEqual(self.Tag.name, 'test_tag')
#
#     def test_tags_str_representations(self):
#         self.assertEqual(str(self.Tag), 'test_tag')


# class TestProductModel(TestCase):
#     def setUp(self):
#
#         self.category = CategoryModel.objects.create(name='test category')
#         self.tag = TagsModel.objects.create(name='test tag')
#
#         self.product = ProductModel.objects.create(
#             name='test product',
#             quantity=3,
#             description='this is a test product',
#             price=100.55,
#             discount=20,
#             available=True,
#             likes=10,
#             special_offer=True,
#             recently_added=True,
#             immediate_delivery=True,
#
#         )
#         self.product.category.add(self.category)
#         self.product.tags.add(self.tag)
#
#     def tearDown(self):
#         ProductModel.objects.all().delete()
#         CategoryModel.objects.all().delete()
#         TagsModel.objects.all().delete()
#
#     def test_product_creation(self):
#         self.assertEqual(ProductModel.objects.count(), 1)
#         self.assertEqual(self.product.name, 'test product')
#         self.assertEqual(self.product.price, 100.55)
#         self.assertTrue(self.product.immediate_delivery)
#         self.assertIn(self.category, self.product.category.all())
#         self.assertIn(self.tag, self.product.tags.all())
#
#     def test_product_str_representation(self):
#         self.assertEqual(str(self.product), 'test product')
#
#     def test_slug(self):
#         self.assertEqual(self.product.slug, 'test-product')
#
#     def test_get_final_price(self):
#         self.assertEqual(self.product.final_price, (100.55*80)/100)


# class TestProductImageModel(TestCase):
#     def setUp(self):
#         self.product = ProductModel.objects.create(name='test product')
#
#         self.image_file = SimpleUploadedFile('test_image.jpg', b'image_data')
#         self.product_image = ProductImage.objects.create(
#             product=self.product,
#             image=self.image_file
#         )
#
#     def tearDown(self):
#         ProductModel.objects.all().delete()
#         ProductImage.objects.all().delete()
#
#     def test_product_image_creation(self):
#
#         self.assertIsNotNone(self.product_image.id)
#         self.assertEqual(self.product_image.product, self.product)
#         self.assertIsNotNone(self.product_image.image)
#
#     def test_deleting_product(self):
#         self.product.delete()
#         self.assertFalse(ProductImage.objects.filter(id=self.product_image.id).exists())
#
#     def test_product_image_update(self):
#         last_product_name = self.product_image.image.name
#         new_image = SimpleUploadedFile('new_image.jpg', b'new_image_data')
#         self.product_image.image = new_image
#         self.product_image.save()
#
#         self.product_image.refresh_from_db()
#         self.assertNotEqual(self.product_image.image.name, last_product_name)
#         stored_file_name = os.path.basename(self.product_image.image.name)
#         _, new_image_ext = os.path.splitext(new_image.name)
#         self.assertTrue(stored_file_name.endswith(new_image_ext))
#
#     def test_image_delete(self):
#         self.product_image.delete()
#         self.assertFalse(ProductImage.objects.filter(id=self.product_image.id).exists())


# class TestProductComment(TestCase):
#
#     def setUp(self):
#         self.product = ProductModel.objects.create(name='test product')
#         self.user = UserManageModel.objects.create(username='test user')
#         self.comment = ProductComment.objects.create(
#             product=self.product,
#             user=self.user,
#             comment='this is my test comment'
#         )
#
#     def tearDown(self):
#         ProductComment.objects.all().delete()
#         ProductModel.objects.all().delete()
#         UserManageModel.objects.all().delete()
#
#     def test_product_comment_creation(self):
#         self.assertEqual(ProductComment.objects.count(),1)
#         self.assertEqual(self.comment.comment, 'this is my test comment')
#         self.assertEqual(self.comment.product, self.product)
#         self.assertEqual(self.comment.user, self.user)
#         self.assertIsInstance(self.comment.date_added, timezone.datetime)
#
#     def test_user_deletion_preserves_comments(self):
#         self.user.delete()
#         comments = ProductComment.objects.all()
#         self.assertEqual(len(comments), 1)
#         self.assertEqual(comments[0], self.comment)
#         self.assertIsNone(comments[0].user)
#

# class TestDiscountModel(TestCase):
#     def setUp(self):
#         self.user = UserManageModel.objects.create(username='test user')
#         self.discount_code = DiscountCodeModel.objects.create(discount_code='test-discount-code', percentage=20.50,
#                                                               quantity=2, time_period=timedelta(days=2),
#                                                               created_by=self.user)
#
#     def tearDown(self):
#         self.user.delete()
#         DiscountCodeModel.objects.all().delete()
#
#     def test_discount_code_create(self):
#         self.assertIsNotNone(self.discount_code)
#         self.assertEqual(DiscountCodeModel.objects.all().count(), 1)
#         self.assertEqual(DiscountCodeModel.objects.all()[0].discount_code, 'test-discount-code')
#         self.assertEqual(DiscountCodeModel.objects.all()[0].created_by, self.user)
#
#     def test_discount_code_update(self):
#         self.discount_code.time_period = timedelta(days=3)
#         self.discount_code.save()
#         self.discount_code.refresh_from_db()
#
#         self.assertEqual(DiscountCodeModel.objects.all().count(), 1)
#         self.assertEqual(DiscountCodeModel.objects.all()[0].discount_code, 'test-discount-code')
#         self.assertEqual(DiscountCodeModel.objects.all()[0].time_period, timedelta(days=3))
#
#     def test_discount_code_with_quantity_limit(self):
#
#         self.discount_code.used = 2
#         self.discount_code.save()
#         self.discount_code.refresh_from_db()
#         self.assertFalse(self.discount_code.available)
#
# class TestNotificationModel(TestCase):
#     def setUp(self):
#         self.image_file = SimpleUploadedFile('test_notif_image.jpg', b'image_data')
#         self.notification = NotificationModel.objects.create(title='test notif',
#                                                              description='this is a test notification',
#                                                              image=self.image_file)
#
#     def tearDown(self):
#         NotificationModel.objects.all().delete()
#
#     def test_notification_create(self):
#         self.assertEqual(NotificationModel.objects.all().count(), 1)
#         self.assertEqual(self.notification.title, 'test notif')
#         stored_file_name = os.path.basename(self.notification.image.name)
#         _, new_image_ext = os.path.splitext(self.image_file.name)
#         self.assertTrue(stored_file_name.endswith(new_image_ext))
#
#     def test_notification_update(self):
#         self.notification.title = 'updated title'
#         self.notification.description = 'updated description'
#
#         self.image_file2 = SimpleUploadedFile('updated_notif_image.jpg', b'image_data')
#         self.notification.image = self.image_file2
#
#         self.notification.save()
#         self.notification.refresh_from_db()
#
#         self.assertEqual(NotificationModel.objects.all().count(), 1)
#         self.assertEqual(self.notification.title, 'updated title')
#         self.assertEqual(self.notification.description, 'updated description')
#         stored_file_name = os.path.basename(self.notification.image.name)
#         _, new_image_ext = os.path.splitext(self.image_file2.name)
#         self.assertTrue(stored_file_name.endswith(new_image_ext))
#
#     def test_notification_delete(self):
#
#         self.notification.delete()
#         self.assertEqual(NotificationModel.objects.all().count(), 0)


# ShoppingCart Models:


# class TestShoppingCartModel(TestCase):
#
#     def setUp(self):
#         self.user = UserManageModel.objects.create(username='test user', email='test@example.com')
#
#         self.product1 = ProductModel.objects.create(name='product1', quantity=1, price=100)
#         self.product2 = ProductModel.objects.create(name='product2', quantity=2, price=200)
#         self.product3 = ProductModel.objects.create(name='product3', quantity=3, price=300, discount=10)
#
#         self.shopping_cart = ShoppingCartModel.objects.create(user=self.user)
#
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product1, quantity=1)
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product2, quantity=1)
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product3, quantity=3)
#
#     def tearDown(self):
#         ShoppingCartModel.objects.all().delete()
#         ProductModel.objects.all().delete()
#         UserManageModel.objects.all().delete()
#
#     def test_shopping_cart_creation(self):
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.user, self.user)
#         self.assertEqual(self.shopping_cart.products.all().count(), 3)
#         self.assertEqual(self.product1.final_price + self.product2.final_price + self.product3.final_price*3,
#                          self.shopping_cart.total_price)
#
#     def test_empty_cart_creation(self):
#         user2 = UserManageModel.objects.create(username='user2')
#         empty_cart = ShoppingCartModel.objects.create(user=user2)
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 2)
#         self.assertEqual(empty_cart.products.all().count(), 0)
#         self.assertEqual(empty_cart.total_price, 0)
#
#     def test_shopping_cart_add_products(self):
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product2, quantity=1)
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.user, self.user)
#         self.assertEqual(self.shopping_cart.products.all().count(), 3)
#         self.assertEqual(self.product1.final_price + self.product2.final_price*2 + self.product3.final_price * 3,
#                          self.shopping_cart.total_price)
#
#     def test_updating_existing_cart_items(self):
#         updating_item = CartItemModel.objects.filter(shopping_cart=self.shopping_cart,
#                                                      products=self.product3).first()
#         updating_item.quantity = 2
#         updating_item.save()
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.user, self.user)
#         self.assertEqual(self.shopping_cart.products.all().count(), 3)
#         self.assertEqual(self.product1.final_price + self.product2.final_price + self.product3.final_price * 2,
#                          self.shopping_cart.total_price)
#
#     def test_deleting_existing_cart_item(self):
#         deleting_item = CartItemModel.objects.filter(shopping_cart=self.shopping_cart,
#                                                      products=self.product3).first()
#         deleting_item.delete()
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.user, self.user)
#         self.assertEqual(self.shopping_cart.products.all().count(), 2)
#         self.assertEqual(self.product1.final_price + self.product2.final_price,
#                          self.shopping_cart.total_price)
#
#     def test_user_delete(self):
#         self.user.delete()
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 0)
#
#     def test_create_cart_for_anonymous_user(self):
#         anonymous_user_id = 'abcd_1234_efg'
#         anonymous_cart = ShoppingCartModel.objects.create(anonymous_user_id=anonymous_user_id)
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 2)
#         self.assertIsNone(anonymous_cart.user)
#         self.assertEqual(anonymous_cart.anonymous_user_id, anonymous_user_id)
#         self.assertEqual(anonymous_cart.products.all().count(), 0)
#         self.assertEqual(anonymous_cart.total_price, 0)
#
#     def test_add_products_to_anonymous_cart(self):
#         anonymous_user_id = 'abcd_1234_efg'
#         anonymous_cart = ShoppingCartModel.objects.create(anonymous_user_id=anonymous_user_id)
#         CartItemModel.objects.create(shopping_cart=anonymous_cart, products=self.product1, quantity=1)
#         self.assertEqual(anonymous_cart.products.all().count(), 1)
#         self.assertEqual(anonymous_cart.total_price, self.product1.final_price)
#
#     def test_convert_anonymous_cart_to_user_cart(self):
#         anonymous_user_id = 'abcd_1234_efg'
#         anonymous_cart = ShoppingCartModel.objects.create(anonymous_user_id=anonymous_user_id)
#         CartItemModel.objects.create(shopping_cart=anonymous_cart, products=self.product1, quantity=1)
#
#         user2 = UserManageModel.objects.create(username='user2')
#         anonymous_cart.user = user2
#         anonymous_cart.anonymous_user_id = None
#         anonymous_cart.save()
#         anonymous_cart.refresh_from_db()
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 2)
#         self.assertIsNotNone(anonymous_cart.user)
#         self.assertIsNone(anonymous_cart.anonymous_user_id)
#         self.assertEqual(anonymous_cart.products.all().count(), 1)
#         self.assertEqual(anonymous_cart.total_price, self.product1.final_price)
#
#     def test_product_price_change(self):
#         self.product1.price = 1000
#         self.product1.save()
#         self.product1.refresh_from_db()
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.user, self.user)
#         self.assertEqual(self.shopping_cart.products.all().count(), 3)
#         self.assertEqual(Decimal(self.product1.final_price) + Decimal(self.product2.final_price)
#                          + Decimal(self.product3.final_price*3),
#                          self.shopping_cart.total_price)
#

# PayManagement models:

# class TestInvoiceModel(TestCase):
#
#     def setUp(self):
#         self.user = UserManageModel.objects.create(username='test user', email='test@example.com')
#         self.product1 = ProductModel.objects.create(name='product1', quantity=1, price=100)
#         self.product2 = ProductModel.objects.create(name='product2', quantity=2, price=200)
#         self.product3 = ProductModel.objects.create(name='product3', quantity=3, price=300, discount=10)
#
#         self.shopping_cart = ShoppingCartModel.objects.create(user=self.user)
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product1, quantity=1)
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product2, quantity=1)
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product3, quantity=3)
#
#     def tearDown(self):
#         InvoiceModel.objects.all().delete()
#         InvoiceItemModel.objects.all().delete()
#         ShoppingCartModel.objects.all().delete()
#         ProductModel.objects.all().delete()
#         UserManageModel.objects.all().delete()
#
#     def test_invoice_creation(self):
#         self.shopping_cart.pay_tried = True
#         self.shopping_cart.save()
#         self.assertEqual(InvoiceModel.objects.all().count(), 1)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product1).first().quantity, 1)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product2).first().quantity, 1)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product3).first().quantity, 3)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product3).first().price_at_purchase, 270)
#
#     def test_price_and_discount_change_after_invoice_creation(self):
#         self.shopping_cart.pay_tried = True
#         self.shopping_cart.save()
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product1).first().quantity, 1)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product2).first().quantity, 1)
#         self.product1.price = 200
#         self.product2.discount = 50
#         self.product1.save()
#         self.product2.save()
#         self.product1.refresh_from_db()
#         self.product2.refresh_from_db()
#
#         self.assertEqual(self.product1.final_price, 200)
#         self.assertEqual(self.product2.final_price, 100)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product1).first().price_at_purchase, 100)
#         self.assertEqual(InvoiceItemModel.objects.all().filter(product=self.product2).first().price_at_purchase, 200)
#
#     def test_empty_cart_after_successful_payment(self):
#         self.shopping_cart.pay_tried = True
#         self.shopping_cart.save()
#
#         invoice = InvoiceModel.objects.all().filter(user=self.user).order_by('-invoice_number').first()
#         invoice.successful_payment = True
#         invoice.save()
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(InvoiceModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.products.all().count(), 0)
#
#     def test_empty_cart_after_successful_payment_for_anonymous_user(self):
#         anonymous_user_id = 'abcd_1234_efg'
#         anonymous_cart = ShoppingCartModel.objects.create(anonymous_user_id=anonymous_user_id)
#         CartItemModel.objects.create(shopping_cart=anonymous_cart, products=self.product1, quantity=1)
#
#         anonymous_cart.pay_tried = True
#         anonymous_cart.save()
#         self.assertEqual(InvoiceModel.objects.all().count(), 1)
#
#         invoice = InvoiceModel.objects.all().filter(anonymous_user_id=
#         anonymous_user_id).order_by('-invoice_number').first()
#         invoice.successful_payment = True
#         invoice.save()
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 2)
#         self.assertEqual(anonymous_cart.products.all().count(), 0)
#
#     def test_unsuccessful_payment(self):
#
#         self.shopping_cart.pay_tried = True
#         self.shopping_cart.save()
#
#         invoice = InvoiceModel.objects.all().filter(user=self.user).order_by('-invoice_number').first()
#         invoice.successful_payment = False
#         invoice.save()
#
#         self.assertEqual(ShoppingCartModel.objects.all().count(), 1)
#         self.assertEqual(InvoiceModel.objects.all().count(), 1)
#         self.assertEqual(self.shopping_cart.products.all().count(), 3)


# /// OrderManagementModels ///

# class TestOrderModel(TestCase):
#
#     def setUp(self):
#         self.user = UserManageModel.objects.create(username='test user', email='test@example.com')
#         self.product1 = ProductModel.objects.create(name='product1', quantity=1, price=100)
#         self.shopping_cart = ShoppingCartModel.objects.create(user=self.user)
#         CartItemModel.objects.create(shopping_cart=self.shopping_cart, products=self.product1, quantity=1)
#         self.shopping_cart.pay_tried = True
#         self.shopping_cart.save()
#         invoice = InvoiceModel.objects.all().filter(user=self.user).order_by('-invoice_number').first()
#         invoice.successful_payment = True
#         invoice.save()
#
#     def tearDown(self):
#         InvoiceModel.objects.all().delete()
#         ShoppingCartModel.objects.all().delete()
#         ProductModel.objects.all().delete()
#         UserManageModel.objects.all().delete()
#         OrdersModel.objects.all().delete()
#
#     def test_order_model_creation(self):
#         self.assertEqual(OrdersModel.objects.all().count(), 1)
#         self.assertEqual(OrdersModel.objects.all().first().status, 'Pending')














