CHUCKIE APPLE  -  for the BBC Micro Model B
===========================================

The sequel to Chuckie Egg that never was. In 1983 Nigel Alderton, author of
Chuckie Egg, designed "Chuckie Apple" before joining Ocean, but it was never
finished. His original design notes were published, with his permission and
under a Creative Commons Attribution 2.5 licence, by The Chuckie Egg
Professional's Resource Kit:  http://www.bagshot-row.org/chuckie-egg/

This is a native BBC Micro version built from that design: 6502 machine code,
MODE 2, four levels (Nigel's own sketched level first, then three more).

Original design: Nigel Alderton, 1983 (CC BY 2.5)
BBC Micro version: D8fydd-Beep, 2026


LOADING
-------
Disc / MMFS / Gotek:   boot APPLE.ssd with SHIFT-BREAK, or  *RUN APPLE
Tape (APPLE.uef):      *TAPE  then  *RUN   (about 2 3/4 minutes)

Runs on a standard 32K Model B. It takes over the machine (it uses the
filing system's workspace once loaded), so press BREAK to leave.


KEYS
----
Z left    X right    : up    / down
SPACE     kick an apple / grab a crate
RETURN    throw a ball


HOW TO PLAY
-----------
Dig through the stuff. Get all six apples off the screen through the three
arrow chutes, and clear away every crate and golden apple too - then the exit
opens. Walk out of it to finish the level. (A crate shoved out of a side
chute is away for a couple of seconds - the exit is open until it's back.)

* Undermine an apple and it falls - onto monsters, if you time it right.
  An apple landing on another apple smashes the lower one (that counts!).
* Walk under an apple and it rides on your head. Carry it up the middle
  shaft and out of the top chute.
* Tap SPACE with an apple on your head to pop it up, then step away - it
  drops behind you onto whatever's chasing you.
* Push apples sideways (several at once is harder work). Kick them with
  SPACE and they slide. Kick one that can't move and it explodes - it comes
  back as a ghost when you next walk through where it was.
* Push all six out of a chute in one unbroken line for the SUPER BONUS:
  ten times the bonus, and four levels on.
* Crates: hold SPACE and walk away to pull one. Carry one out of the top
  chute to earn a ball (hold up to three). It turns up again elsewhere.
  A crate stuck at the bottom can be shoved out of a side chute.
* A ball bounces round the tunnels and kills the first monster it meets.
  Hit a crate with it and it becomes a GOLDEN APPLE - get it out of any
  chute for an EXTRA LIFE (up to 9).
* Anything pushed, lifted, dropped or kicked into a monster squashes it.
* UXB apples (orange) turn up now and then with a 10 second fuse. Walk into
  one to defuse it. Leave it and it blows a crater - and you, if you're close.
* Watch the TIME. An extra life every 10,000 points.


POKES
-----
In true 8-bit tradition you can change how the game plays. Load it without
running it, poke new values in, then start it:

    *LOAD APPLE              (disc)   or   *TAPE then *LOAD ""   (tape)
    ?&2D79=75
    CALL &4218

  ?&2D79=n   How long a crate stays away after you shove it out of a
             chute, in 25ths of a second. Normally 50 (2 seconds). If you
             can't escape before the last crate comes back, try 75 (3 s)
             or 125 (5 s). Up to 255.
  ?&1945=n   Lives at the start, 1-9. Normally 5.
  ?&194F=n   Balls at the start, 0-3. Normally 0.
  ?&2FB3=n   Speed of the cyan monster. Normally 80; lower is slower.
  ?&2FB4=n   Speed of the red monster. Normally 112.
  ?&2FB5=n   Speed of the digger. Normally 56. (Keep all three under 200.)
  ?&22BF=n   Hundreds digit of the TIME you start each life with, 1-9.
             Normally 9.
  ?&345B=0 and ?&345C=0   Silence the footsteps.

  To turn off all sound, type *FX210,1 before starting the game
  (*FX210,0 turns it back on).

To keep your changes, save it after poking (disc):

    *SAVE APPLE FFFF1900 +293D FFFF4218


SOURCE
------
source/ has the full commented 6502 source (BeebAsm) and the Python script
that draws the graphics and levels. build.py rebuilds everything:
    python3 build.py path/to/beebasm
