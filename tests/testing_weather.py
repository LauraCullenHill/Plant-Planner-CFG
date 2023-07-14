from unittest import TestCase, mock, main
from todays_weather import get_lat_lng_from_postcode, get_weather_data, get_uv_data, \
     get_pollen_count, generate_temp_advice, generate_uv_advice, generate_pollen_advice, \
     get_all_details, weather_information, uv_information, pollen_information, print_summary

class TestGetLatLngFromPostcode(TestCase):

    def test_valid_postcode(self):
        expected = (53.402636, -2.222864)
        result = get_lat_lng_from_postcode('M20 5NT')
        self.assertEqual(expected, result)

    def test_invalid_postcode(self):
        with self.assertRaises(Exception):
            get_lat_lng_from_postcode('230 MGG')

class TestGetWeatherData(TestCase):

    def test_valid_weather_search(self):
        result = get_weather_data('56d606d8cf1592faae517b13cad44c68', 53.402636, -2.222864)
        self.assertEqual(list(result.keys()), ['description', 'temperature', 'humidity'])

    def test_invalid_api_weather_search(self):
        with self.assertRaises(Exception):
            get_weather_data('44557788', 53.402636, -2.222864)

class TestGetUVData(TestCase):

    def test_valid_uv_search(self):
        result = get_uv_data('openuv-65hqrlhgjscfg-io', 53.402636, -2.222864)
        self.assertEqual(list(result.keys()), ['uv', 'uv_max', 'uv_max_time', 'sunrise', 'sunset'])

    def test_invalid_api_uv_search(self):
        with self.assertRaises(Exception):
            get_uv_data('44557788', 53.402636, -2.222864)

class TestGetPollenData(TestCase):

    def test_valid_pollen_search(self):
        result = get_pollen_count(53.402636, -2.222864)
        self.assertEqual(list(result.keys()), ['grass_pollen', 'tree_pollen', 'weed_pollen'])

    def test_invalid_longitude_pollen_search(self):
        with self.assertRaises(Exception):
            get_uv_data(1, -2.222864)

class TestTempAdvice(TestCase):

    def test_high_temp(self):
        result = generate_temp_advice(25)
        message = "The weather is hot today, best to stay indoors and keep hydrated\n"
        self.assertEqual(result, message)

    def test_warm_temp(self):
        result = generate_temp_advice(20)
        message = "The weather is warm, have plenty of cool drinks and take regular breaks\n"
        self.assertEqual(result, message)

    def test_cool_temp(self):
        result = generate_temp_advice(10)
        message = "The temperature is cool today\n"
        self.assertEqual(result, message)

    def test_cold_temp(self):
        result = generate_temp_advice(0)
        message = "It's cold today, wrap up warm!\n"
        self.assertEqual(result, message)

    def test_icy_temp(self):
        result = generate_temp_advice(-1)
        message = "Icy conditions, not suitable for gardening\n"
        self.assertEqual(result, message)

class TestUVAdvice(TestCase):

    def test_very_high_uv(self):
        result = generate_uv_advice(8)
        message = "Peak UV levels are very high today, best to stay indoors\n"
        self.assertEqual(result, message)

    def test_high_uv(self):
        result = generate_uv_advice(6)
        message = "Peak UV levels are high today, take care\n"
        self.assertEqual(result, message)

    def test_safe_uv(self):
        result = generate_uv_advice(5)
        message = "UV levels are safe today\n"
        self.assertEqual(result, message)

class TestPollenAdvice(TestCase):

    def test_high_tree_moderate_grass_low_weed(self):
        result = generate_pollen_advice({'grass_pollen': 'Moderate', 'tree_pollen': 'High', 'weed_pollen': 'Low'})
        message = """The Tree Pollen is high today. Take an antihistamine if required.
The Grass Pollen is at a moderate level today. Take appropriate measures.
The Weed Pollen is at a low level today. No specific precautions needed.\n"""
        self.assertEqual(result, message)

    def test_low_grass_moderate_tree_high_weed(self):
        result = generate_pollen_advice({'grass_pollen': 'Low', 'tree_pollen': 'Moderate', 'weed_pollen': 'High'})
        message = """The Weed Pollen is high today. Take an antihistamine if required.
The Tree Pollen is at a moderate level today. Take appropriate measures.
The Grass Pollen is at a low level today. No specific precautions needed.\n"""
        self.assertEqual(result, message)

    def test_high_grass_low_tree_moderate_weed(self):
        result = generate_pollen_advice({'grass_pollen': 'High', 'tree_pollen': 'Low', 'weed_pollen': 'Moderate'})
        message = """The Grass Pollen is high today. Take an antihistamine if required.
The Weed Pollen is at a moderate level today. Take appropriate measures.
The Tree Pollen is at a low level today. No specific precautions needed.\n"""
        self.assertEqual(result, message)

    def test_all_pollen_high(self):
        result = generate_pollen_advice({'grass_pollen': 'High', 'tree_pollen': 'High', 'weed_pollen': 'High'})
        message = """The Grass Pollen, Tree Pollen, Weed Pollen is high today. Take an antihistamine if required.\n"""
        self.assertEqual(result, message)

    def test_all_pollen_low(self):
        result = generate_pollen_advice({'grass_pollen': 'Low', 'tree_pollen': 'Low', 'weed_pollen': 'Low'})
        message = """The Grass Pollen, Tree Pollen and Weed Pollen is at a low level today. No specific precautions needed.\n"""
        self.assertEqual(result, message)


