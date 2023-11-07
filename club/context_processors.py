# Reference: https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-your-own-context-processors


def club(request):

    context = {}

    # Display admin btn in the public interface:
    context["display_admin_btn"] = False
    if request.user.is_authenticated and request.user.is_active:
        context["display_admin_btn"] = True

    return context
