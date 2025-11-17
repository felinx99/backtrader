#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import pytz
import sys

from .. import feed
from .. import TimeFrame
from ..utils import date2num


class stockCSVData(feed.CSVDataBase):
    '''
    Parses a `VisualChart <http://www.visualchart.com>`_ CSV exported file.

    Specific parameters (or specific meaning):

      - ``dataname``: The filename to parse or a file-like object
    '''

    params = (
        ('date', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', 6),
    )

    datafields = [
        'date', 'open', 'high', 'low', 'close', 'volume', 'openinterest'
    ]

    def _loadline(self, linetokens):
        itokens = iter(linetokens)

        dttxt = next(itokens)  
        tz_shanghai = pytz.timezone('Asia/Shanghai')
        try:
        # 尝试更复杂的格式: 'YYYY-MM-DD HH:MM'
            dt_object = datetime.datetime.strptime(dttxt, '%Y-%m-%d %H:%M')
        except:
            try:
                # 如果复杂格式失败，尝试简单格式: 'YYYYMMDD'
                dt_object = datetime.datetime.strptime(dttxt, '%Y%m%d')
            except Exception as e:
                # 如果两种格式都失败
                print(f"parse '{dttxt}' error with either format.")
                sys.exit(1) # 退出程序
        
        dt_tz = tz_shanghai.localize(dt_object)

        self.lines.datetime[0] = date2num(dt_tz)
        self.lines.open[0] = float(next(itokens))
        self.lines.high[0] = float(next(itokens))
        self.lines.low[0] = float(next(itokens))
        self.lines.close[0] = float(next(itokens))
        self.lines.volume[0] = float(next(itokens))
        self.lines.openinterest[0] = 0

        return True


class stockCSV(feed.CSVFeedBase):
    DataCls = stockCSVData
