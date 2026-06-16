from django.test import TestCase

from cars.models import Brand, Car
from .models import TestDriveRequest, InspectionRequest, ContactMessage, LeadStatus


def make_car(car_type=Car.CarType.NEW, **kwargs):
    brand, _ = Brand.objects.get_or_create(name="تويوتا")
    return Car.objects.create(
        brand=brand,
        car_type=car_type,
        model_name="لاندكروزر",
        year=2024,
        **kwargs,
    )


class TestDriveRequestTest(TestCase):
    def setUp(self):
        self.car = make_car(car_type=Car.CarType.NEW)

    def test_create_request(self):
        req = TestDriveRequest.objects.create(
            car=self.car,
            name="أحمد محمد",
            phone="0501234567",
            preferred_time="الخميس الصباح",
        )
        self.assertEqual(req.status, LeadStatus.NEW)
        self.assertIn("أحمد", str(req))

    def test_default_status_new(self):
        req = TestDriveRequest.objects.create(car=self.car, name="خالد", phone="0509999999")
        self.assertEqual(req.status, "new")

    def test_status_change(self):
        req = TestDriveRequest.objects.create(car=self.car, name="سامي", phone="0508888888")
        req.status = LeadStatus.CONTACTED
        req.save()
        self.assertEqual(TestDriveRequest.objects.get(pk=req.pk).status, "contacted")

    def test_internal_note(self):
        req = TestDriveRequest.objects.create(car=self.car, name="فهد", phone="0507777777")
        req.internal_note = "تم التواصل عبر الهاتف"
        req.save()
        self.assertEqual(TestDriveRequest.objects.get(pk=req.pk).internal_note, "تم التواصل عبر الهاتف")

    def test_car_optional(self):
        req = TestDriveRequest.objects.create(car=None, name="علي", phone="0506666666")
        self.assertIsNone(req.car)

    def test_ordering_newest_first(self):
        r1 = TestDriveRequest.objects.create(car=self.car, name="أول", phone="111")
        r2 = TestDriveRequest.objects.create(car=self.car, name="ثاني", phone="222")
        self.assertEqual(TestDriveRequest.objects.first(), r2)


class InspectionRequestTest(TestCase):
    def setUp(self):
        self.car = make_car(car_type=Car.CarType.USED)

    def test_create_request(self):
        req = InspectionRequest.objects.create(
            car=self.car,
            name="محمد علي",
            phone="0551234567",
            preferred_time="الأحد بعد الظهر",
        )
        self.assertEqual(req.status, LeadStatus.NEW)
        self.assertIn("معاينة", str(req))

    def test_car_nullable(self):
        req = InspectionRequest.objects.create(car=None, name="ناصر", phone="0559999999")
        self.assertIsNone(req.car)

    def test_status_closed(self):
        req = InspectionRequest.objects.create(car=self.car, name="بدر", phone="0558888888")
        req.status = LeadStatus.CLOSED
        req.save()
        self.assertEqual(InspectionRequest.objects.get(pk=req.pk).status, "closed")


class ContactMessageTest(TestCase):
    def test_create_with_phone(self):
        msg = ContactMessage.objects.create(
            name="سلمى",
            phone="0501111111",
            message="أريد الاستفسار عن سيارة",
        )
        self.assertEqual(msg.status, LeadStatus.NEW)
        self.assertIn("سلمى", str(msg))

    def test_create_with_email(self):
        msg = ContactMessage.objects.create(
            name="رانيا",
            email="rania@example.com",
            message="هل يتوفر لديكم فحص؟",
        )
        self.assertEqual(msg.email, "rania@example.com")

    def test_phone_and_email_both_optional(self):
        msg = ContactMessage.objects.create(name="زائر", message="رسالة")
        self.assertEqual(msg.phone, "")
        self.assertEqual(msg.email, "")

    def test_ordering_newest_first(self):
        ContactMessage.objects.create(name="أولى", message="م1")
        ContactMessage.objects.create(name="ثانية", message="م2")
        self.assertEqual(ContactMessage.objects.first().name, "ثانية")
