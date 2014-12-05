from factory.django import DjangoModelFactory
from pocs.models import PersonalOnlineCourse
from pocs.models import PocMembership


class POCFactory(DjangoModelFactory):
    FACTORY_FOR = PersonalOnlineCourse
    display_name = "Test POC"


class POCMembershipFactory(DjangoModelFactory):
    FACTORY_FOR = PocMembership
    active = False
