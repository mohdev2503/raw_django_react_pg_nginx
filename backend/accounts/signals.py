import os
from pathlib import Path
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_directory(sender, instance, created, **kwargs):
    """
    Signal to create a directory for the user based on their UUID after user creation.
    """
    if created:
        base_dir = Path('media/user_files')
        user_dir = base_dir / str(instance.id)
        user_dir.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {user_dir}")

