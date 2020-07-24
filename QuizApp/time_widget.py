from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration

class DurationInput(TextInput):

    def _format_value(self, value):
        duration = parse_duration(value)

        seconds = duration.seconds

        minutes = seconds // 60
        seconds = seconds % 60

        minutes = minutes % 60

        return '{:02d}:{:02d}'.format(minutes, seconds)