from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone

from .factories import *
from .models import DEFAULT_EMPLOYEE_PK, DEFAULT_CITY_PK


class DeletionTest(TestCase):

    def setUp(self):
        self.default_employee = EmployeeFactory(pk=DEFAULT_EMPLOYEE_PK)
        self.employee = EmployeeFactory()
        self.employee1 = EmployeeFactory()

        self.emp_pk = self.employee.pk
        employee_hobby = EmployeeHobby.objects.get(employee=self.employee)
        self.employee_hobby_pk = employee_hobby.pk
        self.employee_hobby_type_pk = employee_hobby.type.pk

    def test_creation_process(self):
        self.assertTrue(
            FamilyMember.objects.filter(employee=self.emp_pk).exists())
        self.assertTrue(
            EmployeeNationality.objects.filter(
                employee=self.emp_pk).exists())
        self.assertTrue(
            EmployeeInterview.objects.filter(
                employee=self.emp_pk).exists())

        self.assertTrue(
            JobExperience.objects.filter(
                employee=self.emp_pk).exists())
        self.assertTrue(
            HealthStatus.objects.filter(
                employee=self.emp_pk).exists())
        self.assertTrue(
            Checkup.objects.filter(
                health_status=HealthStatus.objects.get(
                    employee=self.emp_pk).pk).exists())

        self.assertTrue(
            EmployeeHobby.objects.filter(
                employee=self.emp_pk).exists())

        self.assertTrue(HobbyType.objects.filter(employee_hobbies=
        EmployeeHobby.objects.get(
            employee=self.emp_pk)).exists())

        self.assertTrue(
            HobbyLocation.objects.filter(
                employee_hobby=EmployeeHobby.objects.get(
                    employee=self.emp_pk)).exists())

    def test_set_default_for_instance(self):
        self.employee.delete()
        self.check_set_default_relation()

    def test_set_for_instance(self):
        self.employee.delete()
        self.check_set_relation()

    def test_do_nothing_for_instance(self):
        self.employee.delete()
        self.check_do_nothing_relation()

    def test_counter_for_instance(self):
        self.assertEqual(self.employee.delete()[0], 6)

    def test_cascade_with_soft_deletion_model_for_instance(self):
        self.employee.delete()
        self.check_cascade_relation()

    def test_cascade_with_not_soft_deletion_model_for_instance(self):
        self.employee.delete()
        self.check_cascade_relation_with_no_soft_deletion_model()

    def test_set_default_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        self.check_set_default_relation()

    def test_set_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        self.check_set_relation()

    def test_do_nothing_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        self.check_do_nothing_relation()

    def test_cascade_with_soft_deletion_model_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        self.check_cascade_relation()

    def test_cascade_with_not_soft_deletion_model_for_qs(self):
        Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()
        self.check_cascade_relation_with_no_soft_deletion_model()

    def test_counter_for_qs(self):
        counter = Employee.objects.exclude(id=DEFAULT_EMPLOYEE_PK).delete()[0]
        self.assertEqual(counter, 12)

    def test_update_or_create_with_multiple_parameter(self):
        Employee.objects.filter(id=self.emp_pk).update_or_create(
            defaults={'deleted_at': timezone.now(),
                      'last_name': 'test'})
        self.assertFalse(Employee.objects.filter(pk=self.emp_pk).exists())
        deleted_emp = Employee.all_objects.filter(pk=self.emp_pk)
        self.assertTrue(deleted_emp.exists())
        self.assertEqual(deleted_emp[0].last_name, "test")

    def test_set_default_using_update_or_create(self):
        Employee.objects.filter(id=self.emp_pk).update_or_create(
            defaults={'deleted_at': timezone.now()})
        self.check_set_default_relation()

    def test_set_for_using_update_or_create(self):
        Employee.objects.filter(id=self.emp_pk).update_or_create(
            defaults={'deleted_at': timezone.now(),
                      })
        self.check_set_relation()

    def test_do_nothing_using_update_or_create(self):
        Employee.objects.filter(id=self.emp_pk).update_or_create(
            defaults={'deleted_at': timezone.now()})
        self.check_do_nothing_relation()

    def test_cascade_with_soft_deletion_model_using_update_or_create(self):
        Employee.objects.filter(id=self.emp_pk).update_or_create(
            defaults={'deleted_at': timezone.now()})
        self.check_cascade_relation()

    def test_cascade_with_not_soft_deletion_model_using_update_or_create(self):
        Employee.objects.filter(id=self.emp_pk).update_or_create(
            defaults={'deleted_at': timezone.now()})
        self.check_cascade_relation_with_no_soft_deletion_model()

    def check_set_default_relation(self):
        # test on_delete=SET_DEFAULT
        self.assertFalse(Employee.objects.filter(pk=self.emp_pk).exists())
        self.assertTrue(Employee.all_objects.filter(pk=self.emp_pk).exists())

        # test on_delete=SET_DEFAULT
        self.assertFalse(
            FamilyMember.objects.filter(employee=self.emp_pk).exists())

        self.assertTrue(FamilyMember.objects.filter(
            employee=DEFAULT_EMPLOYEE_PK).exists())

    def check_set_relation(self):
        # test on_delete=SET
        self.assertFalse(
            EmployeeNationality.objects.filter(
                employee=self.emp_pk).exists())

        self.assertTrue(EmployeeNationality.objects.filter(
            employee=DEFAULT_EMPLOYEE_PK).exists())

    def check_do_nothing_relation(self):
        # test on_delete=SET
        # test on_delete=DO_NOTHING
        self.assertTrue(
            JobExperience.objects.filter(
                employee=self.emp_pk).exists())

    def check_cascade_relation(self):
        # test cascade with soft deletion model
        self.assertFalse(
            HealthStatus.objects.filter(employee=self.emp_pk).exists())
        h = HealthStatus.all_objects.filter(employee=self.emp_pk)
        self.assertTrue(h.exists())
        self.assertFalse(Checkup.objects.filter(health_status__in=h).exists())
        self.assertTrue(
            Checkup.all_objects.filter(health_status__in=h).exists())

    def check_cascade_relation_with_no_soft_deletion_model(self):
        # test cascade with not soft deletion model
        self.assertFalse(
            EmployeeHobby.objects.filter(employee=self.emp_pk).exists())
        self.assertFalse(HobbyLocation.objects.filter(
            employee_hobby=self.employee_hobby_pk).exists())
        self.assertTrue(
            HobbyType.objects.filter(pk=self.employee_hobby_type_pk).exists())

    def test_protect_and_cascade_models_deletion_with_success(self):
        CityFactory(pk=DEFAULT_CITY_PK)
        city = CityFactory()
        city_pk = city.pk
        company = city.companies.first()
        company_pk = company.pk
        city.delete()
        self.assertFalse(Company.objects.filter(city=city_pk).exists())
        self.assertTrue(Company.objects.filter(city=DEFAULT_CITY_PK).exists())

        producer = company.producers.first()
        producer_pk = producer.pk
        product_pk = producer.products.first().pk

        producer.products.first().delete()
        company.delete()

        self.assertFalse(Company.objects.filter(pk=company_pk).exists())
        self.assertTrue(Company.all_objects.filter(pk=company_pk).exists())

        self.assertFalse(Producer.objects.filter(pk=producer_pk).exists())
        self.assertTrue(Producer.all_objects.filter(pk=producer_pk).exists())

        self.assertFalse(Product.objects.filter(pk=product_pk).exists())
        self.assertTrue(Product.all_objects.filter(pk=product_pk).exists())

    def test_protect_with_fail(self):
        CityFactory(pk=DEFAULT_CITY_PK)
        city = CityFactory()
        company = city.companies.first()
        with self.assertRaises(ProtectedError):
            company.delete()
