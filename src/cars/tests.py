from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse

from .models import Brand, Car, CarImage
from leads.models import TestDriveRequest, InspectionRequest


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


# ── Task 3.7: Car Detail Page Tests ────────────────────────────────────────

class UsedCarDetailViewTest(TestCase):
    def setUp(self):
        self.car = make_car(
            car_type=Car.CarType.USED,
            mileage_km=50000,
            transmission=Car.Transmission.AUTOMATIC,
            fuel_type=Car.FuelType.PETROL,
            engine_size="2.5L",
            exterior_color="أبيض",
            origin=Car.Origin.SAUDI,
            city="الرياض",
            price=80000,
            description="السيارة بحالة ممتازة",
        )
        self.url = reverse("cars:car_detail", args=[self.car.pk])

    def test_detail_page_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "cars/car_detail.html")

    def test_detail_page_shows_car_title(self):
        response = self.client.get(self.url)
        self.assertContains(response, "تويوتا")
        self.assertContains(response, "كامري")

    def test_detail_page_shows_price(self):
        response = self.client.get(self.url)
        self.assertContains(response, "80,000")

    def test_detail_page_shows_specs(self):
        response = self.client.get(self.url)
        self.assertContains(response, "50,000")  # mileage
        self.assertContains(response, "الرياض")  # city

    def test_detail_page_shows_inspection_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, "حجز معاينة")

    def test_detail_page_does_not_show_test_drive_form(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "حجز تجربة قيادة")

    def test_hidden_car_returns_404(self):
        hidden = make_car(model_name="مخفية", status=Car.Status.HIDDEN)
        response = self.client.get(reverse("cars:car_detail", args=[hidden.pk]))
        self.assertEqual(response.status_code, 404)

    def test_sold_car_returns_404(self):
        sold = make_car(model_name="مباعة", status=Car.Status.SOLD)
        response = self.client.get(reverse("cars:car_detail", args=[sold.pk]))
        self.assertEqual(response.status_code, 404)

    def test_inspection_form_submission_saves_request(self):
        response = self.client.post(self.url, {
            "name": "محمد العتيبي",
            "phone": "0501234567",
            "preferred_time": "الخميس صباحاً",
            "note": "",
        })
        self.assertEqual(response.status_code, 302)
        req = InspectionRequest.objects.get(car=self.car)
        self.assertEqual(req.name, "محمد العتيبي")
        self.assertEqual(req.phone, "0501234567")

    def test_inspection_form_submission_requires_name(self):
        response = self.client.post(self.url, {
            "name": "",
            "phone": "0501234567",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(InspectionRequest.objects.filter(car=self.car).exists())

    def test_inspection_form_submission_requires_phone(self):
        response = self.client.post(self.url, {
            "name": "محمد",
            "phone": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(InspectionRequest.objects.filter(car=self.car).exists())

    def test_inspection_request_linked_to_car(self):
        self.client.post(self.url, {
            "name": "أحمد",
            "phone": "0559876543",
        })
        req = InspectionRequest.objects.get(car=self.car)
        self.assertEqual(req.car, self.car)

    def test_success_message_after_submission(self):
        response = self.client.post(self.url, {
            "name": "سارة",
            "phone": "0551234567",
        }, follow=True)
        self.assertContains(response, "تم إرسال طلبك بنجاح")


class NewCarDetailViewTest(TestCase):
    def setUp(self):
        self.car = make_car(
            car_type=Car.CarType.NEW,
            trim="Luxury",
            features_summary="نظام ملاحة\nكاميرا خلفية\nمقاعد جلدية",
            price=150000,
            price_label="ابتداءً من",
        )
        self.url = reverse("cars:car_detail", args=[self.car.pk])

    def test_detail_page_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_shows_features(self):
        response = self.client.get(self.url)
        self.assertContains(response, "كاميرا خلفية")

    def test_detail_page_shows_test_drive_form(self):
        response = self.client.get(self.url)
        self.assertContains(response, "حجز تجربة قيادة")

    def test_detail_page_does_not_show_inspection_form(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "حجز معاينة")

    def test_test_drive_form_submission_saves_request(self):
        response = self.client.post(self.url, {
            "name": "فهد السبيعي",
            "phone": "0507654321",
            "preferred_time": "الأحد من 10 صباحاً",
            "note": "",
        })
        self.assertEqual(response.status_code, 302)
        req = TestDriveRequest.objects.get(car=self.car)
        self.assertEqual(req.name, "فهد السبيعي")

    def test_test_drive_request_linked_to_car(self):
        self.client.post(self.url, {
            "name": "نورة",
            "phone": "0561234567",
        })
        req = TestDriveRequest.objects.get(car=self.car)
        self.assertEqual(req.car, self.car)

    def test_price_label_shown(self):
        response = self.client.get(self.url)
        self.assertContains(response, "ابتداءً من")


class CarDetailLinkTest(TestCase):
    """Ensure the list pages contain links to the detail page."""

    def setUp(self):
        self.used_car = make_car(car_type=Car.CarType.USED)
        self.new_car = make_car(car_type=Car.CarType.NEW, model_name="كورولا")

    def test_used_list_links_to_detail(self):
        response = self.client.get(reverse("cars:used_list"))
        expected_url = reverse("cars:car_detail", args=[self.used_car.pk])
        self.assertContains(response, expected_url)

    def test_new_list_links_to_detail(self):
        response = self.client.get(reverse("cars:new_list"))
        expected_url = reverse("cars:car_detail", args=[self.new_car.pk])
        self.assertContains(response, expected_url)
