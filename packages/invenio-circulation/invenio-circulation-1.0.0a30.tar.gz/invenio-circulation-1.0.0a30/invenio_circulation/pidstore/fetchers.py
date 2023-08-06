# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
# Copyright (C) 2018 RERO.
#
# Invenio-Circulation is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Circulation fetchers."""

from invenio_pidstore.fetchers import FetchedPID

from ..api import Loan
from .pids import CIRCULATION_LOAN_PID_TYPE


def loan_pid_fetcher(record_uuid, data):
    """Fetch PID from loan record."""
    return FetchedPID(
        provider=None,
        pid_type=CIRCULATION_LOAN_PID_TYPE,
        pid_value=str(data["pid"])
    )
