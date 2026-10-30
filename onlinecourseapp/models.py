class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.TextField()  # Must be TextField
    grade = models.IntegerField(default=50)  # Default must be 50

    def __str__(self):
        return f"Question: {self.question_text}"

    def is_get_grade(self, selected_ids):
        all_correct = self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        selected_ids = set(selected_ids)
        if set(all_correct) == selected_ids:
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)  # max_length=200
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.choice_text} (Correct: {self.is_correct})"


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        # Must include enrollment and id
        return f"Submission ID: {self.id}, Enrollment: {self.enrollment}"
