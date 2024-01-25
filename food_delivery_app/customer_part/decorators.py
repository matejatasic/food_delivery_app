from django.shortcuts import render, redirect


def anonimity_required(redirect_to):
    """This decorator redirects authenticated users to the designated route"""

    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper
