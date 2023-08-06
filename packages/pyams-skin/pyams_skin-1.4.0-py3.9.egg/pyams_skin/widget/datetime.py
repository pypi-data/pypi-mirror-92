#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_skin.widget.datetime module

This module defines widgets which are used to handle date, time and
datetime inputs.
"""

from zope.interface import implementer_only
from zope.schema.interfaces import IDate, IDatetime, ITime

from pyams_form.browser.text import TextWidget
from pyams_form.converter import BaseDataConverter
from pyams_form.interfaces import IDataConverter
from pyams_form.interfaces.widget import IFieldWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_skin.interfaces.widget import IDateWidget, IDatetimeWidget, ITimeWidget
from pyams_utils.adapter import adapter_config
from pyams_utils.date import parse_date
from pyams_utils.timezone import tztime


__docformat__ = 'restructuredtext'


class BaseDatetimeDataConverter(BaseDataConverter):
    """Bse datetime data converter"""

    def to_widget_value(self, value):
        if not value:
            return None
        return tztime(value).isoformat()

    def to_field_value(self, value):
        if not value:
            return None
        return tztime(parse_date(value))


#
# Datetime widget
#

@adapter_config(required=(IDatetime, IDatetimeWidget),
                provides=IDataConverter)
class DatetimeDataConverter(BaseDatetimeDataConverter):
    """Datetime widget data converter"""


@implementer_only(IDatetimeWidget)
class DatetimeWidget(TextWidget):
    """Datetime widget"""


@adapter_config(required=(IDatetime, IFormLayer),
                provides=IFieldWidget)
def DatetimeFieldWidget(field, request):  # pylint: disable=invalid-name
    """Datetime field widget factory"""
    return FieldWidget(field, DatetimeWidget(request))


#
# Date widget
#

@adapter_config(required=(IDate, IDateWidget),
                provides=IDataConverter)
class DateDataConverter(BaseDatetimeDataConverter):
    """Date widget data converter"""


@implementer_only(IDateWidget)
class DateWidget(TextWidget):
    """Date widget"""


@adapter_config(required=(IDate, IFormLayer),
                provides=IFieldWidget)
def DateFieldWidget(field, request):  # pylint: disable=invalid-name
    """Date field widget factory"""
    return FieldWidget(field, DateWidget(request))


#
# Time widget
#

@adapter_config(required=(ITime, ITimeWidget),
                provides=IDataConverter)
class TimeDataConverter(BaseDatetimeDataConverter):
    """Time widget data converter"""


@implementer_only(ITimeWidget)
class TimeWidget(TextWidget):
    """Time widget"""


@adapter_config(required=(ITime, IFormLayer),
                provides=IFieldWidget)
def TimeFieldWidget(field, request):  # pylint: disable=invalid-name
    """Time field widget factory"""
    return FieldWidget(field, TimeWidget(request))
