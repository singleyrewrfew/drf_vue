from django.db import migrations, models
import django.db.models.deletion


def convert_role_to_fk(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Role = apps.get_model('roles', 'Role')
    
    role_mapping = {
        'admin': 'admin',
        'editor': 'editor',
        'user': 'user',
    }
    
    for user in User.objects.all():
        old_role = user.role
        if old_role and old_role in role_mapping:
            try:
                new_role = Role.objects.get(code=role_mapping[old_role])
                user.role = new_role
                user.save(update_fields=['role'])
            except Role.DoesNotExist:
                pass


class Migration(migrations.Migration):
    dependencies = [
        ('roles', '0002_init_default_data'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='roles.role', verbose_name='角色'),
        ),
        migrations.RunPython(convert_role_to_fk),
    ]
