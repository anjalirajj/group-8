# Generated by Django 4.0 on 2022-01-16 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('display', '0022_alter_userprofile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issued_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='requested', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BookPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('transaction_status', models.CharField(default='defaults', max_length=50)),
                ('transaction_code', models.CharField(max_length=200)),
                ('transaction_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='BookOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('order_date', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.book')),
                ('issue_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.issued_status')),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='display.bookpayment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
