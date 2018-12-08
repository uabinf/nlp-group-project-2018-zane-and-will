Running:
--------

run `repl.py`, this will automatically load/create the model for the /news/
board.

at the repl prompt (`> `), you may type commands as you wish. Typing `:?` shows
the following help:

  ':q           -- quit.'
  ':o board     -- load a board model, building it if not found.'
  ':o! board    -- load a board model, building it.'
  ':w           -- save a board model.'
  ':[bm/r]      -- rebuilds the current model.'
  ':bn i j      -- builds i-grams through j-grams.'
  ':c w1, w2    -- compares the similarity of w1 and w2.'
  ':e stem      -- shows all words that reduce to that stem.'
  ':n n [x]     -- shows the top x n-grams.'
  ':kgen k      -- creates k clusters with k-means algorithm.'
  ':k word      -- shows which k-cluster the given word is in'
  '<word> [x]   -- shows the top x most similar words to word.'

when naming a board, omit /'s , so /pol/ is loaded with `:o pol`

options in brackets [] are optional and have default values.

other scripts are included for posterity, but aren't required. Also they operate
on the raw json data which I'm not including since you only really need the text.


Work Distribution:
------------------

Will: Presentation Maker, Loudest Speaker, Ideas Guy
Zane: Programming, Sleepiest Speaker, Data Collection

