# Generated by Django 4.0.5 on 2022-07-29 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_quizquestion_remove_quizresult_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='answer',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=10),
        ),
    ]
