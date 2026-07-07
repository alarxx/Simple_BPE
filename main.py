from bpe.normalization import normalization
from bpe.train import (
    build_vocab,
    train_bpe,
    get_all_tokens,
)
from bpe.encode_decode import encode, decode


if __name__ == "__main__":
    corpus = [
        # alphabet (a-z)
        # digits (0-9)
        "Hello, world!", # document_1
        "Hello!",        # document_2
    ]

    # Normalization
    corpus = [normalization(text) for text in corpus]

    # Build initital vocab
    vocab = build_vocab(corpus)
    #   vocab: {('h', 'e', 'l', 'l', 'o', '</w>'): 2, ...}

    # Find most common pair and merge repeatedly
    _, merges = train_bpe(vocab, 2)
    #   vocab(1): {('hel', 'l', 'o', '</w>'): 2, ('w', 'o', 'r', 'l', 'd', '</w>'): 1}
    #   merge(1): [('h', 'e'), ('he', 'l')]

    # Get all tokens
    all_tokens = get_all_tokens(vocab, merges)


    # Encode text
    text = normalization("Hello, BPE!")
    tokens = encode(text, merges, all_tokens)
    print(tokens) # ['hel', 'l', 'o', '</w>', '<unk>', '<unk>', 'e', '</w>']

    # Decode tokens
    text = decode(tokens)
    print(text) # hello ??e
