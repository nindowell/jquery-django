import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

from django.conf import settings
from gemini.models import Post
from faker import Faker

fake = Faker()
fake_ru = Faker('ru_RU')

def create_posts():
    for _ in range(1000):
        title = fake.sentence().replace('.', '')
        content = fake.paragraph(nb_sentences=3)
        post = Post(title=title, title_ru=fake_ru.sentence(nb_words=4), content=content)
        post.save()

if __name__ == "__main__":
    create_posts()
