from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_assignment_max_points_assignment_max_uploads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='test_result',
            field=models.TextField(blank=True, null=True),
        ),
    ]
