# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
# Copyright (C) 2018 RERO.
#
# Invenio-Circulation is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Circulation minters."""

from ..api import Loan
from .providers import CirculationLoanIdProvider


def loan_pid_minter(record_uuid, data):
    """Mint loan identifiers."""
    assert "pid" not in data
    provider = CirculationLoanIdProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
    )
    data["pid"] = provider.pid.pid_value
    return provider.pid
