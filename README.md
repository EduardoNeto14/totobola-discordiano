# totobola-discordiano

This program is a way of automatizing the scores of a game of football predictions.

Each player is asked to guess the results of a number of games and, depending on the result, it can obtain 3 points (if it guesses the right results), 1 point(if it guesses the right tendency) or 0 points (if it's completely wrong).

Also, in each round, the player has the option of using the so-called JOKER(*), which will double his score in a game of its choice (a priori).

## Functionality

This program does not simply count the score of each player. It also is able to:
- format the data in a .csv file in a way that the program can understand;
- get the prediction of Google Sheets (using Google Forms);
- update a local database containing the total scores of different competitions;
- update a local database containing every round of predictions made.
- update Google Sheets with the new total scores.
- if the prediction was made via Google Forms, it can also send the player an email with the score the he got and his position on the table.

## Installation

```shell
pip install -r requirements.txt
```
