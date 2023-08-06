# -*- coding: utf-8 -*-
"""
    pygments-style-ssms
    ~~~~~~~~~~~~~~~~~~~~~~~

    A Pygments style inspired by Microsoft SSMS.

    :copyright: Copyright 2021 Matthias Lüken
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator


class SSMSStyle(Style):
    """
    The SSMS style.
    """

    background_color = "#ffffff"
    default_style = ""

    styles = {
        Comment:                   "#008000",
        Keyword:                   "#0000ff",
        Operator:                  "#808080",
        Name:                      "#000000",
        Name.Function:             "#ff00ff",
        Name.Builtin:              "#01ff00",
        String:                    "#ff0000",
        Error:                     "border:#ff0000",
        Number:                    "#000000"
    }
