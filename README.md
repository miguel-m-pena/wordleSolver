# wordleSolver

As a massive Wordle fan, I had to make this sooner or later. It essentially works by getting a list of english words from a corpus provided by the NLTK library, and then filtering this down to 5 letter words.

I have borrowed and adapted the Website class from another user as I struggled greatly to interact with the Wordle website due to its use of the shadow DOM. I had found other work arounds, but none were as clean, and there's no need to reinvent the wheel. 

From here, the program finds the most frequent letters for each position and checks if together they form a word, if they don't, then it backtracks up a branch and tries the next most frequent. If it completed a cycle in a position and no word was found, it changes from the previous position and begins to cycle again. 

This program plays following the rules of hardmode.


Possible Improvements: Further optimize by having the program investigate further the case when there is more than one piece of information about a letter. At this point, it accounts for this rather rudimentarily. Another improvement would be not guessing duplicate letters until later guesses. Yet another improvement would be to take into account the letters around a position for determining the most frequent letter and thus the best guess.

Support has been implemented for choosing a starting word.
