# Simple_BPE

## Setup

Install python:
```sh
apt install python3 python3-full python3-pip python3-venv
#sudo apt install python3.8
python3 --version
```

Set up python venv:
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
# deactivate
```
Or set up with uv:
```sh
# install python
uv python install 3.13
uv init --python 3.13
uv venv
uv pip install pip
. .venv/bin/activate
pip install -e .
```

---

## Steps

- Text normalization
- Add `</w>` at the end of each word
- Count frequent pairs
- Get the most frequent pair
- Train BPE (merge symbols of vocab n times repeatedly)
- Get all tokens
- Encode a word
- Encode text (by encoding each word, open vocabulary: unknown characters `<unk>` for Out-of-Vocabulary (OOV))
- Decode tokens

---

Train:
```python
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
print(sorted(all_tokens))
#   ['</w>', '<unk>', 'd', 'e', 'h', 'he', 'hel', 'l', 'o', 'r', 'w']
```

---

Encoding and Decoding:
```python
# Encode text
text = normalization("Hello, BPE!")
tokens = encode(text, merges, all_tokens)
print(tokens) # ['hel', 'l', 'o', '</w>', '<unk>', '<unk>', 'e', '</w>']

# Decode tokens
text = decode(tokens)
print(text) # hello ??e
```

---

## Limitations

1. Normalization kills punctuation (`,`, `.`, `!` etc.) and whitespaces (`\n`, `\t`)
2. Original sentence case should be preserved
3. It's better to not tokenize numbers, keep digits as individual tokens: `0-9`
4. `token_to_id` and `id_to_token` are not implemented (easy)
5. Byte-level encoding is not implemented

---

## Licence

Simple_BPE is licensed under the terms of [MPL-2.0](https://mozilla.org/MPL/2.0/), which is simple and straightforward to use, allowing this project to be combined and distributed with any proprietary software, even with static linking. If you modify, only the originally covered files must remain under the same MPL-2.0.

License notice:
```
SPDX-License-Identifier: MPL-2.0
--------------------------------
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.

This file is part of the Simple_BPE:
https://github.com/alarxx/Simple_BPE

Provided “as is”, without warranty of any kind.

Copyright © 2026 Alar Akilbekov. All rights reserved.

Third party copyrights are property of their respective owners.
```

---

