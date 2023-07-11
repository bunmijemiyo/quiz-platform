from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.TextField()


class AnswerChoice(models.Model):
    # The available choices for the answer
    CHOICES = (
        ('a', 'Choice A'),
        ('b', 'Choice B'),
        ('c', 'Choice C'),
        ('d', 'Choice D'),
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1, choices=CHOICES)
    text = models.CharField(max_length=255)
    # New field to indicate correctness
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Make sure only one choice is marked as correct per question
        if self.is_correct:
            AnswerChoice.objects.filter(
                question=self.question).update(is_correct=False)

        super().save(*args, **kwargs)


