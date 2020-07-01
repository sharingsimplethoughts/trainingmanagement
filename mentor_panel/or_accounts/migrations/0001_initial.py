# Generated by Django 2.2.2 on 2019-07-10 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('icon', models.ImageField(upload_to='mentor_panel/category')),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_cover_image', models.ImageField(upload_to='mentor_panel/course/cover_image')),
                ('course_name', models.CharField(max_length=100)),
                ('course_desc', models.CharField(max_length=700)),
                ('is_free', models.BooleanField(default=False)),
                ('course_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=10)),
                ('course_offer', models.PositiveIntegerField(default=0)),
                ('course_offered_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=10)),
                ('is_certificate', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('total_duration_in_seconds', models.PositiveIntegerField(default=0)),
                ('total_number_of_videos', models.PositiveIntegerField(default=0)),
                ('rating', models.PositiveIntegerField(default=0)),
                ('course_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='c_category', to='or_accounts.Category')),
                ('course_mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='c_mentor', to='accounts.RegisteredUser')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('icon', models.ImageField(upload_to='mentor_panel/subcategory')),
                ('slug', models.SlugField(default='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sc_category', to='or_accounts.Category')),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_serial_no', models.PositiveIntegerField(default=0)),
                ('video_title', models.CharField(blank=True, max_length=100)),
                ('video_desc', models.CharField(blank=True, max_length=150)),
                ('video', models.FileField(upload_to='mentor_panel/course/video')),
                ('video_short_clip', models.FileField(upload_to='mentor_panel/course/video/video_short_clip')),
                ('video_cover_image', models.ImageField(upload_to='mentor_panel/course/video/video_cover_image')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('video_length_in_seconds', models.PositiveIntegerField(default=0)),
                ('rating', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cr_course', to='or_accounts.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_name', models.CharField(max_length=50)),
                ('cert', models.FileField(upload_to='mentor_panel/certificate')),
                ('cert_desc', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cert_course', to='or_accounts.Course')),
            ],
        ),
    ]