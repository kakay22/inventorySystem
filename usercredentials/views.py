from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def main(request):
    username=''
    password=''
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Check if the user is an admin superuser
                login(request, user)
                return redirect('dashboard')  # Replace 'admin_dashboard' with the actual admin URL
            else:
                messages.error(request, "You are not authorized to access this page.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'main.html', {'username':username, 'password':password})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Redirect to the login page or homepage after logout
    return redirect('main')  # Replace 'login' with the name of your login URL pattern
