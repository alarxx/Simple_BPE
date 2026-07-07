from bpe.normalization import normalization


if __name__ == "__main__":
    text = " _ Hello, world! _ "

    print(f"Raw:\n{text}", end="\n\n")

    # Normalized text
    text = normalization(text)
    print(f"Normalized:\n{text}", end="\n\n")
