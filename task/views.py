from django.shortcuts import render


def index(request):
    """View function for home page."""
    return render(request, "task/index.html")
