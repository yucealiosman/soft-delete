from django.test import TestCase

from .factories import *
from .models import DEFAULT_EMPLOYEE_PK


class UndeleteTest(TestCase):
    def setUp(self):
        self.default_employee = EmployeeFactory(pk=DEFAULT_EMPLOYEE_PK)
        self.employee = EmployeeFactory()
        self.employee1 = EmployeeFactory()

        self.emp_pk = self.employee.pk
        employee_hobby = EmployeeHobby.objects.get(employee=self.employee)
        self.employee_hobby_pk = employee_hobby.pk
        self.employee_hobby_type_pk = employee_hobby.type.pk

    def test_cascade_with_soft_deletion_model_for_instance(self):
        self.employee.delete()
        emp = Employee.all_objects.get(pk=self.emp_pk)
        emp.undelete()
        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.check_cascade_relation()

    def test_cascade_with_not_soft_deletion_model_for_instance(self):
        self.employee.delete()
        emp = Employee.all_objects.get(pk=self.emp_pk)
        emp.undelete()
        self.check_cascade_relation_with_no_soft_deletion_model()

    def test_cascade_no_revive_with_soft_deletion_model_for_instance(self):
        self.employee.delete()
        emp = Employee.all_objects.get(pk=self.emp_pk)
        emp.undelete()
        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.check_cascade_no_revive_relation()

    def test_cascade_with_soft_deletion_model_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.undelete()
        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.check_cascade_relation()

    def test_cascade_with_not_soft_deletion_model_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.undelete()
        self.check_cascade_relation_with_no_soft_deletion_model()

    def test_cascade_no_revive_with_soft_deletion_model_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.undelete()
        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.check_cascade_no_revive_relation()

    def test_counter_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        count, d = emp.undelete()
        self.assertEqual(count, 3)

    def test_update_or_create_with_multiple_parameter(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.update_or_create(defaults={'deleted_at': None,
                                       'last_name': 'test5'})

        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.assertEqual(Employee.objects.get(pk=self.emp_pk).last_name,
                         "test5")

    def test_cascade_with_soft_deletion_model_using_update_or_create(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.update_or_create(defaults={'deleted_at': None})
        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.check_cascade_relation()

    def test_cascade_with_not_soft_deletion_model_using_update_or_create(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.update_or_create(defaults={'deleted_at': None})
        self.check_cascade_relation_with_no_soft_deletion_model()

    def test_cascade_no_revive_with_soft_deletion_model_using_update_or_create(
            self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        emp = Employee.all_objects.filter(pk=self.emp_pk)
        emp.update_or_create(defaults={'deleted_at': None})
        self.assertTrue(Employee.objects.filter(pk=self.emp_pk).exists())
        self.check_cascade_no_revive_relation()

    def test_undelete_with_state(self):
        author = AuthorFactory()
        old_book = author.books.first()
        old_book.delete()

        new_book = BookFactory()
        author.books.add(new_book)
        author.delete()
        author.undelete()

        self.assertTrue(Author.objects.filter(pk=author.pk).exists())
        self.assertTrue(Book.objects.filter(pk=new_book.pk).exists())
        self.assertFalse(Book.objects.filter(pk=old_book.pk).exists())

    def test_undelete_with_state_qs(self):
        author1, author2 = AuthorFactory.create_batch(size=2)
        old_book1 = author1.books.first()
        old_book2 = author2.books.first()
        old_book1.delete()

        new_book = BookFactory()
        author1.books.add(new_book)
        Author.objects.all().delete()
        Author.all_objects.all().undelete()

        self.assertEqual(Author.objects.all().count(), 2)
        self.assertTrue(Book.objects.filter(pk=new_book.pk).exists())
        self.assertFalse(Book.objects.filter(pk=old_book1.pk).exists())
        self.assertTrue(Book.objects.filter(pk=old_book2.pk).exists())

    def test_undelete_state_with_nested_cascade_relation(self):
        author = AuthorFactory()
        old_book = author.books.first()
        old_chapter = old_book.chapters.first()
        old_book.delete()

        new_book = BookFactory()
        new_chapter = new_book.chapters.first()
        author.books.add(new_book)
        author.delete()
        author.undelete()

        self.assertTrue(Chapter.objects.filter(pk=new_chapter.pk).exists())
        self.assertFalse(Chapter.objects.filter(pk=old_chapter.pk).exists())

    def test_undelete_state_with_multiple_cascade_relation(self):
        author = AuthorFactory()
        old_book = author.books.first()
        old_poem = author.poems.first()
        old_book.delete()
        old_poem.delete()

        new_book = BookFactory()
        new_poem = PoemFactory()
        author.books.add(new_book)
        author.poems.add(new_poem)
        author.delete()
        author.undelete()

        self.assertFalse(Book.objects.filter(pk=old_book.pk).exists())
        self.assertTrue(Book.objects.filter(pk=new_book.pk).exists())
        self.assertFalse(Poem.objects.filter(pk=old_poem.pk).exists())
        self.assertTrue(Poem.objects.filter(pk=new_poem.pk).exists())

    def check_cascade_relation(self):
        # test cascade with soft deletion model
        h = HealthStatus.objects.filter(employee=self.emp_pk)
        self.assertTrue(h.exists())
        self.assertTrue(Checkup.objects.filter(health_status__in=h).exists())

    def check_cascade_no_revive_relation(self):
        self.assertFalse(
            EmployeeProfile.objects.filter(employee=self.emp_pk).exists())
        ep = EmployeeProfile.all_objects.filter(employee=self.emp_pk)
        self.assertTrue(ep.exists())

    def check_cascade_relation_with_no_soft_deletion_model(self):
        # test cascade with not soft deletion model
        self.assertFalse(
            EmployeeHobby.objects.filter(employee=self.emp_pk).exists())
        self.assertFalse(HobbyLocation.objects.filter(
            employee_hobby=self.employee_hobby_pk).exists())
        self.assertTrue(
            HobbyType.objects.filter(pk=self.employee_hobby_type_pk).exists())
