import factory

from tests.app_test.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'username__{n}')


class NationalityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Nationality

    name = factory.Sequence(lambda n: f'nation__{n}')


class EmployeeNationalityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeNationality

    nationality = factory.SubFactory(factory=NationalityFactory)


class FamilyMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FamilyMember

    full_name = factory.Sequence(lambda n: f'family_member__{n}')
    national_id_number = factory.Sequence(lambda n: f'{n}')


class EmployeeInterviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeInterview

    name = factory.Sequence(lambda n: f'interviewer__{n}')


class JobExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobExperience

    company_name = factory.Sequence(lambda n: f'company_name__{n}')


class CheckupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checkup

    checkup_result = factory.Sequence(lambda n: f'checkup_result__{n}')


class HealthStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HealthStatus

    health_status_detail = factory.Sequence(
        lambda n: f'health_status_detail__{n}')

    health_status = factory.RelatedFactory(
        CheckupFactory, 'health_status')


class HobbyLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HobbyLocation

    location_name = factory.Sequence(lambda n: f'hobby_location_name__{n}')


class HobbyTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HobbyType

    type_name = factory.Sequence(lambda n: f'hobby_type_name__{n}')


class EmployeeHobbyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeHobby

    name = factory.Sequence(lambda n: f'hobby_name__{n}')
    hobby_locations = factory.RelatedFactory(
        HobbyLocationFactory, 'employee_hobby')

    type = factory.SubFactory(HobbyTypeFactory)


class EmployeeProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeProfile

    ldap_type = factory.Sequence(lambda n: f'hobby_name__{n}')


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = factory.Sequence(lambda n: f'first__{n}')
    last_name = factory.Sequence(lambda n: f'last__{n}')

    user = factory.SubFactory(UserFactory)
    nationalities = factory.RelatedFactory(
        EmployeeNationalityFactory, 'employee')

    family_members = factory.RelatedFactory(
        FamilyMemberFactory, 'employee')

    interviews = factory.RelatedFactory(
        EmployeeInterviewFactory, 'employee')

    job_experiences = factory.RelatedFactory(
        JobExperienceFactory, 'employee')

    health_status = factory.RelatedFactory(
        HealthStatusFactory, 'employee')

    employee_hobbies = factory.RelatedFactory(
        EmployeeHobbyFactory, 'employee')

    employee_profiles = factory.RelatedFactory(
        EmployeeProfileFactory, 'employee')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'product_name__{n}')


class ProducerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Producer

    name = factory.Sequence(lambda n: f'producer_name__{n}')
    products = factory.RelatedFactory(
        ProductFactory, 'producer')


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Sequence(lambda n: f'company_name__{n}')
    producers = factory.RelatedFactory(
        ProducerFactory, 'company')


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: f'city_name__{n}')
    companies = factory.RelatedFactory(
        CompanyFactory, 'city')


class ChapterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chapter


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    name = factory.Sequence(lambda n: f'book__{n}')
    chapters = factory.RelatedFactory(ChapterFactory, 'book')


class PoemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poem

    name = factory.Sequence(lambda n: f'poem__{n}')


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'author__{n}')
    books = factory.RelatedFactory(BookFactory, 'author')
    poems = factory.RelatedFactory(PoemFactory, 'author')
