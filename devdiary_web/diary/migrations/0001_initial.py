from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('minutes', models.PositiveIntegerField()),
                ('mood', models.CharField(choices=[('+', 'good'), ('=', 'ok'), ('-', 'bad')], default='=', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['-created_at'],
            },
        ),
    ]
