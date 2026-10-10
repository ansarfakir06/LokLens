"""
LokLens — Automated Backend Test Suite (test_api.py)

Tests:
1. Health Check & Environment Status
2. States Listing & Unverified State Handling
3. Administrations Listing & Filtering
4. Promises Listing for Karnataka (5 Guarantees)
5. Category Filtering (Energy, Women, Food, Youth, Transport)
6. Search Filtering (Positive, Case-Insensitive, Empty Results)
7. Invalid Input Validation (400 Bad Request)
8. Single Promise Retrieval & Enriched Civic Fields
9. Non-Existent Resource Handling (404 Not Found)
10. Promise Progress & Metric Structure
11. Documented Sources & Citations
12. Static File Delivery (HTML, CSS, JS, PDF)
"""

import unittest
from app import app

class TestLokLensBackend(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # -------------------------------------------------------------------------
    # 1. System Health & Environment
    # -------------------------------------------------------------------------
    def test_01_health_check(self):
        """Verify the health endpoint returns 200 and reports database status."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("database", data)
        self.assertIn("version", data)

    # -------------------------------------------------------------------------
    # 2. States & Unverified States
    # -------------------------------------------------------------------------
    def test_02_get_states(self):
        """Verify all 5 states are listed and unverified states have messages."""
        response = self.client.get("/api/states")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["count"], 5)
        
        # Check Karnataka
        karnataka = next((s for s in data["states"] if s["id"] == "karnataka"), None)
        self.assertIsNotNone(karnataka)
        self.assertTrue(karnataka["hasData"])

        # Check Unverified State (Tamil Nadu)
        tamil_nadu = next((s for s in data["states"] if s["id"] == "tamil-nadu"), None)
        self.assertIsNotNone(tamil_nadu)
        self.assertFalse(tamil_nadu["hasData"])
        self.assertTrue(len(tamil_nadu["message"]) > 10)

    # -------------------------------------------------------------------------
    # 3. Administrations Listing
    # -------------------------------------------------------------------------
    def test_03_get_administrations(self):
        """Verify administrations endpoint returns governing bodies."""
        response = self.client.get("/api/administrations?state=karnataka")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["count"], 0)
        self.assertEqual(data["administrations"][0]["stateId"], "karnataka")

    # -------------------------------------------------------------------------
    # 4. Karnataka 5 Guarantees
    # -------------------------------------------------------------------------
    def test_04_get_karnataka_promises(self):
        """Verify Karnataka returns all 5 flagship guarantees."""
        response = self.client.get("/api/promises?state=karnataka")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["hasData"])
        self.assertEqual(data["count"], 5)
        
        promise_ids = [p["id"] for p in data["promises"]]
        expected_ids = ["gruha-jyothi", "gruha-lakshmi", "anna-bhagya", "yuvanidhi", "shakti"]
        for exp_id in expected_ids:
            self.assertIn(exp_id, promise_ids)

    # -------------------------------------------------------------------------
    # 5. Category Filtering
    # -------------------------------------------------------------------------
    def test_05_category_filtering(self):
        """Verify promises filter accurately by category."""
        categories = ["energy", "women", "food", "youth", "transport"]
        for cat in categories:
            response = self.client.get(f"/api/promises?state=karnataka&category={cat}")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data["count"], 1, f"Failed for category: {cat}")
            self.assertEqual(data["promises"][0]["category"], cat)

    # -------------------------------------------------------------------------
    # 6. Search Filtering
    # -------------------------------------------------------------------------
    def test_06_search_filtering(self):
        """Verify search finds promises by scheme name and keyword."""
        # Search by term
        response = self.client.get("/api/promises?state=karnataka&search=electricity")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["promises"][0]["id"], "gruha-jyothi")

        # Search with case insensitivity
        response = self.client.get("/api/promises?state=karnataka&search=SHAKTI")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["promises"][0]["id"], "shakti")

        # Search returning empty results
        response = self.client.get("/api/promises?state=karnataka&search=rocketscience")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["count"], 0)

    # -------------------------------------------------------------------------
    # 7. Invalid Input Handling (400 Bad Request)
    # -------------------------------------------------------------------------
    def test_07_invalid_state_validation(self):
        """Verify an unrecognized state returns HTTP 400 Bad Request."""
        response = self.client.get("/api/promises?state=fictional_state")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    # -------------------------------------------------------------------------
    # 8. Single Promise Retrieval & Enriched Civic Fields
    # -------------------------------------------------------------------------
    def test_08_single_promise_details(self):
        """Verify a single promise contains all verified fields and citations."""
        response = self.client.get("/api/promises/anna-bhagya")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertEqual(data["name"], "Anna Bhagya")
        self.assertEqual(data["status"], "adjusted")
        self.assertIn("department", data)
        self.assertIn("governmentOrder", data)
        self.assertIn("eligibility", data)
        self.assertIn("metrics", data)
        self.assertIn("sources", data)
        self.assertGreater(len(data["sources"]), 0)

    # -------------------------------------------------------------------------
    # 9. Non-Existent Resource Handling (404 Not Found)
    # -------------------------------------------------------------------------
    def test_09_promise_not_found(self):
        """Verify non-existent promise ID returns HTTP 404 Not Found."""
        response = self.client.get("/api/promises/nonexistent_promise_999")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)

    # -------------------------------------------------------------------------
    # 10. Promise Progress & Metrics
    # -------------------------------------------------------------------------
    def test_10_promise_progress(self):
        """Verify progress endpoint returns appropriate metrics and transparency note."""
        response = self.client.get("/api/promises/gruha-lakshmi/progress")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["promiseId"], "gruha-lakshmi")
        self.assertIn("metrics", data)
        self.assertIn("dataNotes", data)

    # -------------------------------------------------------------------------
    # 11. Documented Sources
    # -------------------------------------------------------------------------
    def test_11_get_sources(self):
        """Verify sources endpoint returns consolidated citations."""
        response = self.client.get("/api/sources")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["count"], 0)
        self.assertIn("sources", data)

    # -------------------------------------------------------------------------
    # 12. Static File Delivery
    # -------------------------------------------------------------------------
    def test_12_static_assets_served(self):
        """Verify Flask serves frontend static files properly."""
        endpoints = ["/", "/style.css", "/script.js", "/data.js"]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200, f"Failed for static asset: {endpoint}")
            response.close()

if __name__ == "__main__":
    unittest.main()
