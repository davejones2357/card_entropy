import sys
from EntropyPool import CardEntropyPool

def main():
    pool = CardEntropyPool()

    print("Phase 1: enter card batches (e.g. 'KH 4S 9D'). Type 'mix' to hash, 'finished' to move on.")
    while True:
        line = input("> ").strip()
        if not line:
            continue
        if line.lower()[:3] == "fin":
            break
        if line.lower() == "mix":
            pool.mix()
            print(f"Mixed. Entropy pool: {pool.available_bits():.2f} bits, "
                  f"deck remaining: {pool.deck_size_remaining()}")
            continue

        pool.add_cards_from_shorthand(line)
        print(f"Entropy pool: {pool.available_bits():.2f} bits, "
              f"deck remaining: {pool.deck_size_remaining()}")

        # reshuffle hint
        if pool.deck_size_remaining() <= 12:
            print("Warning: low deck entropy per draw; consider reshuffling soon.")

    # ensure we have mixed whatever is in drawn_cards
    pool.mix()
    print(f"\nPhase 2: dice output. Entropy pool: {pool.available_bits():.2f} bits.")
    try:
        m = int(input("Dice per batch (default 6): ") or "6")
    except ValueError:
        m = 6

    while True:
        try:
            dice = pool.roll_dice_batch(m)
        except RuntimeError as e:
            print(f"Done: {e}")
            break
        print("Dice:", dice)
        inp = input("Press Enter for next batch, or 'q' to quit: ").strip().lower()
        if inp == "q":
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
