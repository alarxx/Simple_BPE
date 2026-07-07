"""
    SPDX-License-Identifier: MPL-2.0
    --------------------------------
    This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
    If a copy of the MPL was not distributed with this file,
    You can obtain one at https://mozilla.org/MPL/2.0/.

    This file is part of the Simple_BPE:
    https://github.com/alarxx/Simple_BPE

    Provided “as is”, without warranty of any kind.

    Copyright © 2026 Alar Akilbekov. All rights reserved.
"""

def normalization(text: str) -> str:
    text = text.lower()
    tmp = ""
    for c in text:
        if c.isalnum() or c.isspace():
           tmp += c
        else:
            tmp += " "
    text = tmp
    text = text.split()
    text = " ".join(text)
    return text


if __name__ == "__main__":
    text = " _ Hello, world! _ "
    print(normalization(text))
