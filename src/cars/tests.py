from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Brand, Car, CarImage


def make_car(**kwargs):
    brand, _ = Brand.objects.get_or_create(name="تويوتا")
    defaults = dict(
        brand=brand,
        car_type=Car.CarType.USED,
        status=Car.Status.AVAILABLE,
        model_name="كامري",
        year=2022,
    )
    defaults.update(kwargs)
    return Car.objects.create(**defaults)


class BrandModelTest(TestCase):
    def test_create_brand(self):
        brand = Brand.objects.create(name="هيونداي")
        self.assertEqual(str(brand), "هيونداي")

    def test_brand_name_unique(self):
        Brand.objects.create(name="نيسان")
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="نيسان")


class CarModelTest(TestCase):
    def test_create_used_car(self):
        car = make_car(
            mileage_km=45000,
            transmission=Car.Transmission.AUTOMATIC,
            fuel_type=Car.FuelType.PETROL,
            engine_size="2.5L",
            exterior_color="أبيض",
            origin=Car.Origin.SAUDI,
            city="الرياض",
            price=85000,
        )
        self.assertEqual(car.car_type, "used")
        self.assertEqual(car.city, "الرياض")
        self.assertEqual(car.mileage_km, 45000)
        self.assertIn("كامري", str(car))

    def test_create_new_car(self):
        car = make_car(
            car_type=Car.CarType.NEW,
            trim="Sport",
            features_summary="كاميرا خلفية، نظام صوتي متقدم",
            price=120000,
            price_label="ابتداءً من",
        )
        self.assertEqual(car.car_type, "new")
        self.assertEqual(car.trim, "Sport")

    def test_default_status_is_available(self):
        car = make_car()
        self.assertEqual(car.status, Car.Status.AVAILABLE)

    def test_is_visible_available(self):
        car = make_car(status=Car.Status.AVAILABLE)
        self.assertTrue(car.is_visible)

    def test_is_visible_hidden(self):
        car = make_car(status=Car.Status.HIDDEN)
        self.assertFalse(car.is_visible)

    def test_is_visible_sold(self):
        car = make_car(status=Car.Status.SOLD)
        self.assertFalse(car.is_visible)

    def test_price_optional(self):
        car = make_car(price=None)
        self.assertIsNone(car.price)

    def test_city_optional(self):
        car = make_car(city="")
        self.assertEqual(car.city, "")

    def test_ordering_newest_first(self):
        car1 = make_car(model_name="كامري")
        car2 = make_car(model_name="كورولا")
        cars = list(Car.objects.all())
        self.assertEqual(cars[0], car2)

    def test_str_contains_brand_model_year(self):
        car = make_car()
        s = str(car)
        self.assertIn("تويوتا", s)
        self.assertIn("كامري", s)
        self.assertIn("2022", s)

    def test_no_branch_field(self):
        self.assertFalse(hasattr(Car, "branch"))


class CarImageModelTest(TestCase):
    def setUp(self):
        self.car = make_car()

    def test_multiple_images(self):
        CarImage.objects.create(car=self.car, image="cars/img1.jpg", is_main=True)
        CarImage.objects.create(car=self.car, image="cars/img2.jpg", is_main=False)
        CarImage.objects.create(car=self.car, image="cars/img3.jpg", is_main=False)
        self.assertEqual(self.car.images.count(), 3)

    def test_main_image_first_in_ordering(self):
        CarImage.objects.create(car=self.car, image="cars/img1.jpg", is_main=False, order=0)
        CarImage.objects.create(car=self.car, image="cars/img2.jpg", is_main=True, order=1)
        first = self.car.images.first()
        self.assertTrue(first.is_main)

    def test_images_deleted_with_car(self):
        CarImage.objects.create(car=self.car, image="cars/img1.jpg")
        car_id = self.car.id
        self.car.delete()
        self.assertEqual(CarImage.objects.filter(car_id=car_id).count(), 0)

    def test_str_main_image(self):
        img = CarImage.objects.create(car=self.car, image="cars/img.jpg", is_main=True)
        self.assertIn("رئيسية", str(img))
