from pyppy.container import container, destroy_container, _CONTAINER
from test.testcase import TestCase
from test.testing import container_config_cleanup


class ContainerTest(TestCase):

    def test_container(self):
        with container_config_cleanup():
            cont = container()
            cont.tmp1 = "tmp1"
            cont.tmp2 = "tmp2"
            self.assertEqual(container().tmp1, "tmp1")
            self.assertEqual(container().tmp2, "tmp2")

            destroy_container()

            with self.assertRaises(AttributeError):
                container().tmp1

            with self.assertRaises(AttributeError):
                container().tmp2

    def test_initialize_after_destroy(self):
        cont = container()
        cont.tmp = "tmp"
        destroy_container()

        cont = container()

        with self.assertRaises(AttributeError):
            cont.tmp1

    def test_delattr(self):
        cont = container()
        cont.tmp = "tmp"
        delattr(cont, "tmp")

        with self.assertRaises(AttributeError):
            cont.tmp

    def test_delete_container(self):
        container()
        self.assertTrue(hasattr(container, _CONTAINER))
        container().tmp = "tmp"
        self.assertTrue(hasattr(container(), "tmp"))
        destroy_container()
        self.assertFalse(hasattr(container, _CONTAINER))
