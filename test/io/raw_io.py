from edxia.io import raw_io

import unittest

class TestTXTio(unittest.TestCase):

    def test_format(self):
        esprit_format = raw_io.esprit_ascii_map_format
        self.assertEqual(esprit_format.delimiter, ";")
        self.assertEqual(esprit_format.max_value, 255)
        self.assertEqual(esprit_format.min_value, 0)

        cust_format = raw_io.TextMapFormat(",", 0, 1)
        self.assertEqual(cust_format.delimiter, ",")
        self.assertEqual(cust_format.max_value, 1)
        self.assertEqual(cust_format.min_value, 0)

        cust_format.delimiter = "-"
        cust_format.max_value = 5
        cust_format.min_value = -5


        self.assertEqual(cust_format.delimiter, "-")
        self.assertEqual(cust_format.max_value, 5)
        self.assertEqual(cust_format.min_value, -5)


    def test_loading(self):
        raw_io.load_txt_map("../data/esprit_BSE.txt", raw_io.esprit_ascii_map_format)

    def test_saving(self):
        save_test_maps = "tmp_save_test_map.txt"

        data = raw_io.load_txt_map("../data/esprit_BSE.txt", raw_io.esprit_ascii_map_format)
        raw_io.save_txt_map(save_test_maps, data, raw_io.esprit_ascii_map_format)

        data2 = raw_io.load_txt_map(save_test_maps, raw_io.esprit_ascii_map_format)
        self.assertTrue(((data-data2)<1e-3).all())


    def test_pickle(self):
        npy_save = "tmp_save_test_pickle_map.npy"
        data = raw_io.load_txt_map("../data/esprit_BSE.txt", raw_io.esprit_ascii_map_format)
        raw_io.save_pickle_map(npy_save, data)
        data2 = raw_io.load_pickle_map(npy_save)
        self.assertTrue(((data-data2)<1e-3).all())

if __name__ == '__main__':
    unittest.main()