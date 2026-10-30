"""Generates data.6502 and consts.6502 for CHUCKIE APPLE v2 (BBC Micro).

Everything visual is drawn here as text so it can be edited easily:
  . black  R red  G green  Y yellow  B blue  M magenta  C cyan  W white
  r flashing red/cyan   y flashing yellow/blue
Run:  python3 gen_data.py      (build.py does this for you)

Screen: MODE 2, full width, 28 character rows: 40 x 28 cells, each 4 pixels
wide and 8 lines tall (square on screen). Rows 0-2 are the status area,
rows 3-27 the playfield (40 x 25, walls included).
"""

COL = {'.': 0, 'R': 1, 'G': 2, 'Y': 3, 'B': 4, 'M': 5, 'C': 6, 'W': 7,
       'r': 9, 'y': 11}

def mode2_byte(left, right):
    """MODE 2: two pixels per byte, bits interleaved.
    left pixel colour bits 3,2,1,0 -> byte bits 7,5,3,1; right -> 6,4,2,0"""
    b = 0
    for bit in range(4):
        if left & (1 << bit):  b |= 1 << (2 * bit + 1)
        if right & (1 << bit): b |= 1 << (2 * bit)
    return b

def colbytes(rows):
    """picture -> bytes column by column, the order screen memory uses"""
    w = len(rows[0])
    assert w % 2 == 0 and all(len(r) == w for r in rows), rows
    out = []
    for bc in range(w // 2):
        for r in rows:
            out.append(mode2_byte(COL[r[bc * 2]], COL[r[bc * 2 + 1]]))
    return out

def mirror(rows): return [r[::-1] for r in rows]
def quarter(rows, qx, qy):
    return [r[qx * 4:qx * 4 + 4] for r in rows[qy * 8:qy * 8 + 8]]

# ============================================================ tiles (4 x 8)
EMPTY = ["...."] * 8
STUFF = ["G...", ".G..", "..G.", "...G", "G...", ".G..", "..G.", "...G"]
WALL = ["MMMM", "MMMM", "MM.M", "MMMM", "MMMM", "M.MM", "MMMM", "MMMM"]
CHUTE_UP = ["....",       # the apple chutes: gaps in the wall with arrows
            ".YY.",       # pointing the way the apples leave
            "YYYY",
            ".YY.",
            ".YY.",
            ".YY.",
            "....",
            "...."]
CHUTE_LEFT = ["....",
              "....",
              ".Y..",
              "YYYY",
              "YYYY",
              ".Y..",
              "....",
              "...."]
CHUTE_RIGHT = mirror(CHUTE_LEFT)
EXITSHUT = ["RRRR", "R..R", "RRRR", "R..R", "RRRR", "R..R", "RRRR", "R..R"]
EXITOPEN = ["....",       # flashes, thanks to MODE 2's flashing colours
            "..r.",
            "..rr",
            "rrrr",
            "rrrr",
            "..rr",
            "..r.",
            "...."]
ENTRANCE = ["BBBB", "B..B", "B..B", "B..B", "B..B", "B..B", "B..B", "BBBB"]
CUP = ["........",
       "........",
       "YYYYYYYY",
       "YWYYYYYY",
       "YWYYYYYY",
       ".YYYYYY.",
       ".YYYYYY.",
       "..YYYY..",
       "...YY...",
       "...YY...",
       "...YY...",
       "...YY...",
       "..YYYY..",
       ".YYYYYY.",
       "........",
       "........"]
TILES = [EMPTY, STUFF, WALL, CHUTE_UP, CHUTE_LEFT, CHUTE_RIGHT, EXITSHUT, EXITOPEN, ENTRANCE,
         quarter(CUP, 0, 0), quarter(CUP, 1, 0), quarter(CUP, 0, 1), quarter(CUP, 1, 1)]

# map codes (one picture each, same numbers)
C_EMPTY, C_STUFF, C_WALL, C_GATEU, C_GATEL, C_GATER = 0, 1, 2, 3, 4, 5
C_EXIT, C_EXITOPEN, C_ENTRANCE, C_CUP = 6, 7, 8, 9          # cup is 9-12
P_BLOCKMAN = 1    # man and monsters can't go in
P_DIG      = 2    # stuff: the man digs it, the digger monster digs it
P_BLOCKOBJ = 4    # apples and crates bounce off it
P_GATE     = 8    # apples go through, crates treat it as wall
P_EXIT     = 16   # walking in here finishes the level
P_CUP      = 32   # the cup
P_HARD     = 64   # pushed apples/crates can't go in (but they can plough stuff)
P_TOP      = 128  # the top chute: crates carried up go out here too
PROPS = {C_EMPTY: 0,
         C_STUFF: P_DIG | P_BLOCKOBJ,
         C_WALL: P_BLOCKMAN | P_BLOCKOBJ | P_HARD,
         C_GATEU: P_BLOCKMAN | P_GATE | P_TOP, C_GATEL: P_BLOCKMAN | P_GATE, C_GATER: P_BLOCKMAN | P_GATE,
         C_EXIT: P_BLOCKMAN | P_BLOCKOBJ | P_HARD,
         C_EXITOPEN: P_EXIT | P_BLOCKOBJ | P_HARD,
         C_ENTRANCE: P_BLOCKMAN | P_BLOCKOBJ | P_HARD}
for q in range(4): PROPS[C_CUP + q] = P_CUP | P_BLOCKOBJ | P_HARD
NCODES = 13

# ======================================================= sprites (8 x 16)
MAN_R1 = ["...BBB..",
          "..BBBBBB",
          "...YYYY.",
          "...Y.YY.",
          "...YYYY.",
          "....YY..",
          "..WWWW..",
          ".WWWWWW.",
          ".W.WW.W.",
          ".Y.WW.Y.",
          "...WW...",
          "..CCCC..",
          "..C..C..",
          ".CC...C.",
          ".C....CC",
          "RR....R."]
MAN_R2 = MAN_R1[:11] + ["..CCCC..", "...CC...", "...CC...", "...CC...", "...RRR.."]
MAN_UD1 = ["..BBBB..",
           ".BBBBBB.",
           "..YYYY..",
           "..YYYY..",
           "..YYYY..",
           "...YY...",
           "Y.WWWW.Y",
           ".WWWWWW.",
           "..WWWW..",
           "..WWWW..",
           "..WWWW..",
           "..CCCC..",
           "..C..C..",
           "..C..C..",
           "..C..RR.",
           ".RR....."]
MAN_UD2 = mirror(MAN_UD1)
APPLE = ["....G...",
         "...G.GG.",
         "...GGG..",
         ".RR.RRR.",
         "RRRRRRRR",
         "RWRRRRRR",
         "RWRRRRRR",
         "RRRRRRRR",
         "RRRRRRRR",
         "RRRRRRRR",
         "RRRRRRRR",
         "RRRRRRRR",
         ".RRRRRR.",
         ".RRRRRR.",
         "..RR.RR.",
         "........"]
GOLD = [r.replace('R', 'Y').replace('W', 'W') for r in APPLE]
GHOST = ["....W...", "........", "........", ".WW.WWW.", "W......W", "........",
         "W......W", "........", "W......W", "........", "W......W", "........",
         ".W....W.", "........", "..WW.WW.", "........"]
BOX = ["YYYYYYYY",
       "Y......Y",
       "Y.RRRR.Y",
       "Y.R..R.Y",
       "Y.R..R.Y",
       "Y.R..R.Y",
       "Y.RWWR.Y",
       "Y.RWWR.Y",
       "Y.RWWR.Y",
       "Y.RWWR.Y",
       "Y.R..R.Y",
       "Y.R..R.Y",
       "Y.R..R.Y",
       "Y.RRRR.Y",
       "Y......Y",
       "YYYYYYYY"]
BANG1 = ["........", "........", "........", "...YY...", "..YRRY..", ".YRRRRY.",
         "YRRYYRRY", ".YRYYRY.", "YRRYYRRY", ".YRRRRY.", "..YRRY..", "...YY...",
         "........", "........", "........", "........"]
BANG2 = ["Y......Y", "..R..R..", "........", ".R.YY.R.", "...RR...", "Y.R..R.Y",
         "..Y..Y..", "R......R", "..Y..Y..", "Y.R..R.Y", "...RR...", ".R.YY.R.",
         "........", "..R..R..", "Y......Y", "........"]
MONA1 = ["........", "........", "..CCCC..", ".CCCCCC.", "CCWCCWCC", "CCBCCBCC",
         "CCCCCCCC", "CCCCCCCC", "CRRRRRRC", "CCRRRRCC", "CCCCCCCC", "CCCCCCCC",
         ".CCCCCC.", "C.C..C.C", "C.C..C.C", "........"]
MONA2 = MONA1[:13] + [".C.CC.C.", ".C.CC.C.", "........"]
MONB1 = ["M......M", ".M....M.", "..RRRR..", ".RRRRRR.", "RRYRRYRR", "RRYRRYRR",
         "RRRRRRRR", "RRWWWWRR", "RRW.W.RR", "RRRRRRRR", ".RRRRRR.", "..RRRR..",
         ".R.RR.R.", "R..RR..R", "R......R", "........"]
MONB2 = MONB1[:12] + ["..RRRR..", ".R....R.", ".RR..RR.", "........"]
MONC1 = ["........", "...BB...", "..BBBB..", ".BBBBBB.", ".BWBBWB.", ".BBBBBB.",
         "..BWWB..", "..BWWB..", "...WW...", ".BBBBBB.", "BBBBBBBB", "BBBBBBBB",
         ".BBBBBB.", ".B.BB.B.", "B..BB..B", "........"]
MONC2 = MONC1[:13] + ["B.B..B.B", ".B....B.", "........"]
# the UXB: an orange apple (red and yellow, there's no orange in MODE 2)
# with a lit fuse
UXB = ["....W...",
       "...Y....",
       "...B....",
       ".RYBRYR.",
       "RYRYRYRY",
       "YWYRYRYR",
       "RWRYRYRY",
       "YRYRYRYR",
       "RYRYRYRY",
       "YRYRYRYR",
       "RYRYRYRY",
       "YRYRYRYR",
       ".YRYRYR.",
       ".RYRYRY.",
       "..YR.RY.",
       "........"]
# the power ball: a little ball in byte column 1 (pixels 2-3), lines 6-9
BALL = ["........"] * 6 + ["..WW....", "..YY....", "..YY....", "..WW...."] + ["........"] * 6

SPRITES = [MAN_R1, MAN_R2, mirror(MAN_R1), mirror(MAN_R2), MAN_UD1, MAN_UD2,  # 0-5
           APPLE, BOX, GHOST, BANG1, BANG2,                                    # 6-10
           MONA1, MONA2, MONB1, MONB2, MONC1, MONC2,                           # 11-16
           GOLD, BALL, UXB]                                                    # 17-19

LIFE = ["BBB.", ".YY.", "WWWW", ".WW.", ".CC.", "C..C", "R..R", "...."]
TALLY = ["...G....", "..RGRR..", ".RWRRRR.", ".RWRRRR.", ".RRRRRR.", "..RRRR..", "...RR...", "........"]
BALLICON = ["....", ".WW.", "WYYW", "WYYW", ".WW.", "....", "....", "...."]
MINIS = [LIFE, TALLY, BALLICON]     # offsets 0, 16 (two cells), 48

# ================================================== font: 4 x 8, 1 bit
FONT_CHARS = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.:/-!()"
FONT_SRC = """
.... ### .#. ### ### #.# ### ### ### ### ###
.... #.# ##. ..# ..# #.# #.. #.. ..# #.# #.#
.... #.# .#. ### ### ### ### ### ..# ### ###
.... #.# .#. #.. ..# ..# ..# #.# ..# #.# ..#
.... ### ### ### ### ..# ### ### ..# ### ###
###  ##. ### ##. ### ### ### #.# ### ..# #.# #.. #.# ##. ### ###
#.#  #.# #.. #.# #.. #.. #.. #.# .#. ..# #.# #.. ### #.# #.# #.#
###  ##. #.. #.# ##. ##. #.# ### .#. ..# ##. #.. ### #.# #.# ###
#.#  #.# #.. #.# #.. #.. #.# #.# .#. #.# #.# #.. #.# #.# #.# #..
#.#  ##. ### ##. ### #.. ### #.# ### ### #.# ### #.# #.# ### #..
### ##. ### ### #.# #.# #.# #.# #.# ### ... ... ..# ... .#. .#. #..
#.# #.# #.. .#. #.# #.# #.# #.# #.# ..# ... .#. ..# ... .#. #.. .#.
#.# ##. ### .#. #.# #.# #.# .#. ### .#. ... ... .#. ### .#. #.. .#.
### #.# ..# .#. #.# #.# ### #.# ..# #.. ... .#. #.. ... ... #.. .#.
.## #.# ### .#. ### .#. ### #.# ### ### .#. ... #.. ... .#. .#. #..
"""
def parse_font():
    blocks = FONT_SRC.strip("\n").split("\n")
    glyphs = []
    for g in (blocks[0:5], blocks[5:10], blocks[10:15]):
        cols = [row.split() for row in g]
        for i in range(len(cols[0])):
            glyphs.append([cols[r][i] for r in range(5)])
    assert len(glyphs) == len(FONT_CHARS)
    out = []
    for g in glyphs:
        rows = ["...."] + [(r + "....")[:4] for r in g] + ["....", "...."]
        bits = []
        for r in rows:
            v = 0
            for i, c in enumerate(r[:4]):
                if c == '#': v |= 8 >> i
            bits.append(v)
        out.append(bits)
    return out

# ============================================================== the levels
# The playfield is 40 x 25 cells (rows are numbered 0-24 here; on screen
# they're rows 3-27). Each level starts as stuff inside a wall, then
# tunnels are carved out and things placed.
W, H = 40, 25
TOPROW = 4                # screen row of the playfield's top wall

class Level:
    def __init__(self, name):
        self.name = name
        self.g = [[C_STUFF] * W for _ in range(H)]
        for c in range(W):
            self.g[0][c] = self.g[H - 1][c] = C_WALL
        for r in range(H):
            self.g[r][0] = self.g[r][W - 1] = C_WALL
        self.apples, self.boxes = [], []
    def carve(self, c, r, w, h):
        for rr in range(r, r + h):
            for cc in range(c, c + w):
                assert 1 <= cc <= W - 2 and 1 <= rr <= H - 2, (self.name, cc, rr)
                self.g[rr][cc] = C_EMPTY
    def gates(self):
        """the three chutes Nigel drew: top middle, and both bottom corners"""
        self.g[0][19] = self.g[0][20] = C_GATEU
        self.g[22][0] = self.g[23][0] = C_GATEL
        self.g[22][W - 1] = self.g[23][W - 1] = C_GATER
    def doors(self, entrance_row, exit_row):
        self.ent, self.exitr = entrance_row, exit_row
        self.g[entrance_row][0] = self.g[entrance_row + 1][0] = C_ENTRANCE
        self.g[exit_row][W - 1] = self.g[exit_row + 1][W - 1] = C_EXIT
    def cup(self, c, r):
        self.cupc, self.cupr = c, r
        for q, (dc, dr) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
            self.g[r + dr][c + dc] = C_CUP + q
    def apple(self, c, r): self.apples.append((c, r)); self.carve(c, r, 2, 2)
    def box(self, c, r): self.boxes.append((c, r)); self.carve(c, r, 2, 2)
    def check(self):
        g = self.g
        assert len(self.apples) == 6, self.name
        assert len(self.boxes) <= 2, self.name
        things = self.apples + self.boxes
        seen = set()
        for (c, r) in things:
            for dc in (0, 1):
                for dr in (0, 1):
                    assert (c + dc, r + dr) not in seen, (self.name, "overlap", c, r)
                    seen.add((c + dc, r + dr))
            below = [g[r + 2][c], g[r + 2][c + 1]]
            assert all(PROPS[b] & P_BLOCKOBJ for b in below) or (c, r + 2) in [(x, y) for x, y in things], \
                (self.name, "would fall at the start", c, r)
        # the cup (where monsters hatch) must join up with the man's tunnels
        open_ = lambda c, r: g[r][c] == C_EMPTY or g[r][c] >= C_CUP or (c, r) in seen
        start = (self.cupc, self.cupr); todo = [start]; reach = {start}
        while todo:
            c, r = todo.pop()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c + dc, r + dr)
                if n not in reach and 0 <= n[0] < W and 0 <= n[1] < H and open_(*n):
                    reach.add(n); todo.append(n)
        assert (1, self.ent) in reach, (self.name, "the monsters are shut in")
        # the man starts just inside the entrance
        assert g[self.ent][1] == g[self.ent][2] == g[self.ent + 1][1] == g[self.ent + 1][2] == C_EMPTY, self.name
        assert (1, self.ent) not in seen and (2, self.ent) not in seen
        return self

