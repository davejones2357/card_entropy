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
If cards are drawn **without replacement**, the total entropy available is 
```math
\log_2(52!) \approx 67.9
```
bits. The 0.9 is significant because it has to be thrown away. 67 bits are available, trying to get 68 would be an error - the highest bit would not be genuinely random. Hence the important part of this exercise: **preserve entropy**.

## Input Format (Base‑13 Card Encoding)
Each playing card is encoded as a two‑character base‑13 number:

Low‑order digit: Suit
|Suit|Symbol|Value|
|---|---|---|
|Heart |H	| 0	|
|Diamond |D 	| 1	|
|Spade |S 	| 2	|
|Club |C 	| 3	|

High‑order digit: Value
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

So for example, AS is the ace of spades and is encoded as 12 in base-52.

This yields 52 valid combinations, even though the encoding space is $$13^2 = 169$$.
The script validates input to ensure only real card combinations are accepted.

## What the Script Does
* Accepts a string of card codes in the two‑digit base‑13 format.
* Converts the sequence into a single large integer (base‑52).
* Re‑encodes that integer into base‑6 digits.
* Outputs a sequence equivalent to rolling M six‑sided dice.
* Ensures no entropy is lost or artificially created.

## Example

Input:
```
AH KD 7S TC
```

Internal representation:
```
10 C1 72 03
```

Output (example):
```
3 5 1 6 2 4 4 1 ...
```

## Why This Matters
Entropy conversion is subtle. If you convert between bases incorrectly, you can:

discard randomness (entropy loss), or

create biased digits (entropy inflation).

Both are dangerous in cryptographic contexts. This project demonstrates how to convert entropy correctly, even though it is not intended for real‑world security.

## Usage
```
python convert_cards.py "AH KD 7S TC"
```

The script prints the base‑6 digits representing the same entropy.
