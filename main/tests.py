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

    def test_search_by_title_filters_results(self):
        Project.objects.create(
            name="splitbill.online",
            description="Split a bill in under a minute.",
            tech_stack="React",
            year=2026,
        )
        response = self.client.get(reverse("main:show_projects"), {"title": "split"})

        self.assertContains(response, "splitbill.online")
        self.assertNotContains(response, self.project.name)

    def test_search_with_no_match_shows_empty_message(self):
        response = self.client.get(reverse("main:show_projects"), {"title": "gakadaproyekginian"})

        self.assertContains(response, "gakadaproyekginian")


class ProjectFormTest(TestCase):
    def test_create_project_get_shows_form(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")

    def test_create_project_post_saves_and_redirects(self):
        response = self.client.post(reverse("main:create_project"), {
            "name": "Proyek Baru",
            "description": "Deskripsi proyek baru.",
            "tech_stack": "Django",
            "year": 2026,
            "project_url": "",
            "image": "",
        })

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(name="Proyek Baru").exists())

    def test_create_project_post_invalid_shows_error(self):
        response = self.client.post(reverse("main:create_project"), {
            "name": "",
            "description": "",
            "tech_stack": "",
            "year": "",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.exists())


class ProjectDeleteTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Proyek Dihapus",
            description="Bakal dihapus di test ini.",
            tech_stack="Django",
            year=2026,
        )

    def test_delete_project_post_removes_it(self):
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_delete_project_get_does_not_remove_it(self):
        self.client.get(reverse("main:delete_project", args=[self.project.id]))

        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    def test_delete_nonexistent_project_returns_404(self):
        response = self.client.post(reverse("main:delete_project", args=[uuid.uuid4()]))

        self.assertEqual(response.status_code, 404)


class ProjectDataDeliveryTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="otwptn",
            description="University admissions consulting.",
            tech_stack="Next.js",
            year=2025,
        )

    def test_get_projects_json_returns_json(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, self.project.name)

    def test_get_projects_xml_returns_xml(self):
        response = self.client.get(reverse("main:get_projects_xml"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, self.project.name)
