#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        test_properties
# Purpose:     Test driver for package 'decimalfp' (pickling)
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2019 Michael Amrhein
# ----------------------------------------------------------------------------
# $Source: test/func/test_pickling.py $
# $Revision: 2020-10-28T21:40:30+01:00 $


"""Test driver for package 'decimalfp' (pickling)."""


from pickle import dumps, loads

import pytest


@pytest.mark.parametrize("value",
                         ("17.800",
                          ".".join(("1" * 3097, "4" * 33 + "0" * 19)),
                          "-0.00014",
                          "12345678",
                          None),
                         ids=("compact", "large", "fraction", "int", "zero"))
def test_pickling(impl, value):
    dec = impl.Decimal(value)
    assert loads(dumps(dec)) == dec
