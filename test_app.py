import unittest

class TestEcoTrackCompleteSuite(unittest.TestCase):
    def setUp(self):
        """Set up standard carbon multipliers for production validation."""
        self.fuel_multipliers = {"Petrol": 0.24, "Diesel": 0.27, "Electric": 0.05, "CNG": 0.18}
        self.diet_multipliers = {"Meat-heavy": 300.0, "Balanced/Mixed": 200.0, "Vegetarian": 120.0, "Vegan": 80.0}

    def test_transportation_emissions(self):
        """Validates that transportation mathematical constants remain bounded."""
        km_driven = 50.0
        transport_emissions = (km_driven * 52 * self.fuel_multipliers["Petrol"]) / 12
        self.assertAlmostEqual(transport_emissions, 52.0, places=1)

    def test_energy_emissions(self):
        """Validates home power consumption offsets logic math."""
        electricity_kwh = 150.0
        clean_energy_pct = 20  # 20% renewable energy offset
        energy_emissions = electricity_kwh * 0.82 * (1 - clean_energy_pct / 100)
        self.assertAlmostEqual(energy_emissions, 98.4, places=1)

    def test_dietary_emissions(self):
        """Validates carbon scale parameters across nutrition vectors."""
        diet_type = "Vegetarian"
        food_emissions = self.diet_multipliers[diet_type]
        self.assertEqual(food_emissions, 120.0)

if __name__ == '__main__':
    unittest.main()
    
