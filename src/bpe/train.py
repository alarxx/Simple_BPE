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

from normalization import normalization


END_OF_WORD = "</w>"
UNKNOWN_SYMBOL = "<unk>"


def build_vocab(
    corpus: list[str],
    end: str = END_OF_WORD
) -> dict[tuple[str, ...], int]:
    """Build initital vocab from corpus of text.
    """
    vocab = {}

    for text in corpus:
        for word in text.split():
            s = tuple(word) + (end,) # ('h', 'i', '</w>')
            if s not in vocab:
                vocab[s] = 0
            vocab[s] += 1
    # vocab: {
    #     ('h', 'i', '</w>'): 1,
    #     ('c', 'a', 't', '</w>'): 1,
    #     ...
    # }
    return vocab


if __name__ == "__main__":
    corpus = [
        " _ Hello, world! _ ", # document
    ]

    # Normalization
    corpus = [normalization(text) for text in corpus]

    # Build initital vocab
    vocab = build_vocab(corpus)
    print(vocab) # {('h', 'e', 'l', 'l', 'o', '</w>'): 1, ...}
