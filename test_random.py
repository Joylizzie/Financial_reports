import unittest
import make_random_data


class TestRandom(unittest.TestCase):

    def test_cities(self):
        city_list=make_random_data.make_random_cities(path = 'data/wash_cities.csv', num = 10)

    def test_surnames(self):
        surnames = make_random_data.make_random_surnames(path = 'data/surnames.csv', num = 10)

    def test_first_name(self):
        make_random_data.make_random_first_names(path = 'data/first_names.csv', num = 10)

    def test_phone_numbers(self):
        make_random_data.make_phone_numbers(num = 10)

    def test_street_address(self):
        make_random_data.make_street_address(path = 'data/street_names.csv', num = 10)

    def test_email(self):
        make_random_data.make_random_email_domains(path = 'data/emails.csv', num = 10)


if __name__ == '__main__':
    unittest.main()

