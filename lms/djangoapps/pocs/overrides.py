"""
API related to providing field overrides for individual students.  This is used
by the individual due dates feature.
"""
import json

from .field_overrides import FieldOverrideProvider
from .models import StudentFieldOverride


class PersonalOnlineCoursesOverrideProvider(FieldOverrideProvider):
    """
    A concrete implementation of
    :class:`~courseware.field_overrides.FieldOverrideProvider` which allows for
    overrides to be made on a per user basis.
    """
    def get(self, block, name, default):
        poc = get_current_poc()
        if poc:
            return get_override_for_poc(self.user, block, name, default)
        return default


def get_current_poc():
    """
    TODO
    """
    return None


def get_override_for_poc(poc, block, name, default=None):
    """
    Gets the value of the overridden field for the `poc`.  `block` and `name`
    specify the block and the name of the field.  If the field is not
    overridden for the given poc, returns `default`.
    """
    try:
        override = StudentFieldOverride.objects.get(
            poc=poc,
            location=block.location,
            field=name)
        field = block.fields[name]
        return field.from_json(json.loads(override.value))
    except StudentFieldOverride.DoesNotExist:
        pass
    return default


def override_field_for_poc(poc, block, name, value):
    """
    Overrides a field for the `poc`.  `block` and `name` specify the block
    and the name of the field on that block to override.  `value` is the
    value to set for the given field.
    """
    override, _ = StudentFieldOverride.objects.get_or_create(
        poc=poc,
        location=block.location,
        field=name)
    field = block.fields[name]
    override.value = json.dumps(field.to_json(value))
    override.save()


def clear_override_for_poc(poc, block, name):
    """
    Clears a previously set field override for the `poc`.  `block` and `name`
    specify the block and the name of the field on that block to clear.
    This function is idempotent--if no override is set, nothing action is
    performed.
    """
    try:
        StudentFieldOverride.objects.get(
            poc=poc,
            location=block.location,
            field=name).delete()
    except StudentFieldOverride.DoesNotExist:
        pass
