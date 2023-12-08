import unittest
import server


class TestCsvHandling(unittest.TestCase):

    def test_path_generation(self):
        self.assertEqual('csv/some_filename.csv',
                         server.get_path('some_filename'))

    def test_csv_exists(self):
        with self.subTest():
            self.assertTrue(server.csv_exists('amp_applications'))
        with self.subTest():
            self.assertFalse(server.csv_exists('non_existent_file'))

    def test_csv_parsing(self):
        first_element = {
            "applicationKey":
                "sites-component-distributor|1.14.0"
        }

        second_element = {
            "applicationKey":
                "sites-component-contact|1.21.0"
        }

        with self.subTest():
            json_data = server.read_csv('amp_global_applications')
            self.assertEqual(first_element, json_data[0])
            self.assertEqual(26, len(json_data))
        with self.subTest():
            json_data = server.read_csv('amp_global_applications', limit=2)
            self.assertListEqual([first_element, second_element], json_data)
        with self.subTest():
            json_data = server.read_csv('amp_global_applications', offset=1)
            self.assertEqual(second_element, json_data[0])
            self.assertEqual(25, len(json_data))
        with self.subTest():
            json_data = server.read_csv(
                'amp_global_applications', limit=1, offset=1)
            self.assertListEqual([second_element], json_data)
        with self.subTest():
            json_data = server.read_csv(
                'amp_global_applications', offset=9999999999)
            self.assertListEqual([], json_data)


if __name__ == '__main__':
    unittest.main()
