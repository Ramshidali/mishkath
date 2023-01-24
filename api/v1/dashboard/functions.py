from users.models import Profile


def get_student_batch(request):
    student_instance = None
    
    if Profile.objects.filter(user=request.user):
        student_instance= Profile.objects.get(user=request.user)
        if student_instance.grade_batch :
            return student_instance.grade_batch.batch.pk
        else:
            print("no batch")
            return False
    else:
        return student_instance
    
def get_student_grade(request):
    student_instance = None
    
    if Profile.objects.filter(user=request.user):
        student_instance= Profile.objects.get(user=request.user)
        return student_instance.grade_batch.grade.pk
    else:
        return student_instance