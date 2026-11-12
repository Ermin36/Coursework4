from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import CustomUser

class OwnerOnlyMixin(LoginRequiredMixin):
    """Пускает к объекту только его владельца. Чужие записи — 403."""
    owner_lookup = 'created_by'  # поле модели, где лежит владелец

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model.objects, pk=self.kwargs['pk'])

        if self.request.user.is_superuser:
            return obj

        if getattr(obj, self.owner_lookup) != self.request.user:
            raise PermissionDenied

        return obj


class ManagerMixin(LoginRequiredMixin):
    owner = 'created_by'
    perms = None

    def get_queryset(self):
        qs = super().get_queryset()
        user: CustomUser = self.request.user

        if user.is_superuser:
            return qs

        if self.perms:
            if all(user.has_perms(perm) for perm in self.perms):
                return qs

        return qs.filter(**{self.owner: user})
