# Generated by Django 4.0.5 on 2022-07-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_addnotice_notice_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_statement', models.CharField(max_length=250)),
                ('option_a', models.CharField(max_length=70)),
                ('option_b', models.CharField(max_length=70)),
                ('option_c', models.CharField(max_length=70)),
                ('option_d', models.CharField(max_length=70)),
                ('answer', models.CharField(choices=[('Option A', 'a'), ('Option B', 'b'), ('Option C', 'c'), ('Option D', 'd')], max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='quizresult',
            name='post',
        ),
        migrations.RemoveField(
            model_name='quizresult',
            name='result_of',
        ),
        migrations.DeleteModel(
            name='QuesModel',
        ),
        migrations.DeleteModel(
            name='QuizPost',
        ),
        migrations.DeleteModel(
            name='QuizResult',
        ),
    ]
