from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SMSCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'SMS Kod',
                'verbose_name_plural': 'SMS Kodlar',
                'ordering': ['-created_at'],
            },
        ),
    ]
