# Chuckie Apple

**The Chuckie Egg sequel that never was — a native BBC Micro game built from Nigel Alderton's original 1983 design notes.**

### [▶ Play it in your browser](https://bbc.godbolt.org/?disc=https://raw.githubusercontent.com/d8fydd73-beep/chuckie-apple/main/APPLE.ssd&autoboot)

![Title screen](title.png) ![Playing level 1](game.png)

## The story

After *Chuckie Egg* came out in 1983, Nigel Alderton started work on a follow-up — a Mr Do!-style digging game starring Hen House Harry, full of bouncing, falling, kickable apples. He left to join Ocean Software before it was finished, and the game was never made. His hand-drawn design notes were later published, with his permission, by [The Chuckie Egg Professional's Resource Kit](http://www.bagshot-row.org/chuckie-egg/) under a Creative Commons Attribution 2.5 licence.

This is that game, built for the machine it belongs on: 6502 machine code for the BBC Micro Model B, in MODE 2, with Nigel's own sketched level as level 1 and three more after it.

## Loading

| | |
|---|---|
| **Disc / MMFS / Gotek** | `APPLE.ssd` — SHIFT-BREAK to boot, or `*RUN APPLE` |
| **Tape** | `APPLE.uef` — `*TAPE` then `*RUN` (about 2¾ minutes) |
| **Emulators** | Use `APPLE.ssd` in BeebEm, b2 or jsbeeb. No disc drive? Load `APPLE.uef` from your phone with the [UEF Tape Deck](https://d8fydd73-beep.github.io/uef-tape-deck/). In BeebEm, set *Options → Keyboard Mapping → Default Mapping* so the `:` key works. |

Needs a standard 32K Model B. Press BREAK to leave.

## Keys

| Key | |
|---|---|
| `Z` / `X` | left / right |
| `:` / `/` | up / down |
| `SPACE` | kick an apple · grab a crate · pop an apple off your head |
| `RETURN` | throw a ball |

## How to play

Dig through the stuff and get all six apples off the screen through the three arrow chutes — and clear away every crate and golden apple too. Then the exit opens: walk out of it to finish the level. A crate shoved out of a side chute is away for a couple of seconds, so if it's the last one, the exit is open until it comes back — run for it!

- **Undermine an apple** and it falls — onto monsters, if you time it right. An apple landing on another apple smashes the lower one (and that counts).
- **Walk under an apple** and it rides on your head. Carry it up the middle shaft and out of the top chute. Tap SPACE to pop it up, then step away — it drops behind you onto whatever's chasing you.
- **Push apples** sideways (several at once is harder work), or **kick** them and they slide. Kick one that can't move and it explodes — a few seconds later it comes back where it was.
- **Super bonus:** push all six out of a chute in one unbroken line for ten times the bonus, and four levels on.
- **Crates:** hold SPACE and walk away to pull one. Carry one out of the top chute to earn a **ball** (hold up to three); the crate turns up again somewhere else. A crate stuck on the bottom can be shoved out of a side chute.
- **The ball** bounces round the tunnels and kills the first monster it meets. Hit a crate with it and it becomes a **golden apple** — get it out of any chute for an **extra life** (up to 9).
- **UXB apples** (orange) turn up with a 10-second fuse. Walk into one to defuse it — or it blows a crater in the stuff, and you with it if you're close.
- **The gold cup** is worth 1000 points, and it's the monster nest: they keep hatching there even once it's gone. Leave anything on the nest and the next monster out bursts it.
- Anything pushed, lifted, dropped or kicked into a monster squashes it. Watch the TIME, and there's an extra life every 10,000 points.

## Pokes

In true 8-bit tradition, you can change how the game plays by poking new values into it before it runs. Load it without running it, poke, then start it with `CALL &421B`:

```
*LOAD APPLE          (disc)   or   *TAPE  then  *LOAD ""   (tape)
?&2D74=75
CALL &421B
```

| Poke | What it does | Normal |
|---|---|---|
| `?&2D74=n` | How long a crate stays away after you shove it out of a chute, in 25ths of a second. If you can't escape before the last crate comes back, try 75 (3 s) or 125 (5 s). Up to 255. | 50 (2 s) |
| `?&1945=n` | Lives at the start (1–9) | 5 |
| `?&194F=n` | Balls at the start (0–3) | 0 |
| `?&2FAE=n` `?&2FAF=n` `?&2FB0=n` | Speed of the three monsters (cyan, red, digger) — lower is slower. Keep them under 200. | 80, 112, 56 |
| `?&22BF=n` | Hundreds digit of the TIME you start each life with (1–9) | 9 |
| `?&345E=0` `?&345F=0` | Silence the footsteps | &FC, &FF |
| `?&3347=n` | The lowest note of the bonus count at the end of a level — higher is a higher tune (keep it under 100) | 60 |

To turn off all sound, type `*FX210,1` before starting the game (`*FX210,0` turns it back on).

To keep your changes, save it after poking (disc):

```
*SAVE APPLE FFFF1900 +2940 FFFF421B
```

## Source

`source/` has the full commented 6502 source for [BeebAsm](https://github.com/stardot/beebasm), and the Python script that draws the graphics and builds the levels. To rebuild everything:

```
python3 build.py path/to/beebasm
```

## Credits

- **Original design:** Nigel Alderton, 1983 — licensed [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/)
- **BBC Micro version:** D8fydd-Beep, 2026
