# Generated by Django 2.2.13 on 2020-11-06 15:23

from django.db import migrations, models
import django.db.models.deletion
import django_frontify.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontifyImagePluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_frontify_frontifyimagepluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('image', django_frontify.fields.FrontifyImageField(verbose_name='Image')),
                ('width', models.PositiveIntegerField(blank=True, help_text='The image width as number in pixels. Example: "720" and not "720px".', null=True, verbose_name='Width')),
                ('height', models.PositiveIntegerField(blank=True, help_text='The image height as number in pixels. Example: "720" and not "720px".', null=True, verbose_name='Height')),
                ('format', models.CharField(blank=True, choices=[(None, 'auto'), ('jpg', 'jpg'), ('jpeg', 'jpeg'), ('png', 'png')], max_length=10, verbose_name='Format')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]