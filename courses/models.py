from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    title = models.CharField(max_length=200)

    content = models.TextField()

    video = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title



class Enrollment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Progress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)



class Certificate(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)



class Comment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    text = models.TextField()

    date = models.DateTimeField(auto_now_add=True)



class Rating(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    score = models.IntegerField()




class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Resource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"