def nigel():
    """Nigel Alderton's sketch, widened from 32 x 18 to 40 x 25 cells"""
    L = Level("NIGEL")
    L.carve(9, 1, 2, 23)      # left shaft
    L.carve(19, 1, 2, 23)     # middle shaft, from the top chute to the bottom
    L.carve(1, 11, 8, 2)      # entrance corridor
    L.carve(1, 22, 20, 2)     # bottom corridor to the left chute
    L.carve(34, 11, 5, 2)     # the exit's pocket (dig in to it)
    L.gates(); L.doors(11, 11); L.cup(19, 11)
    for c, r in [(11, 5), (14, 12), (3, 17), (24, 5), (30, 4), (29, 17)]: L.apple(c, r)
    L.box(3, 4); L.box(33, 18)
    return L.check()

def twin():
    """two shafts joined by two long corridors"""
    L = Level("TWIN")
    L.carve(6, 1, 2, 23); L.carve(32, 1, 2, 23)
    L.carve(6, 7, 28, 2); L.carve(6, 16, 28, 2)
    L.carve(19, 1, 2, 6)                          # from the top chute
    L.carve(1, 3, 5, 2)                           # entrance corridor
    L.carve(1, 22, 5, 2); L.carve(34, 22, 5, 2)   # bottom corners
    L.carve(35, 3, 4, 2)                          # exit pocket
    L.carve(19, 9, 2, 7)                          # the cup opens on both corridors
    L.gates(); L.doors(3, 3); L.cup(19, 11)
    for c, r in [(12, 4), (25, 4), (10, 13), (27, 13), (15, 19), (24, 19)]: L.apple(c, r)
    L.box(2, 13); L.box(36, 13)
    return L.check()

