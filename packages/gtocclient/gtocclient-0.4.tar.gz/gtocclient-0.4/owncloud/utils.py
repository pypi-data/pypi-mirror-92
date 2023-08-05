# -*- coding: utf-8 -*-
#
# vim: expandtab shiftwidth=4 softtabstop=4
#
"""ownCloud util module

"""

import six
import datetime


def timedelta_to_seconds(delta):
    '''Convert a timedelta to seconds with the microseconds as fraction
    Note that this method has become largely obsolete with the
    `timedelta.total_seconds()` method introduced in Python 2.7.
    '''
    # Only convert to float if needed
    if delta.microseconds:
        total = delta.microseconds * 1e-6
    else:
        total = 0
    total += delta.seconds
    total += delta.days * 60 * 60 * 24
    return total


def format_time(timestamp, precision=datetime.timedelta(seconds=1)):
    '''Formats timedelta/datetime/seconds
    '''
    precision_seconds = precision.total_seconds()

    if isinstance(timestamp, six.string_types + six.integer_types + (float, )):
        try:
            castfunc = six.integer_types[-1]
            timestamp = datetime.timedelta(seconds=castfunc(timestamp))
        except OverflowError:  # pragma: no cover
            timestamp = None

    if isinstance(timestamp, datetime.timedelta):
        seconds = timestamp.total_seconds()
        # Truncate the number to the given precision
        seconds = seconds - (seconds % precision_seconds)

        return str(datetime.timedelta(seconds=seconds))
    elif isinstance(timestamp, datetime.datetime):  # pragma: no cover
        # Python 2 doesn't have the timestamp method
        if hasattr(timestamp, 'timestamp'):
            seconds = timestamp.timestamp()
        else:
            seconds = timedelta_to_seconds(timestamp - epoch)

        # Truncate the number to the given precision
        seconds = seconds - (seconds % precision_seconds)

        try:  # pragma: no cover
            if six.PY3:
                dt = datetime.datetime.fromtimestamp(seconds)
            else:
                dt = datetime.datetime.utcfromtimestamp(seconds)
        except ValueError:  # pragma: no cover
            dt = datetime.datetime.max
        return str(dt)
    elif isinstance(timestamp, datetime.date):
        return str(timestamp)
    elif timestamp is None:
        return '--:--:--'
    else:
        raise TypeError('Unknown type %s: %r' % (type(timestamp), timestamp))
