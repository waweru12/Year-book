from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Project, Profile, Rating
from .forms import ProfileForm, UploadForm, RatingForm
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='/accounts/login')
def index(request):
    current_user = request.user
    projects = Project.objects.order_by('-overall').all()
    top = projects[0]
    runners=Project.objects.all()[:4]
    try:
        current_user = request.user
        profile =Profile.objects.get(user=current_user)
    except ObjectDoesNotExist:
        return redirect('edit')
    return render(request, 'index.html', locals())

@login_required(login_url='/accounts/login')
def profile(request):
    current_user=request.user
    profile =Profile.objects.get(user=current_user)
    projects = Project.objects.filter(user=current_user)
    my_profile = Profile.objects.get(user=current_user)
    return render(request, 'profile.html', locals())

@login_required(login_url='/accounts/login')
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = current_user
            prof.save()
            return redirect('myprofile')
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', {'form': form, 'profile':profile})

@login_required(login_url='/accounts/login')
def new_project(request):
    current_user = request.user
    profile =Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
            return redirect('index')
    else:
        form = UploadForm()
    return render(request, 'new_project.html', {'form': form,'profile':profile})

@login_required(login_url='/accounts/login')
def project(request, project_id):
    current_user = request.user
    profile =Profile.objects.get(user=current_user)
    message = "Thank you for voting"
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise ObjectDoesNotExist()

   
   
    total_class_of_the_year = 0
    overall_score = 0

    ratings = Rating.objects.filter(project=project_id)
    if len(ratings) > 0:
        users = len(ratings)
    else:
        users = 1
    
    class_of_the_year = list(Rating.objects.filter(project=project_id).values_list('class_of_the_year',flat=True))
  
    
    total_class_of_the_year=sum(class_of_the_year)/users
    


    overall_score=(total_class_of_the_year)/1

    project.class_of_the_year = total_class_of_the_year
    project.overall = overall_score

    project.save()

    
    if request.method == 'POST':
        form = RatingForm(request.POST, request.FILES) 
        if form.is_valid():
            rating = form.save(commit=False)
            rating.project= project
            rating.profile = profile
            if not Rating.objects.filter(profile=profile, project=project).exists():
                rating.overall_score = (rating.class_of_the_year)/1
                rating.save()
    else:
        form = RatingForm()
    return render(request, "project.html",{"project":project,"profile":profile,"ratings":ratings,"form":form, "message":message, 'total_class_of_the_year':total_class_of_the_year, })

@login_required(login_url='/accounts/login')
def search(request):
    current_user = request.user
    profile =Profile.objects.get(user=current_user)
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        projects = Project.search_project(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message, "projects":projects, 'profile':profile})
    else:
        message = "Please enter search term"
        return render(request, 'search.html', {"message":message, "projects":projects,'profile':profile})