class TestGetAllDetails(TestCase):

    def test_success_getting_details(self):
        @mock.patch.object(todays_weather, 'get_lat_lng_from_postcode')
        @mock.patch.object(todays_weather, 'get_pollen_count')
        @mock.patch.object(todays_weather, 'get_uv_data')
        @mock.patch.object(todays_weather, 'get_weather_data')
        def test_run_getting_details(self, mock_get_lat_lng_from_postcode, mock_get_pollen_count, mock_get_uv_data, mock_get_weather_data):
            mock_get_lat_lng_from_postcode.return_value = (53.402636, -2.222864)
            mock_get_pollen_count.return_value = {'grass_pollen': 'Moderate', 'tree_pollen': 'Moderate', 'weed_pollen': 'Low'}
            mock_get_uv_data.return_value = {'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'}
            mock_get_weather_data.return_value = {'description': 'clear sky', 'temperature': 11.300000000000011, 'humidity': 80}
            result = get_all_details("M20 5NT")
            expected = ('M20 5NT', {'grass_pollen': 'Moderate', 'tree_pollen': 'Moderate', 'weed_pollen': 'Low'}, {'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'}, {'description': 'clear sky', 'temperature': 11.300000000000011, 'humidity': 80})
            self.assertEqual(result, expected)

    def test_pollen_none_getting_details(self):
        @mock.patch.object(todays_weather, 'get_lat_lng_from_postcode')
        @mock.patch.object(todays_weather, 'get_pollen_count')
        @mock.patch.object(todays_weather, 'get_uv_data')
        @mock.patch.object(todays_weather, 'get_weather_data')
        def test_run_getting_details(self, mock_get_lat_lng_from_postcode, mock_get_pollen_count, mock_get_uv_data, mock_get_weather_data):
            mock_get_lat_lng_from_postcode.return_value = (53.402636, -2.222864)
            mock_get_pollen_count.return_value = None
            mock_get_uv_data.return_value = {'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'}
            mock_get_weather_data.return_value = {'description': 'clear sky', 'temperature': 11.300000000000011, 'humidity': 80}
            result = get_all_details("M20 5NT")
            expected = ('M20 5NT', None, {'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'}, {'description': 'clear sky', 'temperature': 11.300000000000011, 'humidity': 80})
            self.assertEqual(result, expected)

class TestWeatherInformation(TestCase):

    def test_success_weather_info(self):
        self.assertTrue(weather_information({'description': 'clear sky', 'temperature': 11.300000000000011, 'humidity': 80}))

    def test_failure_weather_info(self):
        self.assertFalse(weather_information(None))

class TestUVInformation(TestCase):

    def test_success_uv_info(self):
        self.assertTrue(uv_information({'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'}))

    def test_failure_uv_info(self):

class TestPollenInformation(TestCase):

    def test_success_pollen_info(self):
        self.assertTrue(pollen_information({'grass_pollen': 'Moderate', 'tree_pollen': 'Moderate', 'weed_pollen': 'Low'}))

    def test_failure_pollen_info(self):
        self.assertFalse(pollen_information(None))

class TestPrintSummary(TestCase):

    def test_success_print_summary(self):
        result = print_summary("M20 5NT", {'grass_pollen': 'Moderate', 'tree_pollen': 'Moderate', 'weed_pollen': 'Low'}, \
                    {'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'},\
                    {'description': 'clear sky', 'temperature': 11.300000000000011, 'humidity': 80})
        expected = (True, True, True)
        self.assertEqual(result, expected)

    def test_missing_weather_data(self):
        result = print_summary("M20 5NT", {'grass_pollen': 'Moderate', 'tree_pollen': 'Moderate', 'weed_pollen': 'Low'}, \
                    {'uv': 1.1812, 'uv_max': 6.7259, 'uv_max_time': '12:06 PM', 'sunrise': '04:03 AM', 'sunset': '08:10 PM'}, \
                    None)
        expected = (False, True, True)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    main()