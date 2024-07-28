from django.shortcuts import render,redirect
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from field.forms import *
from .models import Post,Comment,UserProfile,ThreadModel,MessageModel
from django.views import View
from . forms import *
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin




class Home(View):
	def get(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_on')

		context = {
			'posts':posts
		}
		return render(request, 'blogapp/home.html',context)

class Base(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'blogapp/base.html')

class Audiovideo(LoginRequiredMixin,View):
	def get(self, request, *args, **kwargs):
		return render(request, 'blogapp/audiovideo.html')



class Graphics(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'blogapp/graphics.html')

def signin(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		user = authenticate(username=username,password=password1)

		if user is not None:
			login(request,user)
			
			return redirect('home')

		else:
			messages.error(request,'Bad authenticate')
			return redirect('signin')


	return render(request,'blogapp/signin.html')

def signup(request):
	if request.method == 'POST':
		username=request.POST['username']
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		email=request.POST['username']
		password1=request.POST['password1']
		password2=request.POST['password2']

		myuser=User.objects.create_user(username,email,password1)
		myuser.first_name=firstname
		myuser.last_name=lastname
		myuser.save()
		messages.success(request,'You registered successfully')
		return redirect('signin')
	return render(request,'blogapp/signup.html')

def signout(request):
	logout(request)
	messages.success(request,"you logged out successfully")
	return redirect('home')
	return render(request,'blogapp/signout.html')


 

class Posts(View):
	def get(self, request, *args, **kwargs):
		form = PostForm()

		context = {
			'form':form
		}
		return render(request, 'blogapp/posts.html',context)

	def post(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm(request.POST, request.FILES)

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

		context = {
			'form':form,
			'posts':posts
		}
		return render(request, 'blogapp/posts.html',context)

class PostDetail(View):
	def get(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm()
		comments = Comment.objects.filter(post=post).order_by('-created_on')
		context = {
			'post':post,
			'form':form,
			'comments':comments
		}
		return render(request, 'blogapp/postdetail.html',context)

	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()

		comments = Comment.objects.filter(post=post).order_by('-created_on')
		context = {
			'post':post,
			'form':form,
			'comments':comments
		}
		return render(request, 'blogapp/postdetail.html',context)

class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['body']
	template_name = 'blogapp/postedit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('postdetail',kwargs={'pk':pk})

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'blogapp/postdelete.html'  
	success_url = reverse_lazy('home')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'blogapp/commentdelete.html'

	def get_success_url(self):
		pk = self.kwargs['post_pk']
		return reverse_lazy('postdetail',kwargs={'pk':pk})

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


class ProfileView(LoginRequiredMixin,View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = profile.user
		posts = Post.objects.filter(author=user).order_by('-created_on')

		followers = profile.followers.all()

		if len(followers) == 0:
			is_following = False

		for follower in followers:
			if follower == request.user:
				is_following = True
				break
			else:
				is_following = False

		number_of_followers = len(followers)
		context = {
			'user':user,
			'posts':posts,
			'profile':profile,
			'number_of_followers':number_of_followers,
			'is_following':is_following
		}
		return render(request, 'blogapp/profile.html',context)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = UserProfile
	form_class = UserProfileForm
	template_name = 'blogapp/profile_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('profile',kwargs={'pk':pk})

    #test if user go ahead if no pagenotfound
	def test_func(self):
		profile = self.get_object()
		return self.request.user == profile.user


class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.add(request.user)

		return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.remove(request.user)

		return redirect('profile', pk=profile.pk)


class AddLike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)

		is_dislike = False

		for dislike in post.dislikes.all():
			if dislike == request.user:
				is_dislike = True
				break
		if is_dislike:
			post.dislikes.remove(request.user)

		is_like = False

		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break

		if not is_like:
			post.likes.add(request.user)

		if is_like:
			post.likes.remove(request.user)

		next = request.POST.get('next','/')
		return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)

		is_like = False

		for like in post.likes.all():
			if like == request.user:
				is_like = True
				break
		if is_like:
			post.likes.remove(request.user)

		is_dislike = False

		for dislike in post.dislikes.all():
			if dislike == request.user:
				is_dislike = True
				break

		if not is_dislike:
			post.dislikes.add(request.user)

		if is_dislike:
			post.dislikes.remove(request.user)

		next = request.POST.get('next','/')
		return HttpResponseRedirect(next)

class ListFollowers(View):
	def get(self,request,pk,*args,**kwargs):
		profile = UserProfile.objects.get(pk=pk)
		followers = profile.followers.all()

		context = {
			'profile':profile,
			'followers':followers,
		}
		return render(request, 'blogapp/followers_list.html', context)


# chatting sms ==========================================

class ListThreads(View):
	def get(self, request, *args, **kwargs):
		threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

		context = {
			'threads':threads
		}
		return render(request, 'blogapp/inbox.html',context)

class CreateThread(View):
	def get(self,request,*args,**kwargs):
		form = ThreadForm()

		context = {
			'form':form
		}
		return render(request, 'blogapp/create_thread.html',context)


	def post(self,request,*args,**kwargs):
		form = ThreadForm(request.POST)

		username = request.POST.get('username')

		try:
			receiver = User.objects.get(username=username)
			if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
				thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
				return redirect('thread', pk=thread.pk)
			elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
					thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
					return redirect('thread', pk=thread.pk)

			if form.is_valid():
				thread = ThreadModel(
						user = request.user,
						receiver=receiver
					)
				thread.save()

				return redirect('thread', pk=thread.pk)
		except:
			messages.error(request, 'Invalid username')
			return redirect('create-thread')

class ThreadView(View):
	def get(self, request, pk, *args, **kwargs):
		form = MessageForm()
		thread = ThreadModel.objects.get(pk=pk)
		message_list = MessageModel.objects.filter(thread__pk__contains=pk)
		context = {
			'thread':thread,
			'form':form,
			'message_list':message_list,
		}
		return render(request, 'blogapp/thread.html', context)

class CreateMessage(View):
	def post(self, request, pk, *args, **kwargs):
		#add image
		form = MessageForm(request.POST,request.FILES)
		##############
		thread = ThreadModel.objects.get(pk=pk)

		if thread.receiver == request.user:
			receiver = thread.user
		else:
			receiver = thread.receiver


		#add image
		if form.is_valid():
			message = form.save(commit=False)
			message.thread = thread
			message.sender_user = request.user
			message.receiver_user = receiver
			message.save()
		##########################

		return redirect('thread', pk=pk)
# end of chatting sms ==========================================




# trial
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # or wherever you want to redirect after saving
    else:
        form = ArticleForm()
    return render(request, 'blogapp/create_article.html', {'form': form})

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blogapp/article_list.html', {'articles': articles})