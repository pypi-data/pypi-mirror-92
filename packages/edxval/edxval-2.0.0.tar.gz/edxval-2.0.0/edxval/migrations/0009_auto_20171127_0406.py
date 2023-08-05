# Generated by Django 1.11.7 on 2017-11-27 09:06


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edxval', '0008_remove_subtitles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcriptpreference',
            name='three_play_turnaround',
            field=models.CharField(blank=True, choices=[('extended', '10-Day/Extended'), ('standard', '4-Day/Standard'), ('expedited', '2-Day/Expedited'), ('rush', '24 hour/Rush'), ('same_day', 'Same Day'), ('two_hour', '2 Hour')], max_length=20, null=True, verbose_name='3PlayMedia Turnaround'),
        ),
    ]
