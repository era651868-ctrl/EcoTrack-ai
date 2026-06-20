import unittest

class TestEcoTrackLogic(unittest.TestCase):
    def setUp(self):
        """Set up standard carbon baseline constants for evaluation verification."""
        self.petrol_factor = 2.31  # kg CO2 per Liter
        self.electricity_factor = 0.85  # kg CO2 per kWh

    def test_transportation_calculation(self):
        """Test baseline transport metric logic calculation integrity."""
        distance = 50  # km
        fuel_consumed = distance * 0.08  # Assumed consumption rate
        calculated_emissions = fuel_consumed * self.petrol_factor
        self.assertGreater(calculated_emissions, 0)

    def test_energy_calculation(self):
        """Test baseline utility consumption metric logic calculation integrity."""
        kwh_consumed = 150
        calculated_emissions = kwh_consumed * self.electricity_factor
        self.assertEqual(calculated_emissions, 127.5)

if __name__ == '__main__':
    unittest.main()
  
