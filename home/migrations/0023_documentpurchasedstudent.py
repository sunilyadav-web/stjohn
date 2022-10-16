# Generated by Django 4.0.5 on 2022-10-16 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_rename_discription_downloaddocument_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPurchasedStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=300)),
                ('payment_id', models.CharField(max_length=300)),
                ('signature', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('status', models.BooleanField(default=False)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.downloaddocument')),
            ],
        ),
    ]
