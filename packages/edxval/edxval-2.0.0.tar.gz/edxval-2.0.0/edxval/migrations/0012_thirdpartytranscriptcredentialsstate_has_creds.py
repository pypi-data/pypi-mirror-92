# Generated by Django 1.11.25 on 2019-12-03 05:48


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edxval', '0011_data__add_audio_mp3_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='thirdpartytranscriptcredentialsstate',
            name='has_creds',
            field=models.BooleanField(default=False, help_text='Transcript credentials state'),
        ),
    ]
