from django import forms
from django.contrib.auth.models import User, Group, Permission


# === EDICIÓN DE USUARIO (datos + roles) ===
class UserUpdateForm(forms.ModelForm):
    """El Administrador edita los datos y los roles de un usuario existente."""
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Roles',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'groups']
        labels = {
            'username':   'Usuario',
            'first_name': 'Nombres',
            'last_name':  'Apellidos',
            'email':      'Email',
            'is_active':  'Activo',
        }
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# === ROLES (Group) CON SUS PERMISOS ===
class GroupForm(forms.ModelForm):
    """Crear/editar un rol y marcar sus permisos con checkboxes."""
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type').order_by(
            'content_type__model', 'codename'
        ),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Permisos',
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {'name': 'Nombre del rol'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# === PERMISOS PERSONALIZADOS ===
class PermissionForm(forms.ModelForm):
    """Crear un permiso propio, ej: can_approve_invoice."""
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']
        labels = {
            'name':         'Nombre',
            'codename':     'Código',
            'content_type': 'Modelo asociado',
        }
        widgets = {
            'name':         forms.TextInput(attrs={'class': 'form-control'}),
            'codename':     forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
        }
