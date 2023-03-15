# Generated by Django 3.2.13 on 2022-06-15 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_auto_20211015_0837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalpost',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical post', 'verbose_name_plural': 'historical posts'},
        ),
        migrations.AddField(
            model_name='historicalpost',
            name='collectible_tag_code',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='collectible_tag_code',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpost',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalpost',
            name='type',
            field=models.CharField(choices=[('post', 'Текст'), ('intro', '#intro'), ('link', 'Ссылка'), ('question', 'Вопрос'), ('idea', 'Идея'), ('project', 'Проект'), ('event', 'Событие'), ('battle', 'Батл'), ('weekly_digest', 'Журнал Клуба'), ('guide', 'Путеводитель'), ('thread', 'Тред')], db_index=True, default='post', max_length=32),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('post', 'Текст'), ('intro', '#intro'), ('link', 'Ссылка'), ('question', 'Вопрос'), ('idea', 'Идея'), ('project', 'Проект'), ('event', 'Событие'), ('battle', 'Батл'), ('weekly_digest', 'Журнал Клуба'), ('guide', 'Путеводитель'), ('thread', 'Тред')], db_index=True, default='post', max_length=32),
        ),
    ]
