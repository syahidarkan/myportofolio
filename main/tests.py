import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
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
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
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
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin_test", password="testpass123"))

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
        self.client.force_login(User.objects.create_superuser("admin_test", password="testpass123"))
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


class ProjectUpdateTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin_test", password="testpass123"))
        self.project = Project.objects.create(
            name="splitbill",
            description="Bill splitting tool.",
            tech_stack="React",
            year=2026,
        )
        self.url = reverse("main:update_project", args=[self.project.id])

    def test_update_project_get_prefills_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, 'value="splitbill"')

    def test_update_project_post_saves_changes(self):
        response = self.client.post(self.url, {
            "name": "Updated Project",
            "description": "Updated description",
            "tech_stack": "Next.js",
            "year": 2027,
            "project_url": "",
            "image": "",
        })

        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")
        self.assertEqual(self.project.year, 2027)

    def test_update_project_post_invalid_keeps_old_data(self):
        response = self.client.post(self.url, {"name": "", "description": "", "tech_stack": "", "year": ""})

        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "splitbill")

    def test_update_nonexistent_project_returns_404(self):
        response = self.client.get(reverse("main:update_project", args=[uuid.uuid4()]))

        self.assertEqual(response.status_code, 404)


class ExperienceFormTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin_test", password="testpass123"))
        self.experience = Experience.objects.create(
            title="GDGoC UI",
            description="Head of UI/UX Division.",
            category="volunteer",
            thumbnail="/static/img/exp-photos/gdgoc.jpg",
        )

    def test_create_experience_get_shows_form(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")

    def test_create_experience_post_saves_and_redirects(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "Test Experience",
            "description": "Test description",
            "category": "internship",
            "thumbnail": "",
            "ended_at": "",
        })

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Test Experience").exists())

    def test_create_experience_post_invalid_shows_error(self):
        count_before = Experience.objects.count()
        response = self.client.post(reverse("main:create_experience"), {
            "title": "",
            "description": "",
            "category": "",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experience.objects.count(), count_before)

    def test_update_experience_get_prefills_form(self):
        response = self.client.get(reverse("main:update_experience", args=[self.experience.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, 'value="GDGoC UI"')

    def test_update_experience_keeps_static_thumbnail_path(self):
        response = self.client.post(reverse("main:update_experience", args=[self.experience.id]), {
            "title": "GDGoC UI (edited)",
            "description": "Head of UI/UX Division.",
            "category": "volunteer",
            "thumbnail": "/static/img/exp-photos/gdgoc.jpg",
            "ended_at": "",
        })

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "GDGoC UI (edited)")

    def test_update_experience_can_set_end_date(self):
        response = self.client.post(reverse("main:update_experience", args=[self.experience.id]), {
            "title": self.experience.title,
            "description": self.experience.description,
            "category": "volunteer",
            "thumbnail": "",
            "ended_at": "2026-08-31T17:30",
        })

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertFalse(self.experience.is_ongoing)

    def test_update_form_prefills_end_date_in_datetime_local_format(self):
        self.experience.ended_at = timezone.now().replace(year=2026, month=8, day=31, hour=17, minute=30)
        self.experience.save()
        response = self.client.get(reverse("main:update_experience", args=[self.experience.id]))

        self.assertContains(response, 'value="2026-08-31T17:30"')

    def test_update_nonexistent_experience_returns_404(self):
        response = self.client.get(reverse("main:update_experience", args=[uuid.uuid4()]))

        self.assertEqual(response.status_code, 404)


class ExperienceDeleteTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin_test", password="testpass123"))
        self.experience = Experience.objects.create(
            title="Dihapus",
            description="Bakal dihapus di test ini.",
            category="internship",
        )

    def test_delete_experience_post_removes_it(self):
        response = self.client.post(reverse("main:delete_experience", args=[self.experience.id]))

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())

    def test_delete_experience_get_does_not_remove_it(self):
        self.client.get(reverse("main:delete_experience", args=[self.experience.id]))

        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

    def test_delete_nonexistent_experience_returns_404(self):
        response = self.client.post(reverse("main:delete_experience", args=[uuid.uuid4()]))

        self.assertEqual(response.status_code, 404)


class ExperienceDataDeliveryTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PandaTech",
            description="Founder.",
            category="full-time",
        )

    def test_get_experience_json_returns_json(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, self.experience.title)

    def test_get_experience_xml_returns_xml(self):
        response = self.client.get(reverse("main:get_experience_xml"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, self.experience.title)

    def test_experience_page_renders_from_deserialized_json(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, self.experience.title)
        self.assertContains(response, "Full-Time")


class AuthTest(TestCase):
    def test_register_get_shows_form(self):
        response = self.client.get(reverse("main:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_post_valid_creates_account_and_redirects_to_login(self):
        response = self.client.post(reverse("main:register"), {
            "username": "pengguna_baru",
            "password1": "kata-sandi-aman123",
            "password2": "kata-sandi-aman123",
        })

        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="pengguna_baru").exists())

    def test_register_post_password_mismatch_does_not_create_account(self):
        response = self.client.post(reverse("main:register"), {
            "username": "gagal_daftar",
            "password1": "kata-sandi-aman123",
            "password2": "beda-sekali456",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="gagal_daftar").exists())

    def test_login_get_shows_form(self):
        response = self.client.get(reverse("main:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_post_valid_redirects_and_sets_last_login_cookie(self):
        User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        response = self.client.post(reverse("main:login"), {
            "username": "sasha",
            "password": "kata-sandi-aman123",
        })

        self.assertRedirects(response, reverse("main:show_main"))
        self.assertIn("last_login", response.cookies)

    def test_login_post_wrong_password_shows_error(self):
        User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        response = self.client.post(reverse("main:login"), {
            "username": "sasha",
            "password": "salah-password",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "correct username and password")

    def test_navbar_shows_username_after_login(self):
        User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        self.client.login(username="sasha", password="kata-sandi-aman123")
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "sasha")
        self.assertContains(response, reverse("main:logout"))

    def test_navbar_shows_login_register_when_logged_out(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, reverse("main:login"))
        self.assertContains(response, reverse("main:register"))

    def test_logout_redirects_and_deletes_last_login_cookie(self):
        User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        self.client.login(username="sasha", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:logout"))

        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(response.cookies["last_login"].value, "")


class LastLoginCookieTest(TestCase):
    def test_show_main_without_cookie_shows_default_message(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "Belum ada sesi login")

    def test_show_main_reads_last_login_cookie(self):
        self.client.cookies["last_login"] = "2026-09-28 10:00:00"
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "2026-09-28 10:00:00")


class ProjectPermissionTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Proyek Terkunci",
            description="Buat tes otorisasi.",
            tech_stack="Django",
            year=2026,
        )

    def test_anonymous_create_project_redirects_to_login(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertRedirects(response, f"/login/?next={reverse('main:create_project')}")

    def test_regular_user_create_project_returns_403(self):
        User.objects.create_user(username="biasa", password="kata-sandi-aman123")
        self.client.login(username="biasa", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_create_project(self):
        User.objects.create_superuser("admin_test", password="kata-sandi-aman123")
        self.client.login(username="admin_test", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)

    def test_regular_user_delete_project_returns_403(self):
        User.objects.create_user(username="biasa", password="kata-sandi-aman123")
        self.client.login(username="biasa", password="kata-sandi-aman123")

        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    def test_anonymous_delete_experience_redirects_to_login(self):
        experience = Experience.objects.create(title="X", description="Y", category="internship")

        response = self.client.get(reverse("main:delete_experience", args=[experience.id]))

        self.assertRedirects(response, f"/login/?next={reverse('main:delete_experience', args=[experience.id])}")


class ProjectStarTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="otwptn",
            description="University admissions consulting.",
            tech_stack="Next.js",
            year=2025,
        )

    def test_anonymous_star_redirects_to_login(self):
        response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))

        self.assertRedirects(response, f"/login/?next={reverse('main:toggle_star', args=[self.project.id])}")
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_logged_in_user_can_star_and_unstar(self):
        user = User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        self.client.login(username="sasha", password="kata-sandi-aman123")

        self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertIn(user, self.project.starred_by.all())

        self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.project.refresh_from_db()
        self.assertNotIn(user, self.project.starred_by.all())

    def test_regular_user_does_not_need_to_be_superuser_to_star(self):
        User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        self.client.login(username="sasha", password="kata-sandi-aman123")

        response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))

        self.assertRedirects(response, reverse("main:show_projects"))

    def test_projects_json_shows_username_not_raw_id(self):
        user = User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        self.project.starred_by.add(user)

        response = self.client.get(reverse("main:get_projects_json"))

        self.assertContains(response, "sasha")
        self.assertNotContains(response, f'"starred_by": [{user.id}]')


class EditorRoleTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import Group

        self.editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor = User.objects.create_user(username="editor_user", password="kata-sandi-aman123")
        self.editor.groups.add(self.editor_group)

        self.project = Project.objects.create(
            name="Proyek Editor",
            description="Buat tes peran editor.",
            tech_stack="Django",
            year=2026,
        )
        self.experience = Experience.objects.create(
            title="Pengalaman Editor",
            description="Buat tes peran editor.",
            category="internship",
        )

    def test_editor_can_access_update_project(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:update_project", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)

    def test_editor_can_submit_update_project(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.post(reverse("main:update_project", args=[self.project.id]), {
            "name": "Proyek Editor (diubah)",
            "description": "Sudah diubah editor.",
            "tech_stack": "Django",
            "year": 2026,
            "project_url": "",
            "image": "",
        })

        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Proyek Editor (diubah)")

    def test_editor_cannot_create_project(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 403)

    def test_editor_cannot_delete_project(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    def test_editor_can_access_update_experience(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:update_experience", args=[self.experience.id]))

        self.assertEqual(response.status_code, 200)

    def test_editor_cannot_create_experience(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 403)

    def test_editor_cannot_delete_experience(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.post(reverse("main:delete_experience", args=[self.experience.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

    def test_regular_user_is_not_treated_as_editor(self):
        User.objects.create_user(username="biasa_saja", password="kata-sandi-aman123")
        self.client.login(username="biasa_saja", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:update_project", args=[self.project.id]))

        self.assertEqual(response.status_code, 403)

    def test_projects_page_marks_editor_in_context(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:show_projects"))

        self.assertTrue(response.context["is_editor"])
        self.assertContains(response, reverse("main:update_project", args=[self.project.id]))

    def test_editor_does_not_see_create_or_delete_buttons(self):
        self.client.login(username="editor_user", password="kata-sandi-aman123")

        response = self.client.get(reverse("main:show_projects"))

        self.assertNotContains(response, "TAMBAH PROYEK")
        self.assertNotContains(response, reverse("main:delete_project", args=[self.project.id]))

    def test_anonymous_is_editor_returns_false(self):
        from django.contrib.auth.models import AnonymousUser
        from main.views import is_editor

        self.assertFalse(is_editor(AnonymousUser()))


class CustomForbiddenPageTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="biasa_saja", password="kata-sandi-aman123")
        self.project = Project.objects.create(
            name="X", description="Y", tech_stack="Z", year=2026,
        )

    def test_403_uses_custom_template(self):
        from django.test import override_settings

        self.client.login(username="biasa_saja", password="kata-sandi-aman123")
        with override_settings(DEBUG=False):
            response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        self.assertContains(response, "Akses ditolak", status_code=403)


class ProjectJsonSecurityTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="otwptn", description="Y", tech_stack="Z", year=2025,
        )
        self.user = User.objects.create_user(username="sasha", password="kata-sandi-aman123")
        self.project.starred_by.add(self.user)

    def test_json_does_not_leak_password_hash(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertNotContains(response, "password")
        self.assertNotContains(response, self.user.password)

    def test_json_starred_by_uses_username_not_raw_id(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertContains(response, "sasha")
        self.assertNotContains(response, f'"starred_by": [{self.user.id}]')
