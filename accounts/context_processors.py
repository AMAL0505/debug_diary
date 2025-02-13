from accounts.models import UserProfile
from blogapp.models import Notification

def user_profile(request):
    user_id = request.session.get('user_id', None)
    
    # Debugging: Print session user_id
    print(f"Context Processor - User ID in Session: {user_id}")

    if user_id:
        try:
            profile = UserProfile.objects.get(id=user_id)
            notification_count = profile.received_notifications.filter(is_read=False).count()
            notifications = profile.received_notifications.filter(is_read=False).order_by('-created_at')[:5]
            context = {'userprofile': profile, 'notification_count': notification_count, 'notifications': notifications}

            # Debugging: Print profile username
            print(f"Context Processor - Found User: {profile.username}")
            return context
        except UserProfile.DoesNotExist:
            return {'userprofile': None}
    return {'userprofile': None}
