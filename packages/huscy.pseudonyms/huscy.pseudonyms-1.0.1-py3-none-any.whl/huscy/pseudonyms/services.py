import uuid

from django.db import IntegrityError, transaction

from huscy.pseudonyms.models import Pseudonym


def _generate_code():
    return uuid.uuid1().hex


def create_pseudonym(subject, content_type, object_id=None):
    code = _generate_code()
    try:
        with transaction.atomic():
            return Pseudonym.objects.create(subject=subject, code=code, content_type=content_type,
                                            object_id=object_id)
    except IntegrityError:
        # try again if code is already in use
        return create_pseudonym(subject, content_type, object_id)


def get_pseudonym(subject, content_type, object_id=None):
    filters = {'subject': subject, 'content_type': content_type}
    if object_id:
        filters['object_id'] = object_id
    return Pseudonym.objects.get(**filters)


def get_or_create_pseudonym(subject, content_type, object_id=None):
    try:
        return get_pseudonym(subject, content_type, object_id)
    except Pseudonym.DoesNotExist:
        return create_pseudonym(subject, content_type, object_id)


def get_subject(pseudonym):
    return Pseudonym.objects.get(code=pseudonym).subject
