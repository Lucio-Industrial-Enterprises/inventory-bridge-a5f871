import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        for zone, weight, expected in (
            ("local", 2, 8.0),
            ("regional", 2, 11.0),
            ("local", 1.234, 6.85),
            ("regional", 1.234, 9.85),
        ):
            with self.subTest(zone=zone, weight=weight):
                self.assertEqual(shipping_quote(weight, zone), expected)
                self.assertEqual(
                    shipping_quote(weight, zone, service="standard"), expected
                )

    def test_express_rates(self):
        for zone, expected in (("local", 15.0), ("regional", 18.0)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, "express"), expected)

    def test_express_surcharge(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 1.234, 2, 10.55):
                with self.subTest(zone=zone, weight=weight):
                    self.assertEqual(
                        shipping_quote(weight, zone, service="express"),
                        round(shipping_quote(weight, zone) + 7, 2),
                    )

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service=service)

    def test_invalid_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service=service)

    def test_invalid_service(self):
        for service in ("overnight", "", "Express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown service"):
                    shipping_quote(2, "local", service=service)
