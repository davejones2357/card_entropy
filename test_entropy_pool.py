import unittest

from EntropyPool import (
    CardEntropyPool,
    DeckExhaustedError,
    DuplicateCardError,
    InsufficientEntropyError,
    card_to_index,
)


class CardEntropyPoolExceptionsTests(unittest.TestCase):
    def test_deck_exhaustion_raises_domain_error(self):
        pool = CardEntropyPool()
        pool.drawn_cards = list(range(52))

        with self.assertRaises(DeckExhaustedError):
            pool._add_single_card("AS")

    def test_duplicate_card_raises_domain_error(self):
        pool = CardEntropyPool()
        pool.drawn_cards = [card_to_index("AS")]

        with self.assertRaises(DuplicateCardError):
            pool._add_single_card("AS")

    def test_consume_bits_raw_raises_insufficient_entropy_error(self):
        pool = CardEntropyPool()
        pool.reservoir = b""

        with self.assertRaises(InsufficientEntropyError):
            pool._consume_bits_raw(8)

    def test_roll_dice_batch_raises_insufficient_entropy_error(self):
        pool = CardEntropyPool()
        pool.entropy_bits = 1.0

        with self.assertRaises(InsufficientEntropyError):
            pool.roll_dice_batch(m=6)


if __name__ == "__main__":
    unittest.main()
