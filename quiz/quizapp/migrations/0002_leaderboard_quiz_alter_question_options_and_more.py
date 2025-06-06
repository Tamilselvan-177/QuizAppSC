# Generated by Django 5.1.4 on 2025-03-02 06:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highest_score', models.PositiveIntegerField()),
                ('last_attempt_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Leaderboard',
                'verbose_name_plural': 'Leaderboard',
                'ordering': ['-highest_score', 'last_attempt_date'],
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='quizattempt',
            options={'ordering': ['-attempt_date']},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': 'Topic', 'verbose_name_plural': 'Topics'},
        ),
        migrations.AlterModelOptions(
            name='userresponse',
            options={'verbose_name': 'User Response', 'verbose_name_plural': 'User Responses'},
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizapp.topic'),
        ),
        migrations.AlterField(
            model_name='quizattempt',
            name='attempt_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='quizattempt',
            name='score',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='selected_answer',
            field=models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1),
        ),
        migrations.AddConstraint(
            model_name='quizattempt',
            constraint=models.UniqueConstraint(fields=('user', 'topic'), name='unique_attempt_per_topic'),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.topic'),
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='quizapp.topic'),
        ),
    ]
