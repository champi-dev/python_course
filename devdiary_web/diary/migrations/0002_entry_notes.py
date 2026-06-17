from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
    ]
