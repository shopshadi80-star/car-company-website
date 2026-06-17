from django.test import TestCase, Client
from django.urls import reverse

from cars.models import Brand, Car
from .models import TestDriveRequest, InspectionRequest, ContactMessage, LeadStatus
from .forms import TestDriveForm, InspectionForm, ContactForm


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


# ─── Form Validation Tests ───────────────────────────────────────────────────

class TestDriveFormTest(TestCase):
    def setUp(self):
        brand, _ = Brand.objects.get_or_create(name="تويوتا")
        self.car = Car.objects.create(brand=brand, car_type=Car.CarType.NEW, model_name="كامري", year=2024)

    def test_valid_form(self):
        form = TestDriveForm(data={"name": "أحمد", "phone": "0501234567", "preferred_time": "", "note": ""})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form = TestDriveForm(data={"name": "", "phone": "0501234567"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_phone(self):
        form = TestDriveForm(data={"name": "أحمد", "phone": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)


class InspectionFormTest(TestCase):
    def setUp(self):
        brand, _ = Brand.objects.get_or_create(name="تويوتا")
        self.car = Car.objects.create(brand=brand, car_type=Car.CarType.USED, model_name="كامري", year=2020)

    def test_valid_form(self):
        form = InspectionForm(data={"name": "محمد", "phone": "0559876543", "preferred_time": "", "note": ""})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form = InspectionForm(data={"name": "", "phone": "0559876543"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_phone(self):
        form = InspectionForm(data={"name": "محمد", "phone": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)


class ContactFormTest(TestCase):
    def test_valid_with_phone(self):
        form = ContactForm(data={"name": "سلمى", "phone": "0501111111", "email": "", "message": "استفسار"})
        self.assertTrue(form.is_valid())

    def test_valid_with_email(self):
        form = ContactForm(data={"name": "رانيا", "phone": "", "email": "r@test.com", "message": "مرحبا"})
        self.assertTrue(form.is_valid())

    def test_valid_with_both(self):
        form = ContactForm(data={"name": "خالد", "phone": "0501234567", "email": "k@test.com", "message": "سؤال"})
        self.assertTrue(form.is_valid())

    def test_no_contact_method_invalid(self):
        form = ContactForm(data={"name": "زائر", "phone": "", "email": "", "message": "رسالة"})
        self.assertFalse(form.is_valid())

    def test_missing_message_invalid(self):
        form = ContactForm(data={"name": "زائر", "phone": "0501234567", "email": "", "message": ""})
        self.assertFalse(form.is_valid())

    def test_missing_name_invalid(self):
        form = ContactForm(data={"name": "", "phone": "0501234567", "email": "", "message": "رسالة"})
        self.assertFalse(form.is_valid())


# ─── View / Integration Tests ─────────────────────────────────────────────────

class TestDriveViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        brand, _ = Brand.objects.get_or_create(name="هوندا")
        self.car = Car.objects.create(
            brand=brand, car_type=Car.CarType.NEW, model_name="سيفيك",
            year=2024, status=Car.Status.AVAILABLE,
        )
        self.url = reverse("cars:car_detail", args=[self.car.pk])

    def test_form_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "حجز تجربة قيادة")

    def test_valid_submission_saves_to_db(self):
        response = self.client.post(self.url, {
            "name": "فيصل", "phone": "0501112233", "preferred_time": "", "note": "",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TestDriveRequest.objects.count(), 1)
        req = TestDriveRequest.objects.first()
        self.assertEqual(req.car, self.car)
        self.assertEqual(req.name, "فيصل")

    def test_invalid_submission_no_save(self):
        response = self.client.post(self.url, {"name": "", "phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TestDriveRequest.objects.count(), 0)


class InspectionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        brand, _ = Brand.objects.get_or_create(name="نيسان")
        self.car = Car.objects.create(
            brand=brand, car_type=Car.CarType.USED, model_name="باترول",
            year=2019, status=Car.Status.AVAILABLE,
        )
        self.url = reverse("cars:car_detail", args=[self.car.pk])

    def test_form_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "حجز معاينة")

    def test_valid_submission_saves_to_db(self):
        response = self.client.post(self.url, {
            "name": "نورة", "phone": "0556667788", "preferred_time": "الاثنين", "note": "",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(InspectionRequest.objects.count(), 1)
        req = InspectionRequest.objects.first()
        self.assertEqual(req.car, self.car)

    def test_invalid_submission_missing_phone(self):
        response = self.client.post(self.url, {"name": "نورة", "phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InspectionRequest.objects.count(), 0)


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("leads:contact")

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تواصل معنا")

    def test_valid_submission_saves_to_db(self):
        response = self.client.post(self.url, {
            "name": "عبدالله", "phone": "0509998877", "email": "", "message": "أريد الاستفسار عن سيارة",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, "عبدالله")
        self.assertEqual(msg.status, LeadStatus.NEW)

    def test_no_contact_method_invalid(self):
        response = self.client.post(self.url, {
            "name": "زائر", "phone": "", "email": "", "message": "رسالة بدون وسيلة تواصل",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_missing_message_invalid(self):
        response = self.client.post(self.url, {
            "name": "زائر", "phone": "0501234567", "email": "", "message": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_submission_with_email_only(self):
        response = self.client.post(self.url, {
            "name": "ليلى", "phone": "", "email": "layla@example.com", "message": "رسالة بالبريد",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_saved_message_appears_in_admin_queryset(self):
        ContactMessage.objects.create(name="إدارة", phone="0501234567", message="رسالة")
        self.assertEqual(ContactMessage.objects.count(), 1)
