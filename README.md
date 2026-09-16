# Entropy Conversion: Playing Cards → Base‑6 Dice Rolls
## Disclaimer 
The code in this repo is just an exercise.
Do not use it to secure anything valuable!

## Overview
This Python script converts entropy expressed as a sequence of playing‑card draws (encoded in a two‑digit base‑13 format) into an equivalent sequence of base‑6 digits (i.e., simulated six‑sided dice rolls). The goal is simple: Convert formats and preserve entropy.

## Background
A recent ColdCard hardware‑wallet vulnerability exposed users who relied solely on the device’s internal RNG. Users who supplied their own entropy via physical dice rolls were unaffected.

Rolling dice is reliable but tedious. Generating a 256‑bit seed requires 
```math
\frac{256}{\log_2(6)} \approx 100 
```
dice rolls.
An alternative is drawing playing cards from a well shuffled deck. If each draw is made with replacement and the deck is properly shuffled, each draw yields 
```math
\log_2(52) \approx 5.7 
```
bits, so producing 256 bits requires 
```math
\frac{256}{\log_2(52)} \approx 44.9 
```
card draws, if the card is replaced and the deck adequately shuffled each time.

## Entropy Limits: Cards Without Replacement
Replacing each card and reshuffling the deck would of course be far more tedious than rolling dice. If cards are drawn **without replacement**, the total entropy available is 
```math
\log_2(52!) \approx 225.6
```
bits, which falls short of the 256 required to generate a private key. 

Around the 39th card drawn, the entropy has fallen off by around a third of its initial value:
```math
\frac{ \log_2(52-38)}{ \log_2(52)} \approx \frac{2}{3}
```
Given that the deck has to be reshuffled at least once to complete the job, this is a  sensible point to remind the user to do it.

## Input Format (Base‑13 Card Encoding)
Each playing card is encoded as a two‑character base‑13 number:

High‑order digit: Suit
|Suit|Symbol|Value|
|---|---|---|
|Club |C	| 0	|
|Diamond |D 	| 1	|
|Heart |H 	| 2	|
|Spade |S 	| 3	|

Low‑order digit: Value
|Card|Symbol|Value|
|---|---|---|
|Ten |T 	| 0	|
|Ace |A 	| 1	|
|2 |2 	| 2	|
|	...	|
|9 |9 | 9	|
|Jack |J 	| A	|
|Queen |Q 	| B	|
|King |K 	| C	|

So for example, AS is the ace of spades and is encoded as 31 in base-13.

This yields 52 valid combinations, even though the encoding space is $$13^2 = 169$$.
The script validates input to ensure only real card combinations are accepted.

## What the Script Does
The script runs in two distinct phases:
* Build an entropy pool from cards drawn randomly from a deck.
* Consume entropy from the pool in order to mimic dice rolls.

### Phase 1 - Collect card draws
*	Prompts for card batches (e.g. KH 4S 9D).
*	Commands:
*	**mix** → folds drawn cards into the entropy pool.
*	**finished** (or **fin**) → end phase 1.
*	After each input display the size of the entropy pool and number of cards remaining in the deck. Warns when less than 12 cards remain.

### Phase 2 - Output dice rolls 
* Asks the user for a preferred batch size (default to 6).
* Consume bits from the entropy pool.
* Outputs a sequence equivalent to rolling six‑sided dice.
* User presses RETURN to repeat until pool is exhausted.

## Example

Input:
```
Phase 1: enter card batches (e.g. 'KH 4S 9D'). Type 'mix' to hash, 'finished' to move on.
> 6S AH AS 3S 8C 7D 6H 3C KC 6D
Entropy pool: 55.67 bits, deck remaining: 42
> 8S 3H AD JH 5H 7H 5C QS QH 8D
Entropy pool: 107.92 bits, deck remaining: 32
> fin
```

Output:
```
Dice per batch (default 6):
Dice: [4, 3, 5, 2, 1, 3]
Press Enter for next batch, or 'q' to quit:
Dice: [2, 1, 1, 4, 2, 3]
Press Enter for next batch, or 'q' to quit:
Dice: [6, 6, 6, 3, 1, 3]
Press Enter for next batch, or 'q' to quit:
Done: Not enough mixed bytes in reservoir; call mix() or add more cards.
```

## Why This Matters
Entropy conversion is subtle. If you convert between bases incorrectly, you can discard randomness (entropy loss), or create biased digits (entropy inflation). Both are dangerous in cryptographic contexts. This project demonstrates how to convert entropy correctly, even though it is not intended for real‑world security.

## Usage
```
python convert_cards.py
```
