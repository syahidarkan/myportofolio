import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        # data awal yang bersih buat tiap test, biar ga saling ganggu
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        # halaman profil ga boleh nampilin kartu pengalaman, itu punya halaman experience
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        # hapus semua data terus cek pesan kosongnya muncul
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        # kasih tanggal selesai, is_ongoing harusnya berubah jadi False
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="otwptn",
            description="University admissions consulting, built for the students who need it most.",
            tech_stack="Next.js 14 / Supabase / Resend",
            year=2025,
            project_url="https://otwptn.vercel.app",
            image="otwptn.jpg",
            is_featured=True,
            order=1,
        )

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_projects_page_shows_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)
        self.assertContains(response, str(self.project.year))

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_project_detail_url_is_accessible(self):
        response = self.client.get(reverse("main:show_project_detail", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")

    def test_project_detail_shows_correct_data(self):
        response = self.client.get(reverse("main:show_project_detail", args=[self.project.id]))

        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.tech_stack)

    def test_project_detail_404_for_invalid_id(self):
        response = self.client.get(reverse("main:show_project_detail", args=[uuid.uuid4()]))

        self.assertEqual(response.status_code, 404)

    def test_project_model_str(self):
        self.assertEqual(str(self.project), "otwptn")
        self.assertTrue(self.project.is_featured)
