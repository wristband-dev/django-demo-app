from django.contrib.auth.models import Group, User
from wristband.django_auth import CallbackData, DefaultWristbandAuthBackendAdapter


class MyWristbandAdapter(DefaultWristbandAuthBackendAdapter):
    """
    Custom adapter with role mapping logic.
    """

    def populate_user(self, user: User, callback_data: CallbackData, **kwargs: object) -> User:
        # First, populate basic fields from parent (optional)
        user = super().populate_user(user, callback_data, **kwargs)

        # Now add custom role mapping (requires 'roles' scope)
        user_info = callback_data.user_info
        roles = user_info.roles

        if not roles:
            # No roles scope or no roles assigned - default permissions
            user.groups.clear()
            user.is_staff = False
            user.is_superuser = False
            viewer_group, _ = Group.objects.get_or_create(name="Viewers")
            user.groups.add(viewer_group)
        else:
            # Check for owner role
            role_names = [role.name for role in roles]
            has_owner_role = any(
                role_name.startswith("app:") and role_name.endswith(":owner") for role_name in role_names
            )

            if has_owner_role:
                user.groups.clear()
                user.is_staff = True
                user.is_superuser = True
                owner_group, _ = Group.objects.get_or_create(name="Owners")
                user.groups.add(owner_group)
            else:
                user.groups.clear()
                user.is_staff = False
                user.is_superuser = False
                viewer_group, _ = Group.objects.get_or_create(name="Viewers")
                user.groups.add(viewer_group)

        return user
