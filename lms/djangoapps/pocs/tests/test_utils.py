from pocs.tests.factories import POCFactory
from pocs.tests.factories import POCMembershipFactory
from pocs.utils import EmailEnrollmentState
from student.roles import CoursePocCoachRole
from student.tests.factories import AdminFactory
from student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory


class TestEmailEnrollmentState(ModuleStoreTestCase):
    """unit tests for the EmailEnrollmentState class
    """

    def setUp(self):
        """
        Set up tests
        """
        course = CourseFactory.create()
        coach = AdminFactory.create()
        role = CoursePocCoachRole(course.id)
        role.add_users(coach)
        self.poc = POCFactory(course_id=course.id, coach=coach)

    def create_user(self):
        """provide a legitimate django user for testing
        """
        if getattr(self, 'user', None) is None:
            self.user = UserFactory()

    def register_user_in_poc(self):
        """create registration of self.user in self.poc

        registration will be inactive
        """
        self.create_user()
        POCMembershipFactory(poc=self.poc, student=self.user)

    def create_one(self, email=None):
        if email is None:
            email = self.user.email
        return EmailEnrollmentState(self.poc, email)

    def test_enrollment_state_for_non_user(self):
        """verify behavior for non-user email address
        """
        ee_state = self.create_one(email='nobody@nowhere.com')
        for attr in ['user', 'member', 'full_name', 'in_poc']:
            value = getattr(ee_state, attr, 'missing attribute')
            self.assertFalse(value, "{}: {}".format(value, attr))

    def test_enrollment_state_for_non_member_user(self):
        """verify behavior for email address of user who is not a poc memeber
        """
        self.create_user()
        ee_state = self.create_one()
        self.assertTrue(ee_state.user)
        self.assertFalse(ee_state.in_poc)
        self.assertEqual(ee_state.member, self.user)
        self.assertEqual(ee_state.full_name, self.user.profile.name)

    def test_enrollment_state_for_member_user(self):
        """verify behavior for email address of user who is a poc member
        """
        self.create_user()
        self.register_user_in_poc()
        ee_state = self.create_one()
        for attr in ['user', 'in_poc']:
            self.assertTrue(
                getattr(ee_state, attr, False),
                "attribute {} is missing or False".format(attr)
            )
        self.assertEqual(ee_state.member, self.user)
        self.assertEqual(ee_state.full_name, self.user.profile.name)

    def test_enrollment_state_to_dict(self):
        """verify dict representation of EmailEnrollmentState
        """
        self.create_user()
        self.register_user_in_poc()
        ee_state = self.create_one()
        ee_dict = ee_state.to_dict()
        expected = {
            'user': True,
            'member': self.user,
            'in_poc': True,
        }
        for expected_key, expected_value in expected.iteritems():
            self.assertTrue(expected_key in ee_dict)
            self.assertEqual(expected_value, ee_dict[expected_key])

    def test_enrollment_state_repr(self):
        self.create_user()
        self.register_user_in_poc()
        ee_state = self.create_one()
        representation = repr(ee_state)
        self.assertTrue('user=True' in representation)
        self.assertTrue('in_poc=True' in representation)
        member = 'member={}'.format(self.user)
        self.assertTrue(member in representation)


# TODO: deal with changes in behavior for auto_enroll
class TestGetEmailParams(ModuleStoreTestCase):
    """tests for pocs.utils.get_email_params
    """
    def setUp(self):
        """
        Set up tests
        """
        course = CourseFactory.create()
        coach = AdminFactory.create()
        role = CoursePocCoachRole(course.id)
        role.add_users(coach)
        self.poc = POCFactory(course_id=course.id, coach=coach)
        self.all_keys = [
            'site_name', 'course', 'course_url', 'registration_url',
            'course_about_url', 'auto_enroll'
        ]
        self.url_keys = [k for k in self.all_keys if 'url' in k]
        self.course_keys = [k for k in self.url_keys if 'course' in k]

    def call_FUT(self, auto_enroll=False, secure=False):
        from pocs.utils import get_email_params
        return get_email_params(self.poc, auto_enroll, secure)

    def test_params_have_expected_keys(self):
        params = self.call_FUT()
        self.assertFalse(set(params.keys()) - set(self.all_keys))

    def test_poc_id_in_params(self):
        expected_course_id = self.poc.course_id.to_deprecated_string()
        params = self.call_FUT()
        self.assertEqual(params['course'], self.poc)
        for url_key in self.url_keys:
            self.assertTrue('http://' in params[url_key])
        for url_key in self.course_keys:
            self.assertTrue(expected_course_id in params[url_key])

    def test_security_respected(self):
        secure = self.call_FUT(secure=True)
        for url_key in self.url_keys:
            self.assertTrue('https://' in secure[url_key])
        insecure = self.call_FUT(secure=False)
        for url_key in self.url_keys:
            self.assertTrue('http://' in insecure[url_key])

    def test_auto_enroll_passed_correctly(self):
        not_auto = self.call_FUT(auto_enroll=False)
        self.assertFalse(not_auto['auto_enroll'])
        auto = self.call_FUT(auto_enroll=True)
        self.assertTrue(auto['auto_enroll'])


