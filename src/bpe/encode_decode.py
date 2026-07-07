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

from bpe.normalization import normalization
from bpe.train import (
    build_vocab,
    merge_symbols,
    train_bpe,
    get_all_tokens,
    END_OF_WORD,
    UNKNOWN_SYMBOL
)


def encode_word(
    word: str,
    merges: list[tuple[str, str]],
    all_tokens: set[str],
    end: str = END_OF_WORD,
    unk: str = UNKNOWN_SYMBOL
) -> list[str, ...]:
    """Split the word into chars/symbols and apply the same merging order as during training.
    """
    # Split the word into chars/symbols
    s = tuple(word) + (end,)

    # Apply the same merging order as during training
    for pair in merges:
        s = merge_symbols(s, pair)

    # Check if tokens exist
    word_tokens = []
    for token in s:
        if token in all_tokens:
            word_tokens.append(token)
        else:
            word_tokens.append(unk)

    return word_tokens


def encode(
    text: str,
    merges: list[tuple[str, str]],
    all_tokens: set[str],
    end: str = END_OF_WORD,
    unk: str = UNKNOWN_SYMBOL
) -> list[str]:
    tokens = []

    for word in text.split():
        word_tokens = encode_word(word, merges, all_tokens, end, unk)
        tokens.extend(word_tokens)

    return tokens


def decode(
    tokens: list[str],
    end: str = END_OF_WORD,
    unk: str = UNKNOWN_SYMBOL
) -> str:
    text = "".join(tokens)
    text = text.replace(end, " ")
    text = text.replace(unk, "?")
    text = text.strip()
    return text


if __name__ == "__main__":
    corpus = [
        "Hello, world!",    # document_1
        "Hello!",           # document_2
    ]
    # Normalization
    corpus = [normalization(text) for text in corpus]
    # Build initital vocab
    vocab = build_vocab(corpus) # {('h', 'e', 'l', 'l', 'o', '</w>'): 1, ...}
    # Find most common pair and merge repeatedly
    _, merges = train_bpe(vocab, 2)
    # Get all tokens
    all_tokens = get_all_tokens(vocab, merges)

    # Encode individual words
    print(encode_word("hello", merges, all_tokens)) # ['hel', 'l', '</w>']
    print(encode_word("bpe", merges, all_tokens)) # ['<unk>', '<unk>', 'e', '</w>']

    # Encode text
    tokens = encode(normalization("Hello, BPE!"), merges, all_tokens)
    print(tokens)

    # Decode tokens
    print(decode(tokens))