def ring():
    """a ring road round the middle"""
    L = Level("RING")
    L.carve(6, 5, 28, 2); L.carve(6, 18, 28, 2)
    L.carve(6, 5, 2, 15); L.carve(32, 5, 2, 15)
    L.carve(19, 1, 2, 4)                          # top chute to the ring
    L.carve(1, 11, 5, 2)                          # entrance to the ring
    L.carve(36, 11, 3, 2)                         # exit pocket
    L.carve(1, 22, 38, 2)                         # bottom road, chute to chute
    L.carve(21, 11, 11, 2)                        # the cup opens to the east side of the ring
    L.gates(); L.doors(11, 11); L.cup(19, 11)
    for c, r in [(10, 2), (28, 2), (12, 8), (26, 8), (10, 14), (28, 14)]: L.apple(c, r)
    L.box(2, 3); L.box(36, 3)
    return L.check()

def stairs():
    """a staircase of corridors, with an apple waiting over an apple"""
    L = Level("STAIRS")
    L.carve(1, 3, 12, 2); L.carve(11, 3, 2, 7)
    L.carve(10, 8, 13, 2); L.carve(21, 8, 2, 7)
    L.carve(20, 13, 13, 2); L.carve(31, 13, 2, 7)
    L.carve(28, 18, 11, 2)
    L.carve(19, 1, 2, 7)                          # top chute down to the stairs
    L.carve(1, 22, 10, 2)                         # bottom left corner
    L.carve(7, 15, 14, 2)                         # a tunnel from the cup to the stairs
    L.gates(); L.doors(3, 18); L.cup(5, 15)
    for c, r in [(14, 5), (24, 10), (24, 6), (34, 9), (3, 9), (16, 17)]: L.apple(c, r)
    L.box(36, 5); L.box(6, 19)
    return L.check()

