##############################################################################
#
# Copyright (c) 2013 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id: tests.py 5267 2013-06-21 09:20:54Z roger.ineichen $
"""

import unittest
import doctest


def test_suite():
    suite = unittest.TestSuite((
        doctest.DocFileSuite('checker.txt', encoding='utf8',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        doctest.DocFileSuite('parse_version.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        ))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
