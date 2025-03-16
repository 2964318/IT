from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment

User = get_user_model()

class CourseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='testpass123',
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass',
        )
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Programming',
            teacher='Tony',
            credits=3,
            schedule='Friday 4:00 PM - 6:00 PM',
            capacity=30,
            enrolled_students=0
        )

    def test_course_creation(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('add_course'), {
            'code': 'CS102',
            'name': 'Data Structures',
            'teacher': 'Tony',
            'credits':3,
            'schedule': 'Friday 2:00 PM - 4:00 PM',
            'capacity': 25,
            'enrolled_students': 0
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.count(), 2)

    def test_enrollment_process(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.post(reverse('enroll', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(
            student=self.user,
            course=self.course
        ).exists())

    def test_course_deletion_notifications(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('delete_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.count(), 0)