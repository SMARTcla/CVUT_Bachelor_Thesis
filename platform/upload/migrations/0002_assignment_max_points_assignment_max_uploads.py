from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='max_points',
            field=models.PositiveIntegerField(default=10, help_text='Maximum points for this assignment.'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='max_uploads',
            field=models.PositiveIntegerField(default=20, help_text='Maximum number of downloads for a student.'),
        ),
    ]
