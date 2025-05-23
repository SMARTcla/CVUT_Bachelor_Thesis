def is_teacher_context(request):
    if request.user.is_authenticated:
        is_teacher_flag = request.user.is_superuser or request.user.groups.filter(name="Teachers").exists()
    else:
        is_teacher_flag = False

    return {
        'is_teacher_flag': is_teacher_flag
    }