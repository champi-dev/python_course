from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_entry_notes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='author',
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='entries',
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