LEVELS = [nigel(), twin(), ring(), stairs()]

def rle(grid):
    out = []
    cells = [v for row in grid for v in row]
    i = 0
    while i < len(cells):
        v = cells[i]; n = 1
        while i + n < len(cells) and cells[i + n] == v and n < 15: n += 1
        out.append((n << 4) | v); i += n
    return out

def emit():
    out = ["\\ Generated by gen_data.py - edit that, not this", ""]
    def lines(label, data):
        out.append("." + label)
        for i in range(0, len(data), 16):
            out.append("    EQUB " + ",".join("&%02X" % b for b in data[i:i + 16]))
    t = []
    for tile in TILES:
        assert len(tile) == 8 and all(len(x) == 4 for x in tile)
        t += colbytes(tile)
    lines("tiles", t)
    s = []
    for spr in SPRITES:
        assert len(spr) == 16, len(spr)
        s += colbytes(spr)
    lines("sprites", s)
    m = []
    for mini in MINIS: m += colbytes(mini)
    lines("minis", m)
    f = []
    for g in parse_font():
        f += [(g[i] << 4) | g[i + 1] for i in range(0, 8, 2)]
    lines("font", f)
    out.append(".lmask   EQUB " + ",".join("&%02X" % mode2_byte(c, 0) for c in range(16)))
    out.append(".rmask   EQUB " + ",".join("&%02X" % mode2_byte(0, c) for c in range(16)))
    fm = [FONT_CHARS.index(chr(a)) if chr(a) in FONT_CHARS else 0 for a in range(32, 96)]
    out.append(".fontmap EQUB " + ",".join(str(v) for v in fm))
    out.append(".props   EQUB " + ",".join(str(PROPS[i]) for i in range(NCODES)))
    total = 0
    for n, L in enumerate(LEVELS):
        d = rle(L.g); total += len(d)
        lines("lev%d" % n, d)
    out.append("\\ %d bytes of level maps" % total)
    out.append(".levlo   EQUB " + ",".join("LO(lev%d)" % n for n in range(len(LEVELS))))
    out.append(".levhi   EQUB " + ",".join("HI(lev%d)" % n for n in range(len(LEVELS))))
    out.append(".levcupc EQUB " + ",".join(str(L.cupc) for L in LEVELS))
    out.append(".levcupr EQUB " + ",".join(str(L.cupr + TOPROW) for L in LEVELS))
    out.append(".levent  EQUB " + ",".join(str(L.ent + TOPROW) for L in LEVELS))
    out.append(".levexit EQUB " + ",".join(str(L.exitr + TOPROW) for L in LEVELS))
    tx, ty, tt = [], [], []
    for L in LEVELS:
        things = [(c, r, "T_APPLE") for c, r in L.apples] + [(c, r, "T_BOX") for c, r in L.boxes]
        things += [(1, 1, "T_NONE")] * (8 - len(things))
        tx += [str(c * 2) for c, r, k in things]
        ty += [str((r + TOPROW) * 8) for c, r, k in things]
        tt += [k for c, r, k in things]
    out.append(".thingx  EQUB " + ",".join(tx))
    out.append(".thingy  EQUB " + ",".join(ty))
    out.append(".thingt  EQUB " + ",".join(tt))
    print("\n".join(out))

    consts = ["\\ Generated by gen_data.py", "NTHINGS = 8", "NAPPLES = 6",
              "NLEVELS = %d" % len(LEVELS)]
    for name in ["C_EMPTY", "C_STUFF", "C_WALL", "C_EXIT", "C_EXITOPEN", "C_CUP",
                 "P_BLOCKMAN", "P_DIG", "P_BLOCKOBJ", "P_GATE", "P_EXIT", "P_CUP", "P_HARD", "P_TOP"]:
        consts.append("%s = %d" % (name, globals()[name]))
    open("consts.6502", "w").write("\n".join(consts) + "\n")

def show():
    """print the levels as text, for checking"""
    ch = {C_EMPTY: ' ', C_STUFF: '.', C_WALL: '#', C_GATEU: '^', C_GATEL: '<', C_GATER: '>',
          C_EXIT: 'E', C_ENTRANCE: 'N', 9: 'c', 10: 'c', 11: 'c', 12: 'c'}
    for L in LEVELS:
        rows = [[ch[v] for v in row] for row in L.g]
        for c, r in L.apples:
            for dc in (0, 1):
                for dr in (0, 1): rows[r + dr][c + dc] = 'A'
        for c, r in L.boxes:
            for dc in (0, 1):
                for dr in (0, 1): rows[r + dr][c + dc] = 'X'
        print(L.name)
        print("\n".join("".join(r) for r in rows))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1: show()
    else: emit()
