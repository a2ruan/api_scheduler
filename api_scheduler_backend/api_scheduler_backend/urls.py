"""api_scheduler_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Site level url that is first to recieve any REST API calls.  
# This is routed in the following sequence.
# urls.py (here) -> urls.py (in api folder) -> views.py (in api folder)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Default administrator website
    path('admin/', admin.site.urls),

    # Routing to main api urls.  For example, path("kk",include('api.urls')) will route to ../api/urls if contains kk in the url
    path('', include('api.urls'))
]



