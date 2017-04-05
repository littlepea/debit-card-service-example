from django.test import SimpleTestCase

from authentication import factories


class UserModelTestCase(SimpleTestCase):
    def setUp(self):
        self.parent = factories.ParentUserFactory.build()
        self.child = factories.ChildUserFactory.build()

    def test_is_parent(self):
        self.assertTrue(self.parent.is_parent)

    def test_is_not_parent(self):
        self.assertFalse(self.child.is_parent)
