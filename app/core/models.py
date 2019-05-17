from django.db import models
from user.models import User

NOTE_CHOICES = (
    (-1, 'Not evaluated'),
    (0, 'Failed'),
    (1, 'Failed Plus'),
    (2, 'Passed'),
    (3, 'Passed Good'),
    (4, 'Passed Very Good'),
    (5, 'Passed Excellent'),
)


class Exam(models.Model):
    name = models.CharField(unique=True, max_length=128)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    is_evaluated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class OpenQuestion(models.Model):
    question = models.CharField(unique=True, max_length=256, blank=False)
    answer = models.CharField(max_length=256, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    max_points = models.IntegerField(default=1, blank=False)

    class Meta:
        unique_together = ['question', 'exam']

    def __str__(self):
        return self.question


class OpenAnswer(models.Model):
    student_answer = models.TextField(blank=True)
    assigned_points = models.IntegerField(blank=True)
    assigned_comment = models.TextField(blank=True)

    question = models.OneToOneField(OpenQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class CloseQuestion(models.Model):
    question = models.CharField(unique=True, max_length=256)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    max_points = models.IntegerField(default=1)

    class Meta:
        unique_together = ['question', 'exam']

    def __str__(self):
        return self.question

    @property
    def valid_choices(self):
        return self.closechoice_set.all().filter(is_true=True).count()


class CloseChoice(models.Model):
    choice = models.CharField(max_length=256)
    is_true = models.BooleanField()
    close_question = models.ForeignKey(CloseQuestion, on_delete=models.CASCADE)


    def __str__(self):
        return self.choice


class UserExam(models.Model):
    note = models.IntegerField(choices=NOTE_CHOICES, blank=True)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    exams = models.ManyToManyField(Exam)

    def __str__(self):
        return f"{self.user.last_name}: {self.note}"
