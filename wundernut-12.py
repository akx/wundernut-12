import string
import textwrap

import pytesseract
import wordninja
from PIL import Image


def illuminate_invisible_ink(filename: str):
    image = Image.open(filename).convert("RGB")
    # Find out a palette for the image.
    colors = {c: i for i, c in enumerate(set(image.getdata()))}
    # This assumes the invisible ink is very sharply defined.
    assert len(colors) == 2
    # Convert the two invisible colors to black and white.
    image.putdata(
        [((255, 255, 255) if colors[c] else (0, 0, 0)) for c in image.getdata()]
    )
    return image


def read_handwriting(image):
    # The magician's handwriting is better squished up a bit
    # for better recognition, and Pytesseract works better
    # with slightly smaller images.
    w, h = image.size
    squish = image.resize((int(w * 0.7 * 0.5), int(h * 0.5)))
    return pytesseract.image_to_string(squish).replace("\n", "")


def caesar(s: str, shift: int, keyspace=string.ascii_uppercase):
    """
    Caesar-cipher the string using the given keyspace and shift.
    """
    shift_table = str.maketrans(keyspace, keyspace[shift:] + keyspace[:shift])
    return s.translate(shift_table)


# Zim's list of common letter pairs in English.
COMMON_ENGLISH_PAIRS = (
    "TH HE AN RE ER IN ON AT ND ST ES EN OF TE ED OR TI HI AS TO".split()
)


def englishness(s):
    """
    Compute an arbitrary unitless Englishness metric for the string.
    """
    s = s.upper()
    return sum(s.count(p) for p in COMMON_ENGLISH_PAIRS)


def main():
    # Convert invisible ink to stark black and white.
    image = illuminate_invisible_ink("parchment.png")
    # Read the handwriting from the illuminated ink.
    text = read_handwriting(image)
    # We'll assume the magician is Julius Caesar, but we don't know
    # the shift value, so we'll try out all of them and use a nifty
    # englishness heuristic to guess which shift is the best.
    best_shift, best_result = max(
        [(shift, caesar(text, shift)) for shift in range(26)],
        key=lambda pair: englishness(pair[1]),
    )
    # Okay, so now we'll just need to tell the words apart. Luckily
    # we have a friendly ninja at our disposal.  They'll probably trip
    # up at any spell names there'll inevitably be in the message,
    # but we can't do much about that.
    result = " ".join(wordninja.split(best_result))
    # Since long lines are hard to read, let's wrap the text for display.
    beautiful_result = textwrap.fill(result, width=80)
    # Good to go, :shipit:
    print(beautiful_result)


if __name__ == "__main__":
    main()
