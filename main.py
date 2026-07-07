from bpe.normalization import normalization
from bpe.train import (
    build_vocab,
    train_bpe,
    get_all_tokens,
)
from bpe.encode_decode import encode, decode


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

    # Encode text
    tokens = encode(normalization("Hello, BPE!"), merges, all_tokens)
    print(tokens) # ['hel', 'l', 'o', '</w>', '<unk>', '<unk>', 'e', '</w>']

    # Decode tokens
    print(decode(tokens)) # hello ??e
