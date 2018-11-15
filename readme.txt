V 1.0

Section I. Features:
---

1) Convert .ydk to .txt:

The user selects a .ydk file, it is converted into a text file listing the card names, in the order they are in in the .ydk, and organized by deck location (main, extra, side). It also lists a count of the various card types within the deck.

2) Write Analysis and Deck List to file

The user selects a .ydk file and a Deck Array .csv file [and a Deck Entry file if the Deck Array has not been updated before]. It will create a text file with the deck list and an analysis of the deck.

3) Analyse Deck and Display Results

The user selects a Deck Array .csv file [and a Deck Entry file if the Deck Array has not been updated before]. It will display the results of its analysis in a new window.

4) Display Deck Network

The user selects Deck Array .csv file [and a Deck Entry file if the Deck Array has not been updated before]. It will draw a graph of the deck, with two cards sharing an edge when they share an edge (see the following features).

5) Create/Refresh Deck Array from .ydk

The user selects a .ydk file, and then saves the output file. This must and the following must be run first in order to use 2, 3, or 4. If the user updates their deck (but does not add or remove any cards that would nesseciate upddating via the following feature), they should run this before generating a new deck report.

6) Create/Refresh data-entry form from .ydk
The user selects a .ydk file, and then saves the output file. This must and the following must be run first in order to use 2, 3, or 4.

After generating the file, the user must open it, and for each entry that has a 0 in it, replace that 0 with a 1 when the two card names that intersect there, if they have them in their opening hand, would prevent that hand from being a dead hand. If two copies of the same card name do this, write a '1' in the row/column intersection of that card name.

For example, in a Gouki deck, the row/column intersection of Gouki Twistcobra and Gouki Suprex would have a 1 in it.

Also, if a card, by itself, prevents a hand from being dead, then every entry should be 1. For example, under the current banlist, in many decks, Armageddon Knight has this property, as it singlehandedly allows for a massive play (and so too, ROTA is the same, for it gives one access to Armageddon Knight).

7) Select Directories

Opens a drop-down menu. The user must set the path to their ygopro folder in order for features 1 and 2 to work. The other option is optional.


---
Section II. Explanation of Analysis:
---

The program uses the user input from I.5 I.6 to check every possible opening hand (assuming one goes first, the case of going second will be address in a later version), and computes:

a) How many hands brick

b) How many hands don't brick, and in how many ways there are to do each kind of not-bricking.

c) The probability of bricking in a single duel

d) The probability of bricking at least once in a match

Added to Github!