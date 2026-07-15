from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Extends the default Django User model with a bio and profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __cloned_profile_pic(self):
        # Fallback helper if no profile pic is uploaded
        if self.profile_picture:
            return self.profile_picture.url
        return 'https://via.placeholder.com/150'

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signals to automatically create or update the Profile when a User is created/saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
    """
    Simple tags to organize photos (e.g., 'Nature', 'Portrait', 'Abstract').
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='photos')
    
    # Interactions: tracking which users liked or disliked
    likes = models.ManyToManyField(User, blank=True, related_name='liked_photos')
    dislikes = models.ManyToManyField(User, blank=True, related_name='disliked_photos')

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()