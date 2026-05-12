from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('photo', imagekit.models.fields.ProcessedImageField(
                    blank=True,
                    upload_to='hits/photos/%Y/%m',
                    verbose_name='Фото',
                )),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Скрыт')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Очередность')),
            ],
            options={
                'verbose_name': 'Хит продаж',
                'verbose_name_plural': 'Хиты продаж',
                'ordering': ['order'],
            },
        ),
    ]
