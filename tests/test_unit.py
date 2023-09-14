import unittest
from unittest.mock import patch
from src.apartments import apartment
from src.constants import BHK_2, BHK_3, CORPORATE_WATER_RATE, BOREWELL_WATER_RATE

class TestApartment(unittest.TestCase):

    def setUp(self):
        self.apartment_bhk2 = apartment(BHK_2, "3:1")
        self.apartment_bhk3 = apartment(BHK_3, "2:2")

    def test_monthly_water_allowance(self):
        self.assertEqual(self.apartment_bhk2.monthly_water_allowance, 900)
        self.assertEqual(self.apartment_bhk3.monthly_water_allowance, 1500)

    def test_allot_water(self):
        self.assertEqual(self.apartment_bhk2.allocated_coorporation_water, 675)
        self.assertEqual(self.apartment_bhk2.allocated_borewell_water, 225)
        self.assertEqual(self.apartment_bhk3.allocated_coorporation_water, 750)
        self.assertEqual(self.apartment_bhk3.allocated_borewell_water, 750)

    def test_add_guests(self):
        self.apartment_bhk2.add_guests(2)
        self.assertEqual(self.apartment_bhk2.total_guests, 2)
        self.assertEqual(self.apartment_bhk2.total_water_consumption, 900 + 2 * 10 * 30)

    def test_get_cost_by_corporate(self):
        self.assertEqual(self.apartment_bhk2.get_cost_by_corporate(), 675 * CORPORATE_WATER_RATE)
        self.assertEqual(self.apartment_bhk3.get_cost_by_corporate(), 750 * CORPORATE_WATER_RATE)

    def test_get_cost_by_borewell(self):
        self.assertEqual(self.apartment_bhk2.get_cost_by_borewell(), 225 * BOREWELL_WATER_RATE)
        self.assertEqual(self.apartment_bhk3.get_cost_by_borewell(), 750 * BOREWELL_WATER_RATE)

    def test_get_cost_by_tank(self):
        self.assertEqual(self.apartment_bhk2.get_cost_by_tank(1200), 500 * 2 + 700 * 3)
        self.assertEqual(self.apartment_bhk2.get_cost_by_tank(2000), 500 * 2 + 1000 * 3 + 500 * 5)
        self.assertEqual(self.apartment_bhk2.get_cost_by_tank(3500), 500 * 2 + 1000 * 3 + 1500 * 5 + 500 * 8)

    @patch('src.apartments.math.ceil')
    def test_calculate_billings(self, mock_ceil):
        self.apartment_bhk2.calculate_billings()
        mock_ceil.assert_called_once_with(
            (675 * CORPORATE_WATER_RATE) + (225 * BOREWELL_WATER_RATE) + self.apartment_bhk2.get_cost_by_tank(
                self.apartment_bhk2.total_water_consumption - self.apartment_bhk2.monthly_water_allowance))

if __name__ == '__main__':
    unittest.main()
