import uuid


def upload_to(instance, filename):

    extension = filename.split('.')[-1]

    instance_slug = getattr(instance, 'slug', False)
    if not instance_slug:
        instance_slug = str(uuid.uuid4()).replace('-', '')

    return (
        f'{instance._meta.app_label}/'
        f'images/{instance_slug}.{extension}'
    )
