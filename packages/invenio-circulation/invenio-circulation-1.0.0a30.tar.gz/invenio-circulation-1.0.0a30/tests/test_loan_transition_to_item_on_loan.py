# -*- coding: utf-8 -*-
#
# Copyright (C) 2018-2020 CERN.
# Copyright (C) 2018-2020 RERO.
#
# Invenio-Circulation is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Tests for loan states."""

from datetime import timedelta

import arrow
import pytest

from invenio_circulation.errors import ItemNotAvailableError, \
    TransitionConstraintsViolationError
from invenio_circulation.proxies import current_circulation

from .helpers import SwappedConfig


def test_created_to_item_on_loan_available_item_with_default_location(
    loan_created, params, mock_is_item_available_for_checkout
):
    """Test direct checkout on available item with default location."""

    mock_is_item_available_for_checkout.return_value = True

    assert loan_created["state"] == "CREATED"

    with SwappedConfig(
        "CIRCULATION_ITEM_LOCATION_RETRIEVER",
        lambda x: "pickup_location_pid"
    ):
        loan = current_circulation.circulation.trigger(
            loan_created, **dict(params, trigger="checkout")
        )

    assert loan["state"] == "ITEM_ON_LOAN"
    assert loan["pickup_location_pid"] == "pickup_location_pid"
    assert loan["item_pid"] == dict(type="itemid", value="item_pid")


def test_created_to_item_on_loan_available_item_with_specified_location(
    loan_created, params, mock_is_item_available_for_checkout
):
    """Test direct checkout on available item with different location."""

    mock_is_item_available_for_checkout.return_value = True

    assert loan_created["state"] == "CREATED"

    with SwappedConfig(
        "CIRCULATION_ITEM_LOCATION_RETRIEVER",
        lambda x: "pickup_location_pid"
    ):
        loan = current_circulation.circulation.trigger(
            loan_created, **dict(params, trigger="checkout",
                                 pickup_location_pid="other_location_pid")
        )

    assert loan["state"] == "ITEM_ON_LOAN"
    assert loan["pickup_location_pid"] == "other_location_pid"
    assert loan["item_pid"] == dict(type="itemid", value="item_pid")


def test_created_to_item_on_loan_unavailable_item(
    loan_created, params, mock_ensure_item_is_available_for_checkout
):
    """Test direct checkout on unavailable item."""

    assert loan_created["state"] == "CREATED"

    mock_ensure_item_is_available_for_checkout.side_effect = \
        ItemNotAvailableError(item_pid=dict(type="itemid", value="1"),
                              transition="Fake Transition")

    with pytest.raises(ItemNotAvailableError):
        with SwappedConfig(
            "CIRCULATION_ITEM_LOCATION_RETRIEVER",
            lambda x: "pickup_location_pid"
        ):
            current_circulation.circulation.trigger(
                loan_created, **dict(params, trigger="checkout",
                                     pickup_location_pid="other_location_pid")
            )


def test_created_to_item_on_loan_available_item_with_invalid_duration(
    loan_created, params, mock_is_item_available_for_checkout
):
    """Test direct checkout on available item with invalid duration."""

    mock_is_item_available_for_checkout.return_value = True

    assert loan_created["state"] == "CREATED"

    params["start_date"] = arrow.get("2018-01-01")
    params["end_date"] = params["start_date"] + timedelta(days=60)

    with pytest.raises(TransitionConstraintsViolationError):
        with SwappedConfig(
            "CIRCULATION_ITEM_LOCATION_RETRIEVER",
            lambda x: "pickup_location_pid"
        ):
            current_circulation.circulation.trigger(
                loan_created, **dict(params, trigger="checkout")
            )


def test_created_to_item_on_loan_available_item_with_valid_duration(
    loan_created, params, mock_ensure_item_is_available_for_checkout
):
    """Test direct checkout on available item with valid duration."""

    mock_ensure_item_is_available_for_checkout.side_effect = None

    assert loan_created["state"] == "CREATED"

    params["transaction_date"] = arrow.utcnow()
    params["start_date"] = arrow.get("2018-01-01")
    params["end_date"] = params["start_date"] + timedelta(days=59)

    with SwappedConfig(
        "CIRCULATION_ITEM_LOCATION_RETRIEVER",
        lambda x: "pickup_location_pid"
    ):
        loan = current_circulation.circulation.trigger(
            loan_created, **dict(params, trigger="checkout")
        )

    assert loan["state"] == "ITEM_ON_LOAN"
    assert loan["pickup_location_pid"] == "pickup_location_pid"
    assert loan["item_pid"] == dict(type="itemid", value="item_pid")
    assert loan["transaction_date"] == params["transaction_date"].isoformat()


def test_pending_to_item_on_loan_available_item(
    loan_created, params, mock_ensure_item_is_available_for_checkout
):
    """Test direct checkout on available item."""

    mock_ensure_item_is_available_for_checkout.side_effect = None

    with SwappedConfig(
        "CIRCULATION_ITEM_LOCATION_RETRIEVER",
        lambda x: "pickup_location_pid"
    ):
        loan = current_circulation.circulation.trigger(
            loan_created, **dict(params, trigger="request")
        )

        assert loan["state"] == "PENDING"

        loan = current_circulation.circulation.trigger(
            loan_created, **dict(params, trigger="checkout",
                                 pickup_location_pid="other_location_pid")
        )

        assert loan["state"] == "ITEM_ON_LOAN"
        assert loan["pickup_location_pid"] == "other_location_pid"
        assert loan["item_pid"] == dict(type="itemid", value="item_pid")
