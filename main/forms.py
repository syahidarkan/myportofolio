from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, DateTimeInput

from main.models import Experience, Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "tech_stack",
            "year",
            "project_url",
            "image",
        ]
        labels = {
            "name": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "year": "Tahun",
            "project_url": "URL Proyek",
            "image": "Nama Berkas Gambar",
        }
        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "otwptn",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Next.js / Supabase / Tailwind CSS",
                }
            ),
            "year": NumberInput(
                attrs={
                    "placeholder": "2025",
                    "min": 2000,
                    "max": 2100,
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://otwptn.vercel.app",
                }
            ),
            "image": TextInput(
                attrs={
                    "placeholder": "otwptn.jpg",
                }
            ),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]
        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "Gambar Thumbnail",
            "ended_at": "Tanggal Selesai (kosongkan kalau masih berlangsung)",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Head of UI/UX Division",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 4,
                }
            ),
            "thumbnail": TextInput(
                attrs={
                    "placeholder": "/static/img/exp-photos/gdgoc.jpg atau https://...",
                }
            ),
            # format T dibutuhin input datetime-local supaya nilai lama ikut ke-isi pas edit
            "ended_at": DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }
