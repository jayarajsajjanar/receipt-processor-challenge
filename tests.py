"""Tests for the app."""

import unittest

from flask import request  # pylint:disable=import-error

from app import app, root_debug
from utils import calculate_points, validate_request

# from flask.testing import FlaskClient

# #################  TODO   #################  # pylint:disable=fixme
# 1. Mock out DB. Currently tests are running on the actual DB.


class TestAppFunctions(unittest.TestCase):
    """Test the app functions."""

    def setUp(self):
        """Set up the test client."""
        self.client = app.test_client()
        self.client.testing = True

    def test_root_debug(self):
        """Test the root_debug function."""
        with app.test_request_context("/"):
            self.assertEqual(root_debug(), "Hello World3!")


sample_valid_data = {
    "retailer": "Best Buy",
    "purchaseDate": "2023-10-01",
    "purchaseTime": "13:45",
    "items": [{"shortDescription": "Laptop", "price": "999.99"}],
    "total": "999.99",
}

provided_valid_data_1 = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00",
        },  # noqa: E501
    ],
    "total": "35.35",
}

provided_valid_data_2 = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
    ],
    "total": "9.00",
}


class TestUtils(unittest.TestCase):
    """Test the utility functions."""

    def test_validate_request_valid_1(self):
        """Test the validate_request function with valid data."""
        try:
            validate_request(sample_valid_data)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")

    def test_validate_request_valid_2(self):
        """Test the validate_request function with valid data."""
        sample_valid_data2 = sample_valid_data.copy()
        sample_valid_data2["total"] = "00.00"
        try:
            validate_request(sample_valid_data2)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")

    def test_validate_request_valid_3(self):
        """Test the validate_request function with valid data."""
        sample_valid_data2 = sample_valid_data.copy()
        sample_valid_data2["purchaseDate"] = "2020-10-10"
        try:
            validate_request(sample_valid_data2)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")

    def test_validate_request_valid_4(self):
        """Test the validate_request function with valid data."""
        sample_valid_data2 = sample_valid_data.copy()
        sample_valid_data2["retailer"] = "x"
        try:
            validate_request(sample_valid_data2)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")

    def test_validate_request_invalid_retailer_1(self):
        """Test the validate_request function with invalid data."""
        sample_valid_data_copy = sample_valid_data.copy()
        del sample_valid_data_copy["retailer"]
        with self.assertRaises(Exception):
            validate_request(sample_valid_data_copy)

    def test_validate_request_invalid_retailer_2(self):
        """Test the validate_request function with invalid data."""
        sample_valid_data_copy = sample_valid_data.copy()
        sample_valid_data_copy["retailer"] = "####"
        with self.assertRaises(Exception):
            validate_request(sample_valid_data_copy)

    def test_validate_request_invalid_total_1(self):
        """Test the validate_request function with invalid data."""
        sample_valid_data_copy = sample_valid_data.copy()
        sample_valid_data_copy["total"] = ".9"
        with self.assertRaises(Exception):
            validate_request(sample_valid_data_copy)

    # no exception even though date is invalid
    def test_validate_request_invalid_date_1(self):
        """Test the validate_request function with invalid data."""
        sample_valid_data_copy = sample_valid_data.copy()
        sample_valid_data_copy["purchaseDate"] = "2020-10-"
        try:
            validate_request(sample_valid_data_copy)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")

    # no exception even though date is invalid
    def test_validate_request_invalid_date_2(self):
        """Test the validate_request function with invalid data."""
        sample_valid_data_copy = sample_valid_data.copy()
        sample_valid_data_copy["purchaseDate"] = "2020-10-"
        try:
            validate_request(sample_valid_data_copy)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")

    # no exception even though time is invalid
    def test_validate_request_invalid_time_2(self):
        """Test the validate_request function with invalid data."""
        sample_valid_data_copy = sample_valid_data.copy()
        sample_valid_data_copy["purchaseTime"] = ""
        try:
            validate_request(sample_valid_data_copy)
        except Exception as e:  # pylint:disable=broad-exception-caught
            self.fail(f"validate_request raised an exception {e}")


class TestCalculatePoints(unittest.TestCase):
    """Test the calculate_points function."""

    def test_calculate_points_1(self):
        """Test the calculate_points function."""
        retailer_name = "a"
        total = 100.00
        items = [
            {"shortDescription": "Laptop", "price": 999.99},
            {"shortDescription": "Mouse", "price": 25.00},
        ]
        purchaseDate = "2023-10-01"  # pylint:disable=invalid-name
        purchaseTime = "15:00"  # pylint:disable=invalid-name
        points = calculate_points(
            retailer_name, total, items, purchaseDate, purchaseTime
        )
        self.assertEqual(points, 297)

    def test_calculate_points_2(self):
        """Test the calculate_points function."""
        retailer_name = "a"
        total = 99.01
        items = [
            {"shortDescription": "Laptop", "price": 999.99},
            {"shortDescription": "Mouse", "price": 25.00},
        ]
        purchaseDate = "2023-10-01"  # pylint:disable=invalid-name
        purchaseTime = "15:00"  # pylint:disable=invalid-name
        points = calculate_points(
            retailer_name, total, items, purchaseDate, purchaseTime
        )
        self.assertEqual(points, 222)

    def test_calculate_points_generated_by_llm(self):
        """Test the calculate_points function."""
        retailer_name = "a"  # 1
        total = 100.00  # 25
        items = [
            {"shortDescription": "Laptop", "price": 999.99},
            {"shortDescription": "Mouse", "price": 25.00},
        ]  # 5 + 999.99 * 0.2 = 5 + 200 = 210
        purchaseDate = "2023-10-01"  # 6  # pylint:disable=invalid-name
        purchaseTime = "15:00"  # 10  # pylint:disable=invalid-name
        points = calculate_points(
            retailer_name,
            total,
            items,
            purchaseDate,
            purchaseTime,
            generated_by_llm=True,
        )
        self.assertEqual(points, 302)


class FlaskAppTestCase(unittest.TestCase):
    """Test the Flask app."""

    def setUp(self):
        """Set up the test client."""
        self.client = app.test_client()
        self.client.testing = True
        # self.client["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        # db.init_app(self.client)

    def test_request_process_receipt_endpoint(self):
        """Test the request to the process receipt endpoint."""
        with app.test_request_context(
            "/receipts/process",
            method="POST",
            json=sample_valid_data,
        ):

            self.assertEqual(request.path, "/receipts/process")
            self.assertEqual(request.method, "POST")
            self.assertEqual(request.get_json(), sample_valid_data)

    def test_response_process_receipt_endpoint(self):
        """Test the request to the process receipt endpoint."""
        response = self.client.post(
            "/receipts/process", json=sample_valid_data
        )  # noqa: E501

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json["id"])

    def test_response_full_1(self):
        """Test the request to the process receipt endpoint."""
        response = self.client.post(
            "/receipts/process", json=provided_valid_data_1
        )  # noqa: E501

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json["id"])

        receipt_id = response.json["id"]

        response = self.client.get(f"/receipts/{receipt_id}/points")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["points"], 28)

    def test_response_full_2(self):
        """Test the request to the process receipt endpoint."""
        response = self.client.post(
            "/receipts/process", json=provided_valid_data_2
        )  # noqa: E501

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json["id"])

        receipt_id = response.json["id"]

        response = self.client.get(f"/receipts/{receipt_id}/points")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["points"], 109)


if __name__ == "__main__":
    unittest.main()
