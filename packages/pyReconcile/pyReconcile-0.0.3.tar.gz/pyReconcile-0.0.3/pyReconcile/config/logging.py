# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Access to Logging facilities both for dev/debug and production purposes.

Library logging makes use of the python logging module's "extra" dict for
providing fields and their values for logging, and does not fill in "message".

This requires providing a format string that makes use of individual fields
for successfull logging.

This module provides read-only reference for the necessary Extra parameter
names required by any application-developer-supplied logging.formatter objects
used to extract logs from this library.

This module also provides a helper-function to enable basic logging for
library development.

Since this is a library, logging is disabled by default.
"""

import logging

##Defualt Configurations
pyReconcile_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
"""str: Default format string used for Library logging.

Used in :func:`ENABLE_DEVELOPMENT_LOGGING`
"""

pyReconcile_scheduler_format = (
    "%(asctime)s | %(name)s | %(levelname)s | %(run_id)s | %(type)s | %(description)s"
)
"""str: Format string used by the `pyReconcile.Scheduler` .

Used in :func:`ENABLE_DEVELOPMENT_LOGGING`
"""

## Since Scheduler relies on Extra arguments to log fields, Message is empty.
## Since Message is empty, propagating up to the default Logger results in useless log.
logging.getLogger("pyReconcile.Scheduler").propagate = False

## NullHandler prevents the library from logging until configured by the app-dev.
logging.getLogger("pyReconcile").addHandler(logging.NullHandler())


def ENABLE_DEVELOPMENT_LOGGING():
    """Enable logging for library development."""

    default_console_handler = logging.StreamHandler()
    default_console_handler.setLevel(logging.DEBUG)
    default_console_handler.setFormatter(logging.Formatter(pyReconcile_format))

    scheduler_console_handler = logging.StreamHandler()
    scheduler_console_handler.setLevel(logging.DEBUG)
    scheduler_console_handler.setFormatter(
        logging.Formatter(pyReconcile_scheduler_format)
    )

    logging.getLogger("pyReconcile").addHandler(default_console_handler)
    logging.getLogger("pyReconcile.Scheduler").addHandler(scheduler_console_handler)

    logging.getLogger("pyReconcile").setLevel(logging.DEBUG)
    logging.getLogger("pyReconcile.Scheduler").setLevel(logging.DEBUG)