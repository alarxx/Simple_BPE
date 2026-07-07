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
    vocab: dict[tuple[str, ...], int] = {}

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


def count_pairs(
    vocab: dict[tuple[str, ...], int],
) -> dict[tuple[str, str], int]:
    """Count number of all occurring pairs (frequency).
    """
    pairs: dict[tuple[str, str], int] = {}

    for s, n in vocab.items():
        # s, n = ('h', 'i', '</w>'), 5
        for i in range(len(s) - 1):
            pair = (s[i], s[i+1])
            if pair not in pairs:
                pairs[pair] = 0
            pairs[pair] += n # 1 * n

    return pairs


def merge_symbols(
    s: tuple[str, ...],
    pair: tuple[str, str]
) -> tuple[str, ...]:
    """Merge all occurrences of pair in a word.
    """
    _s: list[str] = [] # merged

    i = 0
    while i < len(s):
        if i < len(s)-1 and s[i] == pair[0] and s[i+1] == pair[1]:
            _s.append(s[i] + s[i+1])
            i += 2
        else:
            _s.append(s[i])
            i += 1

    return tuple(_s)


def merge_vocab(
    vocab: dict[tuple[str, ...], int],
    pair: tuple[str, str]
) -> dict[tuple[str, ...], int]:
    """Merge all occurrences of pair in vocab "words".
    """
    _vocab: dict[tuple[str, ...], int] = {}

    # apply merge for each word
    for s, n in vocab.items():
        merged = merge_symbols(s, pair)
        if merged not in _vocab:
            _vocab[merged] = 0
        _vocab[merged] += n

    return _vocab


def train_bpe(
    vocab: dict[tuple[str, ...], int],
    num_merges: int
) -> tuple[dict[tuple[str, ...], int], list[tuple[str, str]]]:
    """Repeateldy merge most common pairs several times in a loop.
    """
    merges: list[tuple[str, str]] = [] # each merge-pair is a token

    for i in range(num_merges):
        # Count number of pairs
        pairs = count_pairs(vocab)

        # Find most common pair (named after collections.Counter.most_common(topn))
        most_common = max(pairs, key=lambda p: pairs[p])

        # Save merge-pair
        merges.append(most_common)

        # Merge-pair in vocab
        vocab = merge_vocab(vocab, most_common)

        print(f"merges({i}):", merges, end="\n\n")
        print(f"vocab({i}):", vocab, end="\n\n")

    return vocab, merges


def get_all_tokens(
    vocab: dict[tuple[str, ...], int], # initial vocab
    merges: list[tuple[str, str]],
    unk: str = UNKNOWN_SYMBOL
) -> set[str]:
    tokens: set[str] = set()

    # 1. base vocab symbols, e.g. 'h', 'i', '</w>'
    for s in vocab:
        for c in s:
            tokens.add(c)

    # 2. merge-tokens
    for l, r in merges:
        tokens.add(l + r)

    # 3. special symbols
    tokens.add(unk)

    return tokens


if __name__ == "__main__":
    corpus = [
        "Hello, world!",    # document_1
        "Hello!",           # document_2
    ]

    # Normalization
    corpus = [normalization(text) for text in corpus]

    # Build initital vocab
    vocab = build_vocab(corpus)
    print(vocab) # {('h', 'e', 'l', 'l', 'o', '</w>'): 1, ...}

    # # One manual merge
    # # Count number of pairs
    # pairs = count_pairs(vocab)
    # print(pairs)
    #
    # # Find most common pair (named after collections.Counter.most_common(topn))
    # most_common = max(pairs, key=lambda p: pairs[p])
    # print(most_common)
    #
    # # Merge pair in vocab
    # vocab = merge_vocab(vocab, most_common)
    # print(vocab)

    # Loop merge repeatedly
    _, merges = train_bpe(vocab, 2)

    # Get all tokens
    all_tokens = get_all_tokens(vocab, merges)
    print(sorted(all_tokens))
