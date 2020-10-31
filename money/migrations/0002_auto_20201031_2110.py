# Generated by Django 3.1.2 on 2020-10-31 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='money',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moneys_account', to='money.account'),
        ),
        migrations.AlterField(
            model_name='money',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moneys_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
