from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput

from main.models import Project


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
