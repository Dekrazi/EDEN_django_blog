# Generated by Django 4.2 on 2023-05-10 08:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("eden", "0003_alter_comment_author"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="created",
        ),
        migrations.AddField(
            model_name="comment",
            name="date_posted",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="eden.post",
            ),
        ),
    ]