# TODO: deal with changes in behavior for auto_enroll
class TestEnrollEmail(ModuleStoreTestCase):
    """tests for the enroll_email function from pocs.utils
    """
    def setUp(self):
        course = CourseFactory.create()
        coach = AdminFactory.create()
        role = CoursePocCoachRole(course.id)
        role.add_users(coach)
        self.poc = POCFactory(course_id=course.id, coach=coach)
        self.outbox = self.get_outbox()

    def create_user(self):
        """provide a legitimate django user for testing
        """
        if getattr(self, 'user', None) is None:
            self.user = UserFactory()

    def register_user_in_poc(self):
        """create registration of self.user in self.poc

        registration will be inactive
        """
        self.create_user()
        POCMembershipFactory(poc=self.poc, student=self.user)

    def get_outbox(self):
        from django.core import mail
        return mail.outbox

    def call_FUT(
        self,
        student_email=None,
        auto_enroll=False,
        email_students=False,
        email_params=None
    ):
        from pocs.utils import enroll_email
        if student_email is None:
            student_email = self.user.email
        before, after = enroll_email(
            self.poc, student_email, auto_enroll, email_students, email_params
        )
        return before, after

    def test_enroll_non_member_sending_email(self):
        """register a non-member and send an enrollment email to them
        """
        self.create_user()
        # ensure no emails are in the outbox now
        self.assertEqual(len(self.outbox), 0)

        before, after = self.call_FUT(email_students=True)
        self.assertFalse(before.in_poc)
        self.assertTrue(after.in_poc)
        for state in [before, after]:
            self.assertEqual(state.member, self.user)
            self.assertTrue(state.user)

        # mail was sent and to the right person
        self.assertEqual(len(self.outbox), 1)
        msg = self.outbox[0]
        self.assertTrue(self.user.email in msg.recipients())

    def test_enroll_member_sending_email(self):
        """register a member and send an enrollment email to them
        """
        self.register_user_in_poc()
        # ensure no emails are in the outbox now
        self.assertEqual(len(self.outbox), 0)

        before, after = self.call_FUT(email_students=True)
        for state in [before, after]:
            self.assertTrue(state.in_poc)
            self.assertEqual(state.member, self.user)
            self.assertTrue(state.user)

        # mail was sent and to the right person
        self.assertEqual(len(self.outbox), 1)
        msg = self.outbox[0]
        self.assertTrue(self.user.email in msg.recipients())

    def test_enroll_non_member_no_email(self):
        """register a non-member but send no email"""
        self.create_user()
        # ensure no emails are in the outbox now
        self.assertEqual(len(self.outbox), 0)

        before, after = self.call_FUT(email_students=False)
        self.assertFalse(before.in_poc)
        self.assertTrue(after.in_poc)
        for state in [before, after]:
            self.assertEqual(state.member, self.user)
            self.assertTrue(state.user)

        # ensure there are still no emails in the outbox now
        self.assertEqual(len(self.outbox), 0)

    def test_enroll_member_no_email(self):
        """enroll a member but send no email
        """
        self.register_user_in_poc()
        # ensure no emails are in the outbox now
        self.assertEqual(len(self.outbox), 0)

        before, after = self.call_FUT(email_students=False)
        for state in [before, after]:
            self.assertTrue(state.in_poc)
            self.assertEqual(state.member, self.user)
            self.assertTrue(state.user)

        # ensure there are still no emails in the outbox now
        self.assertEqual(len(self.outbox), 0)
