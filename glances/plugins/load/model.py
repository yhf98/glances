# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# SPDX-FileCopyrightText: 2022 Nicolas Hennion <nicolas@nicolargo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
#

"""Load plugin."""

import os
import psutil

from glances.globals import iteritems
from glances.plugins.core.model import PluginModel as CorePluginModel
from glances.plugins.plugin.model import GlancesPluginModel
from glances.logger import logger

# Fields description
fields_description = {
    'min1': {
        'description': 'Average sum of the number of processes \
waiting in the run-queue plus the number currently executing \
over 1 minute.',
        'unit': 'float',
    },
    'min5': {
        'description': 'Average sum of the number of processes \
waiting in the run-queue plus the number currently executing \
over 5 minutes.',
        'unit': 'float',
    },
    'min15': {
        'description': 'Average sum of the number of processes \
waiting in the run-queue plus the number currently executing \
over 15 minutes.',
        'unit': 'float',
    },
    'cpucore': {'description': 'Total number of CPU core.', 'unit': 'number'},
}

# SNMP OID
# 1 minute Load: .1.3.6.1.4.1.2021.10.1.3.1
# 5 minute Load: .1.3.6.1.4.1.2021.10.1.3.2
# 15 minute Load: .1.3.6.1.4.1.2021.10.1.3.3
snmp_oid = {
    'min1': '1.3.6.1.4.1.2021.10.1.3.1',
    'min5': '1.3.6.1.4.1.2021.10.1.3.2',
    'min15': '1.3.6.1.4.1.2021.10.1.3.3',
}

# Define the history items list
# All items in this list will be historised if the --enable-history tag is set
items_history_list = [
    {'name': 'min1', 'description': '1 minute load'},
    {'name': 'min5', 'description': '5 minutes load'},
    {'name': 'min15', 'description': '15 minutes load'},
]


class PluginModel(GlancesPluginModel):
    """Glances load plugin.

    stats is a dict
    """

    def __init__(self, args=None, config=None):
        """Init the plugin."""
        super(PluginModel, self).__init__(
            args=args, config=config, items_history_list=items_history_list, fields_description=fields_description
        )

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Call CorePluginModel in order to display the core number
        try:
            self.nb_log_core = CorePluginModel(args=self.args).update()["log"]
        except Exception as e:
            logger.warning('Error: Can not retrieve the CPU core number (set it to 1) ({})'.format(e))
            self.nb_log_core = 1

    def _getloadavg(self):
        """Get load average. On both Linux and Windows thanks to PsUtil"""
        try:
            return psutil.getloadavg()
        except (AttributeError, OSError):
            pass
        try:
            return os.getloadavg()
        except (AttributeError, OSError):
            return None

    @GlancesPluginModel._check_decorator
    @GlancesPluginModel._log_result_decorator
    def update(self):
        """Update load stats."""
        # Init new stats
        stats = self.get_init_value()

        if self.input_method == 'local':
            # Update stats using the standard system lib

            # Get the load using the os standard lib
            load = self._getloadavg()
            if load is None:
                stats = self.get_init_value()
            else:
                stats = {'min1': load[0], 'min5': load[1], 'min15': load[2], 'cpucore': self.nb_log_core}

        elif self.input_method == 'snmp':
            # Update stats using SNMP
            stats = self.get_stats_snmp(snmp_oid=snmp_oid)

            if stats['min1'] == '':
                stats = self.get_init_value()
                return stats

            # Python 3 return a dict like:
            # {'min1': "b'0.08'", 'min5': "b'0.12'", 'min15': "b'0.15'"}
            for k, v in iteritems(stats):
                stats[k] = float(v)

            stats['cpucore'] = self.nb_log_core

        # Update the stats
        self.stats = stats

        return self.stats

    def update_views(self):
        """Update stats views."""
        # Call the father's method
        super(PluginModel, self).update_views()

        # Add specifics information
        try:
            # Alert and log
            self.views['min15']['decoration'] = self.get_alert_log(
                self.stats['min15'], maximum=100 * self.stats['cpucore']
            )
            # Alert only
            self.views['min5']['decoration'] = self.get_alert(self.stats['min5'], maximum=100 * self.stats['cpucore'])
        except KeyError:
            # try/except mandatory for Windows compatibility (no load stats)
            pass

    def msg_curse(self, args=None, max_width=None):
        """Return the dict to display in the curse interface."""
        # Init the return message
        ret = []

        # Only process if stats exist, not empty (issue #871) and plugin not disabled
        if not self.stats or (self.stats == {}) or self.is_disabled():
            return ret

        # Build the string message
        # Header
        msg = '{:4}'.format('LOAD')
        ret.append(self.curse_add_line(msg, "TITLE"))
        msg = ' {:1}'.format(self.trend_msg(self.get_trend('min1')))
        ret.append(self.curse_add_line(msg))
        # Core number
        if 'cpucore' in self.stats and self.stats['cpucore'] > 0:
            msg = '{:3}core'.format(int(self.stats['cpucore']))
            ret.append(self.curse_add_line(msg))
        # Loop over 1min, 5min and 15min load
        for load_time in ['1', '5', '15']:
            ret.append(self.curse_new_line())
            msg = '{:7}'.format('{} min'.format(load_time))
            ret.append(self.curse_add_line(msg))
            if args.disable_irix and self.nb_log_core != 0:
                # Enable Irix mode for load (see issue #1554)
                load_stat = self.stats['min{}'.format(load_time)] / self.nb_log_core * 100
                msg = '{:>5.1f}%'.format(load_stat)
            else:
                # Default mode for load
                load_stat = self.stats['min{}'.format(load_time)]
                msg = '{:>6.2f}'.format(load_stat)
            ret.append(self.curse_add_line(msg, self.get_views(key='min{}'.format(load_time), option='decoration')))

        return ret
