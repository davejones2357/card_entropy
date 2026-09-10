import math
import hashlib

RANKS = {
    'T': 0, 'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9, 'J': 10, 'Q': 11, 'K': 12
}
SUITS = {'C': 0, 'D': 1, 'H': 2, 'S': 3}

def card_to_index(card_str):
    card_str = card_str.strip().upper()
    if len(card_str) != 2:
        raise ValueError(f"Bad card shorthand: {card_str}")
    r, s = card_str[0], card_str[1]
    if r not in RANKS or s not in SUITS:
        raise ValueError(f"Bad card shorthand: {card_str}")
    return SUITS[s] * 13 + RANKS[r]

class CardEntropyPool:
    def __init__(self):
        self.drawn_cards = []      # indices of cards drawn (0..51)
        self.entropy_bits = 0.0    # total available entropy
        self.reservoir = b""       # mixed entropy bytes

    def deck_size_remaining(self):
        return 52 - len(self.drawn_cards)

    def add_cards_from_shorthand(self, line):
        # line like: "KH 4S 9D"
        tokens = [t for t in line.strip().split() if t]
        for t in tokens:
            try:
                self._add_single_card(t)
            except ValueError as e:
                print(f"Error adding card {t}: {e}")

    def _add_single_card(self, card_str):
        if self.deck_size_remaining() <= 0:
            raise RuntimeError("Deck exhausted, reshuffle needed.")
        idx = card_to_index(card_str)
        if idx in self.drawn_cards:
            raise RuntimeError(f"Card {card_str} already drawn (no replacement).")
        self.drawn_cards.append(idx)

        # entropy of this draw: log2(remaining_cards_before_draw)
        n_drawn = len(self.drawn_cards)
        remaining_before = 53 - n_drawn  # 52 - (n_drawn - 1)
        h = math.log2(remaining_before)
        self.entropy_bits += h

    def mix(self):
        if not self.drawn_cards:
            return
        h = hashlib.sha256()
        for c in self.drawn_cards:
            h.update(c.to_bytes(1, 'big'))
        self.reservoir += h.digest()
        self.drawn_cards.clear()

    def available_bits(self):
        # reservoir bytes are just a container; entropy_bits tracks real bits
        return self.entropy_bits

    def _consume_bits_raw(self, n_bits):
        needed_bytes = math.ceil(n_bits / 8)
        if len(self.reservoir) < needed_bytes:
            raise RuntimeError("Not enough mixed bytes in reservoir; call mix() or add more cards.")
        out = self.reservoir[:needed_bytes]
        self.reservoir = self.reservoir[needed_bytes:]
        self.entropy_bits -= n_bits
        return out

    def roll_die(self):
        # needs log2(6) ≈ 2.585 bits; use 3 bits and reject 6–7
        while True:
            b = self._consume_bits_raw(3)
            v = b[0] & 0b111
            if v < 6:
                return v + 1 # v+1 as die face is 1..6, not 0..5

    def roll_dice_batch(self, m=6):
        needed_bits = m * math.log2(6)
        if self.available_bits() < needed_bits:
            raise RuntimeError("Not enough entropy for requested batch.")
        dice = [self.roll_die() for _ in range(m)]
        return dice
