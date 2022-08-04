# Generated by Django 3.0.6 on 2022-08-04 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebdjango', '0002_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='merge_ratings_book_datasets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('book_isbn', models.CharField(max_length=80)),
                ('book_rating', models.IntegerField(default=0)),
                ('book_title', models.CharField(max_length=250)),
                ('book_author', models.CharField(max_length=250)),
                ('publisher', models.CharField(max_length=250)),
                ('imagine_url_s', models.CharField(max_length=500)),
                ('imagine_url_m', models.CharField(max_length=500)),
                ('imagine_url_l', models.CharField(max_length=500)),
            ],
        ),
        migrations.DeleteModel(
            name='merge',
        ),
    ]