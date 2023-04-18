import json
import qrcode
import random
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pdb
# Create your views here.


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            total_product = ("Title: " + "\n" + product.title + "\n"+ "\n" + "📝: " + "\n" + product.description )
            qr.add_data(total_product)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)

            image_file = ContentFile(buffer.read())
            qr_code_file = InMemoryUploadedFile(image_file, None, 'qr_code.png', 'image/png', image_file.tell, None)
            
            #Important! Set the user field to the current user before saving the product instance
            product.user = request.user
            # Save QR code to product model
            product.qr_code.save(qr_code_file.name, qr_code_file, save=False)
            #Do NOT mute this product.save(), otherwise you get an error in html
            product.save()
            messages.success(request, "You got QR!")
            return redirect('allPosts')
        else:
            messages.error(request, "Insufficient info")
            return HttpResponseRedirect(reverse("index"))
    else:
        form = PostForm()

    return render(request, 'qr/index.html', {
          'form': form
        })
    


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        #Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("allPosts"))
        else:
            return render(request, "qr/login.html", {
                "message" : "Invalid username and/ or password."
            })
    else:
        return render(request, "qr/login.html")
    

# def logout_view(request):
#     username = get_object_or_404(User, username=request.user)
#     bye_message = ["Great job!", "Have a good one!", "Hasta la vista, baby!"]
#     bye_message = random.choice(bye_message)
   
#     logout(request)
#     return render(request, "qr/logout_view.html", {
#         "username" : username,
#         "bye_message" : bye_message
#     })
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Ensure pw matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "qr/register.html", {
                "message":"password must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "qr/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "qr/register.html")
    

def allPosts(request):
    all_posts = Post.objects.all().order_by("-create_date")
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render (request, "qr/allPosts.html",{
        "posts" : posts
    })


def post(request, post_id):
    post= Post.objects.get(pk=post_id)
    return render(request, "qr/post.html", {
        "post" : post
    })


def category(request):
    categories = Post.category.field.choices
    categories = [x[0] for x in categories]
    return render(request, "qr/category.html" ,{
        "categories" : categories
    })


def category_detail(request, category):
          # the left category is the attribute of the Product class, the right category is the category_detail function parameter 
          # which is comming in from the detail.html
          # And this line of code returns all the category related listings
          category_listings = Post.objects.filter(category=category).order_by("-create_date")
          return render(request, "qr/category_detail.html", {
        "category_listings" : category_listings,
        "category" : category
    })

@login_required
def createP(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Your profile has been successfully created!")
                return HttpResponseRedirect(reverse('index'))
            except IntegrityError:
                print(f"Hey!{profile.profile_picture}")
                return render(request, "qr/createP.html", {
                "message": "Your profile already exists"
            })
    else:
        form = ProfileForm()
    return render(request, 'qr/createP.html',{
        "form" : form
    })


def profile(request, username):
  try: 
    user = User.objects.get(username=username)
    userProfile = UserProfile.objects.get(user=user)
    all_user_posts = Post.objects.filter(user=user).order_by("-create_date")
    page = request.GET.get('page', 1)
    paginator = Paginator(all_user_posts, 5)
    try:
       posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "qr/profile.html", {
        "userProfile" : userProfile,
        "posts" : posts
    })
  except ObjectDoesNotExist:
      messages.error(request, "Create your profile here!")
      return HttpResponseRedirect(reverse("createP"))
      


def followToggle(request, username):
    authorObj = User.objects.get(username=username)
    currentUserObj = User.objects.get(username=request.user.username)
    following = authorObj.following.all()

    if username != currentUserObj.username:
        if currentUserObj in following:
            authorObj.following.remove(currentUserObj.id)
        else:
            authorObj.following.add(currentUserObj.id)
    else:
       messages.error(request, "Cannot follow yourself")        
    return HttpResponseRedirect(reverse(profile, args=[authorObj.username]))


@login_required
def following_page(request):
  try: 
    # pdb.set_trace()
    current_user = User.objects.get(pk=request.user.id)
    all_following_posts = Post.objects.filter(user__in=current_user.followers.all()).order_by('-create_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_following_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "qr/following_posts.html",{
        "posts" : posts
    })
  except:
     return render(request, "network/login.html") 

  
@csrf_exempt
def update_post(request, post_id):
    # pdb.set_trace()
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        body = data.get('body', '').strip()
        print(f"Hey!{request.POST}")
        if body:
            post.body = body
            post.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status':'error', 'message': 'Invalid request'})
       
    
@csrf_exempt
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user.is_authenticated and user not in post.likes.all():
        post.likes.add(user)
        like_count = post.likes.count()
        liked = True
        print(post_id)
        return JsonResponse({'success': True, 'like_count': like_count, 'liked': liked, 'status':f'{request.user} liked!'})
    else:
        liked = False
        return JsonResponse({'success': False, 'liked': liked})         
    
   
@csrf_exempt
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user.is_authenticated and user in post.likes.all():
        post.likes.remove(user)
        like_count = post.likes.count()
        liked = False
        return JsonResponse({'success': True, 'like_count': like_count, 'liked': liked, 'status':f'{request.user} Unliked!'})
    else:
        liked = False
        return JsonResponse({'success': False, 'liked': liked})
 
    
def backup(request):
    #Dump the database into a JSON string
    backup = json.dumps(list(Post.objects.all().values()), indent=4, sort_keys=True, default=str)
    # Create a file-like object to write the backup data to
    response = HttpResponse(content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="lyrics.json"'
    # Write the backup data to the response object
    response.write(backup)
    # Return the response object
    return response
