import unittest
from audit import classify


class Mapping(unittest.TestCase):
    def test_house_rules_cannot_become_functional_blockers(self):
        for gate in ['2a', '4', '38i', '44b', '48', '54', '58', '63', '67']:
            self.assertEqual(classify({'gate': gate, 'tier': 'floor'}), 'design-review')

    def test_accessibility_and_fake_send_are_inspection_candidates(self):
        for gate in ['26a', '27', '40', '62', '70']:
            self.assertEqual(classify({'gate': gate}), 'functional-review')

    def test_new_rules_need_review_instead_of_automatic_enforcement(self):
        self.assertEqual(classify({'gate': '999', 'grade': 'FAIL'}), 'design-review')
        self.assertEqual(classify({'gate': 'F2'}), 'finish')


if __name__ == '__main__':
    unittest.main()
