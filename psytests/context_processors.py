def check_role(request):
    return {
        'is_counselor': request.user.groups.filter(name="Counselor").exists()
        }