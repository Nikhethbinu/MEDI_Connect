from django.db import migrations


# ==========================================
# DELETE ONLY OLD DOCTOR AVAILABILITY ROWS
# ==========================================

def delete_old_availability(apps, schema_editor):

    DoctorAvailability = apps.get_model(
        'doctors',
        'DoctorAvailability'
    )

    # Delete only rows from the DoctorAvailability table.
    DoctorAvailability.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        # Replace this with the actual migration name
        # generated in Step 2.
        ('doctors', '0005_add_availability_date'),
    ]

    operations = [
        migrations.RunPython(
            delete_old_availability,
            migrations.RunPython.noop
        ),
    ]