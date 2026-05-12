from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_product_is_case'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', imagekit.models.fields.ProcessedImageField(
                    upload_to='products/photos/%Y/%m',
                    verbose_name='Фото',
                )),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='photos',
                    to='products.product',
                    verbose_name='Продукт',
                )),
            ],
            options={
                'verbose_name': 'Фото продукта',
                'verbose_name_plural': 'Фото продуктов',
                'ordering': ['order'],
            },
        ),
    ]
