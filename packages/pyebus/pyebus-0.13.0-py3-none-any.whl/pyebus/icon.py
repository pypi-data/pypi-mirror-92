"""MDI Icon Utility."""
from . import types


def get_icon(fielddef, state=None):
    """Get Default Icon for `fielddef`."""
    type_ = fielddef.type_
    if fielddef.unit in ("°C", "K", "°F"):
        return "mdi:thermometer"
    elif isinstance(type_, (types.TimeType, types.DateType, types.DateTimeType, types.HourMinuteType)):
        return "mdi:timer"
    elif isinstance(type_, types.EnumType):
        if tuple(sorted(type_.values)) in [("off", "on"), ("no", "yes")]:
            if state in (False, "off", "no"):
                return "mdi:toggle-switch-off"
            else:
                return "mdi:toggle-switch"
    return None
