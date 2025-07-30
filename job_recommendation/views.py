from django.shortcuts import render

# View for the Home Page
def home_view(request):
    return render(request, 'index.html')
    # Renders the main landing page with Login, Register, About Us buttons

# View for the About Us Page
def about_view(request):
    return render(request, 'about.html', {
        'nav_mode': 'about_page'  # ✅ Shows Home, Login, and Register only
    })
    # Renders the About Us page with 3 interactive circles and detailed info
