from django.db import models
import random
# Create your models here.
COURSES=(('1','BCA'),('2','MCA'))

class Students(models.Model):
    enrollment_no=models.CharField(max_length=30)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    dateTime=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(default=1)
    course=models.CharField(max_length=10,choices=COURSES,default=1)
    image=models.FileField(blank=True,null=True)

    def save(self,*args,**kwargs):
        if self.enrollment_no=='' or self.enrollment_no==None:
            course=self.get_course_display()
            self.enrollment_no=course+"11001"+str(random.randrange(100, 999))
            # print(self.enrollment_no)
        super(Students, self).save(*args, **kwargs)

    def __str__(self) :
        return f"id{self.id}.{self.first_name}"
    

