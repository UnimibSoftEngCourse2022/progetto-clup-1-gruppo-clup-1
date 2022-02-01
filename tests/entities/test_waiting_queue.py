import unittest
from collections.abc import Iterable

from src.clup.entities.waiting_queue import WaitingQueue


class TestWaitingQueue(unittest.TestCase):
    def setUp(self):
        self.q = WaitingQueue()

    def test_new_waiting_queue_is_empty(self):
        self.assertTrue(len(self.q) == 0)

    def test_pushing_an_element_should_increment_lenght(self):
        self.q.push('a')
        self.q.push('b')

        self.assertTrue(len(self.q) == 2)

    def test_push_and_pop_should_empty_the_list_and_give_same_element(self):
        self.q.push('a')
        element = self.q.pop()

        self.assertTrue(len(self.q) == 0)
        self.assertEqual(element, 'a')

    def test_pop_should_return_first_element(self):
        self.q.push('a')
        self.q.push('b')

        element = self.q.pop()

        self.assertTrue(len(self.q) == 1)
        self.assertEqual(element, 'a')

    def test_insert_should_increase_length(self):
        self.q.push('a')

        self.q.insert(0, 'b')

        self.assertTrue(len(self.q) == 2)

    def test_insert_should_place_element_in_arbitrary_place(self):
        self.q.push('a')
        self.q.push('b')

        self.q.insert(1, 'c')
        self.q.pop()
        element = self.q.pop()

        self.assertEqual(element, 'c')

    def test_insert_past_length_should_place_at_end(self):
        self.q.push('a')

        self.q.insert(100, 'b')
        self.q.pop()
        element = self.q.pop()

        self.assertEqual(element, 'b')

    def test_in_operator(self):
        self.q.push('a')

        self.assertTrue('a' in self.q)
        self.assertFalse('b' in self.q)

    def test_waiting_queue_is_iterable(self):
        is_iterable = isinstance(self.q, Iterable)

        self.assertTrue(is_iterable)

    def test_waiting_queue_iterator_return_elements(self):
        elements = set()
        self.q.push('a')
        self.q.push('b')

        for e in self.q:
            elements.add(e)

        self.assertEqual(elements, {'a', 'b'})
