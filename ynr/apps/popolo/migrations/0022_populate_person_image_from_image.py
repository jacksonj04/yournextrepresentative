# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-20 11:22
from __future__ import unicode_literals

from django.db import migrations


def popolate_person_image_model(apps, schema_editor):
    """
    Add this migration here as it's part of the *[Extra] migration work
    and will be safe to delete as part of a migration clean up in future.

    That is, it won't generally be useful to new users of the codebase once
    the merging work is done, and it's nice to keep the migration tree smaller
    in the People app.
    """

    Person = apps.get_model("popolo", "Person")
    Image = apps.get_model("images", "Image")
    ContentType = apps.get_model("contenttypes", "ContentType")
    PersonImage = apps.get_model("people", "PersonImage")

    person_content_type_id = ContentType.objects.get_for_model(Person).pk
    image_qs = Image.objects.select_related("extra").filter(
        content_type_id=person_content_type_id
    )
    for image in image_qs:
        PersonImage.objects.create(
            person_id=image.object_id,
            image=image.image,
            source=image.source,
            copyright=image.extra.copyright,
            uploading_user=image.extra.uploading_user,
            user_notes=image.extra.user_notes,
            md5sum=image.extra.md5sum,
            user_copyright=image.extra.user_copyright,
            notes=image.extra.notes,
            is_primary=image.is_primary,
        )
    # Make sure we've copied all the images
    assert PersonImage.objects.count() == image_qs.count()


class Migration(migrations.Migration):

    dependencies = [
        ("popolo", "0021_auto_20180918_1534"),
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            popolate_person_image_model, migrations.RunPython.noop
        )
    ]
