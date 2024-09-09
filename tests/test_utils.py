import unittest
from copy_app.utils import get_value_from_dict

class TestGetValueFromDict(unittest.TestCase):

    def test_key_at_top_level(self):
        data = {'a': 1, 'b': 2}
        self.assertEqual(get_value_from_dict(data, 'a'), 1)
        self.assertEqual(get_value_from_dict(data, 'b'), 2)

    def test_key_in_nested_dict(self):
        data = {'a': {'b': {'c': 3}}}
        self.assertEqual(get_value_from_dict(data, 'c'), 3)

    def test_key_in_list_within_dict(self):
        data = {'a': [{'b': 2}, {'c': 3}]}
        self.assertEqual(get_value_from_dict(data, 'c'), 3)

    def test_key_not_present(self):
        data = {'a': 1, 'b': 2}
        self.assertIsNone(get_value_from_dict(data, 'c'))

    def test_empty_dict(self):
        data = {}
        self.assertIsNone(get_value_from_dict(data, 'a'))

    def test_empty_list(self):
        data = []
        self.assertIsNone(get_value_from_dict(data, 'a'))

    def test_complex_structure(self):
        data = {
            'a': {
                'b': [
                    {'c': 3},
                    {'d': {'e': 5}}
                ]
            }
        }
        self.assertEqual(get_value_from_dict(data, 'c'), 3)
        self.assertEqual(get_value_from_dict(data, 'e'), 5)

if __name__ == '__main__':
    unittest.main()