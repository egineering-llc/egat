from egat.test_runner_helpers import WorkerThread
from egat.test_runner_helpers import WorkProvider
from egat.execution_groups import execution_group
import unittest

@execution_group(1)
class Fixture1():
    def meth1():
        pass
    def meth2():
        pass
    @execution_group(2)
    def meth3():
        pass

class Fixture2():
    @execution_group(2)
    def meth1():
        pass
    @execution_group(3)
    @execution_group(4)
    def meth2():
        pass
    def meth3():
        pass

class MockWorkPool():
    failed_ex_groups = None

class TestWorkerThread(unittest.TestCase):
    def test_has_failed_ex_groups(self):
        wp = WorkProvider()
        env = { 'env': 'env' }

        # Same class, no failed ex groups
        self.assertFalse(
            WorkerThread.has_failed_ex_groups(Fixture1, Fixture1.meth1, env, wp)
        )
        self.assertFalse(
            WorkerThread.has_failed_ex_groups(Fixture1, Fixture1.meth2, env, wp)
        )

        # Same class, with failed class ex groups
        wp.add_failed_ex_groups([1], env)

        self.assertTrue(
            WorkerThread.has_failed_ex_groups(Fixture1, Fixture1.meth1, env, wp)
        )
        self.assertTrue(
            WorkerThread.has_failed_ex_groups(Fixture1, Fixture1.meth2, env, wp)
        )

        # Same class, no ex groups, with wp.failed_ex_groups reset
        wp = WorkProvider()

        self.assertFalse(
            WorkerThread.has_failed_ex_groups(Fixture1, Fixture1.meth1, env, wp)
        )
        self.assertFalse(
            WorkerThread.has_failed_ex_groups(Fixture1, Fixture1.meth2, env, wp)
        )

        # Same class, with one method having a failed ex_group
        wp.add_failed_ex_groups([2], env)

        self.assertTrue(
            WorkerThread.has_failed_ex_groups(Fixture2, Fixture2.meth1, env, wp)
        )
        self.assertFalse(
            WorkerThread.has_failed_ex_groups(Fixture2, Fixture2.meth2, env, wp)
        )

    def test_get_ex_groups(self):
        self.assertEqual([1], WorkerThread.get_ex_groups(Fixture1))
        self.assertEqual([], WorkerThread.get_ex_groups(Fixture1.meth1))
        self.assertEqual([], WorkerThread.get_ex_groups(Fixture1.meth2))
        self.assertEqual([2], WorkerThread.get_ex_groups(Fixture1.meth3))

        self.assertEqual([], WorkerThread.get_ex_groups(Fixture2))
        self.assertEqual([2], WorkerThread.get_ex_groups(Fixture2.meth1))
        self.assertEqual([3, 4], sorted(WorkerThread.get_ex_groups(Fixture2.meth2)))
        self.assertEqual([], WorkerThread.get_ex_groups(Fixture2.meth3))

        # class and method
        self.assertEqual([1], WorkerThread.get_ex_groups(Fixture1, Fixture1.meth1))

        # class and method, each have an execution group
        self.assertEqual(
            [1, 2],
            sorted(WorkerThread.get_ex_groups(Fixture1, Fixture1.meth3))
        )

        # two methods
        self.assertEqual(
            [2], 
            WorkerThread.get_ex_groups(Fixture1.meth2, Fixture1.meth3)
        )

        # two classes
        self.assertEqual([1], WorkerThread.get_ex_groups(Fixture1, Fixture2))

        # class and method with multiple groups
        self.assertEqual(
            [1, 3, 4], 
            sorted(WorkerThread.get_ex_groups(Fixture1, Fixture2.meth2))
        )
