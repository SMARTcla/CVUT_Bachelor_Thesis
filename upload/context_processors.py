# upload/context_processors.py

def is_teacher_context(request):
    """
    Возвращает флаг is_teacher_flag, который показывает, является ли пользователь учителем.
    """
    if request.user.is_authenticated:
        is_teacher_flag = request.user.is_superuser or request.user.groups.filter(name="Teachers").exists()
    else:
        is_teacher_flag = False

    return {
        'is_teacher_flag': is_teacher_flag
    }