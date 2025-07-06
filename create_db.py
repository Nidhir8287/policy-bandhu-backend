import os
import django
from django.contrib.auth import get_user_model

# Ensure the settings module is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Setup Django so that apps are ready
django.setup()

user = get_user_model()


def create_super_user():
    user.objects.create_user(
        email="admin@admin.com",
        password="akhu1234",
        name='Akhu',
        is_staff=True,
        is_superuser=True
    )
    return


def create_staff():
    user.objects.create(
        email='staff1@example.com',
        password='text31234',
        name='Staff 1'
    )
    user.objects.create(
        email='staff2@example.com',
        password='text21234',
        name='Staff 2'
    )
    user.objects.create(
        email='staff3@example.com',
        password='text11234',
        name='Staff 3'
    )


def create_user():
    user.objects.create(
        email='user1@example.com',
        password='text31234',
        name='User 1'
    )
    user.objects.create(
        email='user2@example.com',
        password='text21234',
        name='User 2'
    )
    user.objects.create(
        email='user3@example.com',
        password='text11234',
        name='User 3'
    )


def create_question():
    Question.objects.create(id=1, title='Sample Question 1')
    Question.objects.create(id=2, title='Sample Question 2')


def create_choice():
    skills = Skill.objects.all()
    questions = Question.objects.all()
    for i in range(8):
        choice = Choice.objects.create(
            id=i+1,
            choice_text="This is choice {}".format(i+1),
            question=questions[i//4])
        choice.skills.set(
            [skills[i % skills.count()], skills[(i+1) % skills.count()]])


def create_assessment():
    questions = Question.objects.all()
    users = user.objects.all()
    assessment = Assessment.objects.create(id=1, title='Sample Assessment 1')
    assessment.questions.set(questions)
    assessment.allowed_users.set(users)


if __name__ == "__main__":
    create_super_user()
    create_staff()
    create_user()
    create_question()
    create_choice()
    create_assessment()
