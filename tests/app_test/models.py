from django.db import models
from django.utils.translation import gettext as _

from django_soft_delete import deletion
from django_soft_delete.models import SoftDeletionModel

DEFAULT_EMPLOYEE_PK = 1
DEFAULT_CITY_PK = 1


class Nationality(SoftDeletionModel):
    name = models.CharField(max_length=255, null=True, blank=True)


class User(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True,
                                unique=True)


class Employee(SoftDeletionModel):
    user = models.ForeignKey(User, on_delete=deletion.CASCADE,
                             verbose_name=_('User'), null=True,
                             blank=True)

    first_name = models.CharField(verbose_name=_("First Name"),
                                  max_length=150,
                                  blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Last Name"),
                                 max_length=150,
                                 blank=True, null=True)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class EmployeeNationality(SoftDeletionModel):
    nationality = models.ForeignKey(Nationality, null=True, blank=True,
                                    on_delete=deletion.CASCADE)
    employee = models.ForeignKey(Employee, null=True, blank=True,
                                 on_delete=deletion.SET(DEFAULT_EMPLOYEE_PK),
                                 related_name='nationalities')


class FamilyMember(SoftDeletionModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    national_id_number = models.CharField(max_length=255, null=True,
                                          blank=True)

    employee = models.ForeignKey("Employee", on_delete=deletion.SET_DEFAULT,
                                 null=True, blank=True,
                                 related_name='family_members',
                                 default=DEFAULT_EMPLOYEE_PK)


class EmployeeInterview(SoftDeletionModel):
    employee = models.ForeignKey("Employee", on_delete=deletion.SET_NULL,
                                 null=True, blank=True,
                                 related_name="interviews")
    name = models.CharField(max_length=255, null=True, blank=True)


class JobExperience(SoftDeletionModel):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    employee = models.ForeignKey("Employee", null=True, blank=True,
                                 on_delete=deletion.DO_NOTHING,
                                 related_name="experiences")


class HealthStatus(SoftDeletionModel):
    health_status_detail = models.CharField(max_length=255, null=True,
                                            blank=True, )

    employee = models.OneToOneField("Employee", null=True, blank=True,
                                    on_delete=deletion.CASCADE,
                                    related_name='health_status')


class Checkup(SoftDeletionModel):
    checkup_result = models.TextField(null=True, blank=True, max_length=10000)
    health_status = models.ForeignKey("HealthStatus", null=True, blank=True,
                                      on_delete=deletion.CASCADE,
                                      related_name="checkups")


class EmployeeProfile(SoftDeletionModel):
    employee = models.ForeignKey("Employee", null=True, blank=True,
                                 on_delete=deletion.CASCADE_NO_REVIVE,
                                 related_name='employee_profiles')
    ldap_type = models.CharField(max_length=255, null=True, blank=True)
    profile = models.CharField(max_length=255, null=True, blank=True)


class HobbyType(models.Model):
    type_name = models.TextField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=100)


class EmployeeHobby(models.Model):
    name = models.TextField(null=True, blank=True, max_length=100)

    employee = models.ForeignKey(Employee, null=True, blank=True,
                                 on_delete=deletion.CASCADE,
                                 related_name='employee_hobbies')

    type = models.ForeignKey(HobbyType, null=True, blank=True,
                             on_delete=deletion.CASCADE,
                             related_name='employee_hobbies')


class HobbyLocation(models.Model):
    location_name = models.TextField(null=True, blank=True, max_length=100)
    employee_hobby = models.ForeignKey("EmployeeHobby", null=True, blank=True,
                                       on_delete=deletion.CASCADE,
                                       related_name="hobby_locations")


class Producer(SoftDeletionModel):
    name = models.TextField(null=True, blank=True, max_length=100)
    company = models.ForeignKey("Company", null=True, blank=True,
                                on_delete=deletion.CASCADE,
                                related_name="producers")


class Product(SoftDeletionModel):
    name = models.TextField(null=True, blank=True, max_length=100)

    producer = models.ForeignKey("Producer", null=True, blank=True,
                                 on_delete=deletion.PROTECT,
                                 related_name="products")


class City(models.Model):
    name = models.TextField(null=True, blank=True, max_length=100)


class Company(SoftDeletionModel):
    name = models.TextField(null=True, blank=True, max_length=100)
    city = models.ForeignKey(City, null=True, blank=True,
                             on_delete=deletion.SET(DEFAULT_CITY_PK),
                             related_name="companies")


class Author(SoftDeletionModel):
    name = models.CharField(max_length=255, null=True, blank=True)


class Book(SoftDeletionModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True,
                               on_delete=deletion.CASCADE,
                               related_name="books")


class Poem(SoftDeletionModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True,
                               on_delete=deletion.CASCADE,
                               related_name="poems")


class Chapter(SoftDeletionModel):
    book = models.ForeignKey(Book, null=True, blank=True,
                             on_delete=deletion.CASCADE,
                             related_name="chapters")
