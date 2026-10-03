import curses
import time
import random

TOTAL_STARS = 28
MIN_TERM_HEIGHT = 24
MIN_TERM_WIDTH = 40


def run_level(stdscr, level_num, score, sh, sw,
              player_char="M", colors=None,
              stars_collected=0, key_collected=False,
              cheated=False):
    """
    Retourne (résultat, score, stars_collected, key_collected, cheated)
    résultat : 'win' | 'dead' | 'quit' | 'resize'
    """
    if colors is None:
        colors = {}
    C = lambda k: colors.get(k, 0)

    gravity    = 0.4
    jump_power = -5
    velocity_y = 0.0
    velocity_x = 0.5
    level_width = max(130, sw + 30)


# ══════════════════════════════════════════════════════════════════════
#  DONNÉES PAR NIVEAU
# ══════════════════════════════════════════════════════════════════════

    if level_num == 1:
        sol_y = sh - 2;  enemy_char = "👾"
        enemy_speed = 1;  enemy_move_step = 0.25
        ground = [
            (0,  sol_y, 18), (20, sol_y, 22),
            (43, sol_y, 27), (72, sol_y, 19),
            (92, sol_y, level_width - 92),
        ]
        elevated = [
            (10,  sh-6,  20),   # idx 5
            (40,  sh-10, 25),   # idx 6
            (70,  sh-5,  15),   # idx 7
            (93, sh-8,  22),   # idx 8
        ]
        platforms = ground + elevated
        bricks  = [[12,sh-7],[13,sh-7],[14,sh-7],[42,sh-11],[43,sh-11]]
        enemies = [[15,sh-7,1,5],[45,sh-11,-1,6],[75,sh-6,1,7]]
        stars   = [[71,sol_y-1],[112,sh-9]]
        key_pos = None
        boss    = None

    elif level_num == 2:
        sol_y = sh - 2;  enemy_char = "👻"
        enemy_speed = 1;  enemy_move_step = 0.35
        ground = [
            (0,  sol_y, 15), (18, sol_y, 20),
            (40, sol_y, 18), (60, sol_y, 22),
            (85, sol_y, level_width - 35),
        ]
        elevated = [
            (8,   sh-5,  12),   # idx 5
            (25,  sh-9,  18),   # idx 6
            (50,  sh-6,  10),   # idx 7
            (65,  sh-11, 20),   # idx 8
            (90,  sh-7,  12),   # idx 9
            (108, sh-10, 14),   # idx 10
        ]
        platforms = ground + elevated
        bricks = [
            [10,sh-6],[11,sh-6],
            [27,sh-10],[28,sh-10],[29,sh-10],
            [67,sh-12],[68,sh-12],
            [110,sh-11],[111,sh-11],[112,sh-10],
        ]
        enemies = [
            [10,sh-6,1,5],[22,sol_y-1,1,1],[44,sol_y-1,1,2],
            [65,sol_y-1,-1,3],[90,sol_y-1,1,4],
            [30,sh-10,-1,6],[52,sh-7,1,7],[70,sh-12,-1,8],
        ]
        stars   = [[17,sol_y-1],[75,sh-12],[109,sh-11]]
        key_pos = None
        boss    = None

    elif level_num == 3:
        sol_y = sh - 5;  enemy_char = "👾"
        enemy_speed = 1;  enemy_move_step = 0.35
        ground = [
            (0,  sol_y, 12), (14, sol_y, 14),
            (31, sol_y, 16), (48, sol_y, 19),
            (69, sol_y, 20), (92, sol_y, level_width - 92),
        ]
        elevated = [
            (5,   sh-9,  10),   # idx 6
            (20,  sh-13, 15),   # idx 7
            (40,  sh-8,   8),   # idx 8
            (55,  sh-12, 12),   # idx 9
            (75,  sh-9,  10),   # idx 10
            (90,  sh-13, 18),   # idx 11
            (112, sh-10, 10),   # idx 12
        ]
        platforms = ground + elevated
        bricks = [
            [6,sh-10],[7,sh-10],
            [22,sh-14],[23,sh-14],[24,sh-14],
            [42,sh-9],[43,sh-9],
            [57,sh-13],[58,sh-13],
            [92,sh-14],[93,sh-14],
            [114,sh-11],[115,sh-11],[116,sh-11],
        ]
        enemies = [
            [6,sh-10,1,6],[22,sh-14,-1,7],[41,sh-9,1,8],
            [57,sh-13,-1,9],[76,sh-10,1,10],[92,sh-14,-1,11],
        ]
        stars   = [[13,sol_y-1],[26,sh-14],[68,sol_y-1],[99,sh-14]]
        key_pos = [44, sh-9]
        boss    = None

    elif level_num == 4:
        sol_y = sh - 4;  enemy_char = "👻"
        enemy_speed = 1;  enemy_move_step = 0.35
        ground = [
            (0,  sol_y, 10), (13, sol_y, 12),
            (27, sol_y, 10), (40, sol_y, 15),
            (57, sol_y, 13), (73, sol_y, 12),
            (87, sol_y, level_width - 87),
        ]
        elevated = [
            (5,   sh-7,   8),   # idx 7
            (15,  sh-11, 10),   # idx 8
            (30,  sh-7,   7),   # idx 9
            (42,  sh-12, 14),   # idx 10
            (60,  sh-8,   9),   # idx 11
            (75,  sh-12, 12),   # idx 12
            (92,  sh-7,  10),   # idx 13
            (108, sh-11, 15),   # idx 14
        ]
        platforms = ground + elevated
        bricks = [
            [6,sh-8],[7,sh-8],
            [17,sh-12],[18,sh-12],[19,sh-12],
            [44,sh-13],[45,sh-13],
            [62,sh-9],[63,sh-9],
            [77,sh-13],[78,sh-13],[79,sh-13],
            [110,sh-12],[111,sh-12],
        ]
        enemies = [
            [17,sol_y-1,1,1],
            [45,sol_y-1,-1,3],[62,sol_y-1,1,4],[90,sol_y-1,1,6],
            [8,sh-8,1,7],[20,sh-12,-1,8],[48,sh-13,1,10],
            [63,sh-9,-1,11],[80,sh-13,1,12],[112,sh-12,-1,14],
        ]
        stars   = [[12,sol_y-1],[26,sol_y-1],[57,sol_y-1],[84,sol_y-1],[115,sh-12]]
        key_pos = None
        boss    = None

    elif level_num == 5:
        sol_y = sh - 2;  enemy_char = "🤖"
        enemy_speed = 1;  enemy_move_step = 0.35
        # Souterrain : sol plein, pas de trous, plafond de grotte
        ground = [(0, sol_y, level_width)]  # idx 0 — sol continu  
        elevated = [  
            # ── Plafond de la grotte (stalactites) ────────────────────
            (0,   4,  14),   # idx 1  plafond gauche
            (17,  3,  10),   # idx 2  plafond
            (30,  5,  12),   # idx 3  plafond
            (45,  3,   8),   # idx 4  plafond
            (56,  2,  10),   # idx 5  plafond
            (70,  3,  12),   # idx 6  plafond
            (90,  5,  15),   # idx 7  plafond
            (108, 3,  18),   # idx 8  plafond droit
            # ── Platforme intermediaire ───────────────────────────────
            
            # ── Plateformes basses ────────────────────────────────────
            (8,   sh-8,  12),   # idx 11   surface sh-9
            (25,  sh-6,  10),   # idx 12  surface sh-7
            (42,  sh-10, 14),   # idx 13  surface sh-11
            (62,  sh-7,   9),   # idx 14  surface sh-8
            (78,  sh-9,  12),   # idx 15  surface sh-10
            (95,  sh-6,  15),   # idx 16  surface sh-7
            (115, sh-8,  10),   # idx 17  surface sh-9
        ]
        platforms = ground + elevated
        bricks = [ 
            [9,  sh-9],[10, sh-9],
            [44, sh-11],[45,sh-11],
            [80, sh-10],
        ]
        enemies = [  # 🤖 sur les plateformes de passage
            [10, sh-9,   1,  9],
            [27, sh-7,  -1, 10],
            [44, sh-11,  1, 11],
            [64, sh-8,  -1, 12],
            [80, sh-10,  1, 13],
            [97, sh-7,  -1, 14],
            [117,sh-9,   1, 15],
        ]
        # 3 💫 dans la grotte (facile sol, difficile plafond, moyen passage)
        stars   = [[20, sol_y-1],[60, 3],[105, sh-7]]
        key_pos = None
        boss    = None
        fire_pits = []  # pas de lave dans la grotte

    elif level_num == 6:  # LABYRINTHE D'IROSHI — Forêt dense Ninjago
        # Dédale de jungle dense et mortelle sur l'île de Ninjago.
        # Nommé en l'honneur d'Hiroshi, premier explorateur à s'en échapper.
        # Centre : l'Oasis du Joyau. Gardé par des Nindroids et des créatures.
        sol_y = sh - 2;  enemy_char = "🤖"
        enemy_speed = 1;  enemy_move_step = 0.42
        # ── LARGEUR ÉTENDUE : remplit toute la fenêtre + scroll ───────
        level_width = max(sw * 4, 300)  # niveau très long
        ground = [(0, sol_y, level_width)]

        # ─ PLATEFORMES : 5 strates verticales pour remplir tout l'écran
        # sh ~ 40-50 lignes → strates à sh-7, sh-13, sh-19, sh-25, sh-31, sh-37
        elevated = [
            # ══ Strate 1 : souches/racines (sh-7) ══
            (3,   sh-7,   9),   # idx 1
            (16,  sh-7,  10),   # idx 2
            (29,  sh-7,   9),   # idx 3
            (43,  sh-7,  11),   # idx 4
            (58,  sh-7,   9),   # idx 5
            (72,  sh-7,  10),   # idx 6
            (86,  sh-7,   9),   # idx 7
            (100, sh-7,  11),   # idx 8
            (115, sh-7,   9),   # idx 9
            (130, sh-7,  10),   # idx 10
            (145, sh-7,   9),   # idx 11
            (160, sh-7,  11),   # idx 12
            (175, sh-7,   9),   # idx 13
            (190, sh-7,  10),   # idx 14
            (205, sh-7,   9),   # idx 15
            (220, sh-7,  11),   # idx 16
            (235, sh-7,   9),   # idx 17
            (250, sh-7,  10),   # idx 18
            (265, sh-7,   9),   # idx 19
            (280, sh-7,  11),   # idx 20
            # ══ Strate 2 : branches basses (sh-13) ══
            (6,   sh-13,  9),   # idx 21
            (21,  sh-13, 10),   # idx 22
            (36,  sh-13,  9),   # idx 23
            (51,  sh-13, 10),   # idx 24
            (66,  sh-13,  9),   # idx 25
            (80,  sh-13, 10),   # idx 26
            (95,  sh-13,  9),   # idx 27
            (110, sh-13, 10),   # idx 28
            (125, sh-13,  9),   # idx 29
            (140, sh-13, 10),   # idx 30
            (155, sh-13,  9),   # idx 31
            (170, sh-13, 10),   # idx 32
            (185, sh-13,  9),   # idx 33
            (200, sh-13, 10),   # idx 34
            (215, sh-13,  9),   # idx 35
            (230, sh-13, 10),   # idx 36
            (245, sh-13,  9),   # idx 37
            (260, sh-13, 10),   # idx 38
            (275, sh-13,  9),   # idx 39
            (290, sh-13, 10),   # idx 40
            # ══ Strate 3 : branches hautes (sh-19) ══
            (9,   sh-19,  9),   # idx 41
            (24,  sh-19, 10),   # idx 42
            (39,  sh-19,  9),   # idx 43
            (54,  sh-19, 10),   # idx 44
            (69,  sh-19,  9),   # idx 45
            (84,  sh-19, 10),   # idx 46
            (99,  sh-19,  9),   # idx 47
            (114, sh-19, 10),   # idx 48
            (129, sh-19,  9),   # idx 49
            (144, sh-19, 10),   # idx 50
            (159, sh-19,  9),   # idx 51
            (174, sh-19, 10),   # idx 52
            (189, sh-19,  9),   # idx 53
            (204, sh-19, 10),   # idx 54
            (219, sh-19,  9),   # idx 55
            (234, sh-19, 10),   # idx 56
            (249, sh-19,  9),   # idx 57
            (264, sh-19, 10),   # idx 58
            (279, sh-19,  9),   # idx 59
            (294, sh-19, 10),   # idx 60
            # ══ Strate 4 : mi-canopée (sh-25) ══
            (12,  sh-25,  9),   # idx 61
            (27,  sh-25, 10),   # idx 62
            (42,  sh-25,  9),   # idx 63
            (57,  sh-25, 10),   # idx 64
            (72,  sh-25,  9),   # idx 65
            (87,  sh-25, 10),   # idx 66
            (102, sh-25,  9),   # idx 67
            (117, sh-25, 10),   # idx 68
            (132, sh-25,  9),   # idx 69
            (147, sh-25, 10),   # idx 70
            (162, sh-25,  9),   # idx 71
            (177, sh-25, 10),   # idx 72
            (192, sh-25,  9),   # idx 73
            (207, sh-25, 10),   # idx 74
            (222, sh-25,  9),   # idx 75
            (237, sh-25, 10),   # idx 76
            (252, sh-25,  9),   # idx 77
            (267, sh-25, 10),   # idx 78
            (282, sh-25,  9),   # idx 79
            # ══ Strate 5 : canopée haute (sh-31) ══
            (15,  sh-31,  9),   # idx 80
            (32,  sh-31, 10),   # idx 81
            (49,  sh-31,  9),   # idx 82
            (66,  sh-31, 10),   # idx 83
            (83,  sh-31,  9),   # idx 84
            (100, sh-31, 10),   # idx 85
            (117, sh-31,  9),   # idx 86
            (134, sh-31, 10),   # idx 87
            (151, sh-31,  9),   # idx 88
            (168, sh-31, 10),   # idx 89
            (185, sh-31,  9),   # idx 90
            (202, sh-31, 10),   # idx 91
            (219, sh-31,  9),   # idx 92
            (236, sh-31, 10),   # idx 93
            (253, sh-31,  9),   # idx 94
            (270, sh-31, 10),   # idx 95
            # ══ Strate 6 : cimes (sh-37) — oasis de Joyau ══
            (18,  sh-37,  9),   # idx 96
            (37,  sh-37, 10),   # idx 97
            (56,  sh-37,  9),   # idx 98
            (75,  sh-37, 10),   # idx 99
            (94,  sh-37,  9),   # idx 100
            (113, sh-37, 10),   # idx 101  ← OASIS DU JOYAU (centre)
            (132, sh-37,  9),   # idx 102
            (151, sh-37, 10),   # idx 103
            (170, sh-37,  9),   # idx 104
            (189, sh-37, 10),   # idx 105
            (208, sh-37,  9),   # idx 106
            (227, sh-37, 10),   # idx 107
            (246, sh-37,  9),   # idx 108
            (265, sh-37, 10),   # idx 109
            (284, sh-37,  8),   # idx 110
        ]
        platforms = ground + elevated

        # ─ TRONCS 🪵 CASSABLES — colonnes reliant chaque strate ───────
        forest_trunks = []
        # Générés automatiquement entre chaque strate, tous les ~15 cols
        trunk_xs = list(range(7, level_width - 5, 15))
        for tx in trunk_xs:
            # Tronc sol → strate1 (sh-7)
            forest_trunks.append((tx, sh-7, 6))
            # Tronc strate1 → strate2
            forest_trunks.append((tx+1, sh-13, 5))
            # Tronc strate2 → strate3
            forest_trunks.append((tx, sh-19, 5))
            # Tronc strate3 → strate4
            forest_trunks.append((tx+1, sh-25, 5))
            # Tronc strate4 → strate5
            forest_trunks.append((tx, sh-31, 5))
            # Tronc strate5 → strate6 (demi)
            forest_trunks.append((tx+1, sh-37, 5))

        # ── BRIQUES 🧱 — pièges et passages ───────────────────────────
        bricks = []
        # Une brique juste au-dessus de chaque plateforme strate1 (sh-7 → brique sh-8)
        for px, py, pw in elevated[:20]:   # strate1
            bricks.append([px+2, py-1])
            bricks.append([px+4, py-1])
        # Briques strate3 (artefacts cachés)
        for px, py, pw in elevated[40:60]:  # strate3
            bricks.append([px+1, py-1])
        # Rempart de Cyrus Borg (strate5) — blocs défensifs
        for px, py, pw in elevated[79:96]:  # strate5
            bricks.append([px+2, py-1])
            bricks.append([px+5, py-1])
            bricks.append([px+7, py-1])

        # ── ENNEMIS 🤖 Nindroids ──────────────────────────────────────
        enemies = []
        # Strate1 : patrouillent sur chaque plateforme (2/3 des plateformes)
        for i in range(0, 20, 1):
            px, py, pw = elevated[i]
            ey = py - 1
            enemies.append([px+2, ey, 1 if i%2==0 else -1, i+1])
            if i % 3 == 0:  # double patrouille sur 1/3
                enemies.append([px+pw-2, ey, -1, i+1])
        # Strate2
        for i in range(20, 40, 1):
            px, py, pw = elevated[i]
            ey = py - 1
            if i % 2 == 0:
                enemies.append([px+2, ey, 1, i+1])
        # Strate3
        for i in range(40, 60, 1):
            px, py, pw = elevated[i]
            ey = py - 1
            if i % 3 != 1:
                enemies.append([px+2, ey, -1 if i%2 else 1, i+1])
        # Strate4 : élite Nindroids + gardiens du rempart
        for i in range(60, 79, 1):
            px, py, pw = elevated[i]
            ey = py - 1
            enemies.append([px+3, ey, 1 if i%2==0 else -1, i+1])
        # Strate5 + 6 : gardiens des cimes et de l'Oasis
        for i in range(79, min(110, len(elevated))):
            px, py, pw = elevated[i]
            ey = py - 1
            if i % 2 == 0:
                enemies.append([px+2, ey, 1, i+1])

        # ── ÉTOILES 💫 — réparties verticalement ──────────────────────
        stars = [
            [10,  sol_y-1],           # sol — facile
            [30,  sh-8],              # strate1
            [55,  sh-14],             # strate2
            [80,  sh-20],             # strate3
            [105, sh-26],             # strate4
            [118, sh-32],             # strate5 — Oasis du Joyau
            [145, sh-38],             # strate6 — cimes
            [170, sh-26],             # strate4 cachée
            [220, sh-20],             # strate3 cachée
            [260, sh-32],             # strate5 — Crystal du Royaume
            [285, sh-38],             # perchoir final
        ]

        # ── CLÉ CACHÉE dans l'Oasis ───────────────────────────────────
        key_pos = [118, sh-38]  # joyau du labyrinthe

        boss      = None
        fire_pits = []

        # ── DÉCORATION + SENSEI GARMADON ──────────────────────────────
        jungle_decos = []
        # 🦜 Perroquets sur les cimes
        for x_d in range(20, level_width, 23):
            jungle_decos.append(('🦜', x_d, sh-38))
        # 🦋 Papillons strate4
        for x_d in range(15, level_width, 18):
            jungle_decos.append(('🦋', x_d, sh-26))
        # 🐍 Serpents au sol
        for x_d in range(8, level_width, 20):
            jungle_decos.append(('🐍', x_d, sol_y-1))
        # 🌺 Fleurs strate2
        for x_d in range(10, level_width, 14):
            jungle_decos.append(('🌺', x_d, sh-14))


    elif level_num == 7:  # ══ CITADELLE AÉRIENNE — Approche de Bowser ══
        sol_y = sh - 3;  enemy_char = "👻"
        enemy_speed = 1;  enemy_move_step = 0.45
        ground = [
            (0,  sol_y, 10), (14, sol_y, 12),
            (34, sol_y, 11), (52, sol_y, 14),
            (76, sol_y, 10), (94, sol_y, level_width - 94),
        ]
        elevated = [
            (7,   sh-8,  10),   # idx 6
            (24,  sh-12, 12),   # idx 7
            (45,  sh-9,   9),   # idx 8
            (61,  sh-14, 12),   # idx 9
            (82,  sh-10, 10),   # idx 10
            (101, sh-13, 14),   # idx 11
        ]
        platforms = ground + elevated
        bricks = [
            [8, sh-9],[9, sh-9],
            [26, sh-13],[27, sh-13],[28, sh-13],
            [47, sh-10],[48, sh-10],
            [63, sh-15],[64, sh-15],
            [103, sh-14],[104, sh-14],[105, sh-14],
        ]
        enemies = [
            [8,  sh-9,   1,  6],
            [26, sh-13, -1,  7],
            [47, sh-10,  1,  8],
            [63, sh-15, -1,  9],
            [84, sh-11,  1, 10],
            [104,sh-14, -1, 11],
        ]
        stars   = [[18,sol_y-1],[68,sh-15],[114,sh-14]]
        key_pos = None
        boss    = None
        fire_pits = []

    elif level_num == 8:
        sol_y = sh - 2;  enemy_char = "👾"
        enemy_speed = 1;  enemy_move_step = 0.35
        ground = [
            (0,  sol_y, 10),
            (12, sol_y, 10),
            (24, sol_y, 24),
            (52, sol_y,  6),
            (61, sol_y, 26),
            (91, sol_y, level_width - 91),
        ]
        fire_pits = [(10, 11),(22, 23),(58, 60)]
        elevated = [
            (12, sh-6,  14),   # idx 6 : abri gauche    — surface sh-7
            (50, sh-9,  16),   # idx 7 : plateforme haute — surface sh-10
            (88, sh-6,  20),   # idx 8 : trône Bowser   — surface sh-7
        ]
        platforms = ground + elevated
        bricks = [
            [13, sh-7],[14, sh-7],
            [51, sh-10],[52, sh-10],[53, sh-10],
            [89, sh-7],[90, sh-7],[91, sh-7],
        ]
        enemies = [
            [15, sh-7,   1, 6],   # 👾 patrouille abri gauche
            [53, sh-10, -1, 7],   # 👾 patrouille plateforme haute
        ]
        stars   = [[57, sh-10]]
        key_pos = None
        # boss : HP 5, tirs 2× ralentis (35 → 70)
        boss    = [100, sh-7, 5, -1, 0]

    elif level_num == 9:  # ══ FUITE DU CHÂTEAU — Dernière épreuve ══
        sol_y = sh - 2;  enemy_char = "🤖"
        enemy_speed = 1;  enemy_move_step = 0.40
        ground = [
            (0,  sol_y, 14), (18, sol_y, 12),
            (34, sol_y, 16), (56, sol_y, 12),
            (74, sol_y, 15), (96, sol_y, level_width - 96),
        ]
        elevated = [
            (10,  sh-7,  12),   # idx 6
            (28,  sh-11, 11),   # idx 7
            (49,  sh-8,  10),   # idx 8
            (67,  sh-12, 10),   # idx 9
            (88,  sh-7,  12),   # idx 10
            (108, sh-10, 12),   # idx 11
        ]
        platforms = ground + elevated
        bricks = [
            [12, sh-8],[13, sh-8],
            [30, sh-12],[31, sh-12],
            [51, sh-9],[52, sh-9],
            [69, sh-13],[70, sh-13],[71, sh-13],
            [110,sh-11],[111,sh-11],
        ]
        enemies = [
            [12, sh-8,   1,  6],
            [30, sh-12, -1,  7],
            [51, sh-9,   1,  8],
            [69, sh-13, -1,  9],
            [90, sh-8,   1, 10],
            [110,sh-11, -1, 11],
        ]
        stars   = [[39,sol_y-1],[118,sh-11]]
        key_pos = None
        boss    = None
        fire_pits = []

    # ══════════════════════════════════════════════════════════════════
    #  FLAG P/U
    # ══════════════════════════════════════════════════════════════════
    flag_x       = level_width - 5
    flag_base_y  = sol_y - 1
    flag_top_y   = sol_y - 2
    platforms.append((flag_x, flag_base_y + 1, 2))

    if level_num != 8:  # fire_pits uniquement niveau 8
        fire_pits = []

    if level_num != 6:  # troncs uniquement Labyrinthe d'Iroshi
        forest_trunks = []
        jungle_decos = []  # décoration visible uniquement niv 6
    # Convertir troncs en briques cassables individuelles [x, y]
    trunk_bricks = []
    for tx, ty, th in forest_trunks:
        for row in range(ty, ty + th):
            trunk_bricks.append([tx, row])

    # ══════════════════════════════════════════════════════════════════
    #  INIT COMMUN
    # ══════════════════════════════════════════════════════════════════
    coins = []
    for px, py, w in platforms[:-1]:
        if py - 1 >= 0:
            coins.append([px + w // 2, py - 1])
    coins.append([random.randint(2, level_width - 2), sol_y - 1])

    x = 5;  y = float(sol_y - 1)
    on_ground = True;  facing = 1
    projectiles = []
    boss_projs  = []
    boss_alive  = (boss is not None)

    # Intro
    stdscr.clear()
    if level_num == 8:
        msg  = "  NIVEAU 8 — BOSS FINAL : BOWSER !  " 
        hint = "  Vainc Bowser !  Appuie sur une touche..."
    elif level_num == 7:
        msg  = "  NIVEAU 7 — LA CITADELLE AÉRIENNE ☁️  "
        hint = "  Escalade l'avant-poste de Bowser !  Appuie sur une touche..."
    elif level_num == 9:
        msg  = "  NIVEAU 9 — LA FUITE DU CHÂTEAU 🏰  "
        hint = "  Sors vivant du château après Bowser !  Appuie sur une touche..."
    elif level_num == 6:
        msg  = "  NIVEAU 6 — Lloyd au LABYRINTHE D'IROSHI "
        hint = "  Monte jusqu'à la canopée, puis redescends si besoin avec ⬇️ !  Appuie sur une touche..."
    elif level_num == 5:
        msg  = "  NIVEAU 5 — LES SOUTERRAINS !  "
        hint = "  Luigi vs les Nindroids de Bowser !  Appuie sur une touche..."
    else:
        msg  = f"  NIVEAU {level_num}  "
        hint = "  Appuie sur une touche..."
    try:
        stdscr.addstr(sh//2,   max(0, sw//2-len(msg)//2),  msg)
        stdscr.addstr(sh//2+1, max(0, sw//2-len(hint)//2), hint)
    except curses.error: pass
    stdscr.refresh()
    stdscr.nodelay(False);  stdscr.getch();  stdscr.nodelay(True)
    for _ in range(3): curses.beep();  time.sleep(0.05)

    frame = 0;  enemy_acc = 0.0

    # ☁️ Nuages aléatoires : (col, row) fixes pour toute la durée du niveau
    # Lignes 1-3 (sous le HUD), colonnes réparties sur tout le niveau
    nb_clouds = random.randint(5, 15)
    clouds = [(random.randint(0, level_width - 2), random.randint(1, 3))
              for _ in range(nb_clouds)]



# ══════════════════════════════════════════════════════════════════════
#  BOUCLE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════
    while True:
        stdscr.erase()   # erase ≠ clear : pas de curseur reset, diff minimal au refresh
        cur_sh, cur_sw = stdscr.getmaxyx()
        if (cur_sh, cur_sw) != (sh, sw):
            return 'resize', score, stars_collected, key_collected, cheated
        key = stdscr.getch()

        if key == ord('q'):
            return 'quit', score, stars_collected, key_collected, cheated

        # 🔐 DEV : Ctrl+D → menu de sélection de niveau ───────────────
        if key == 4:   # Ctrl+D = ASCII 4
            cheated = True
            # Construire la liste des niveaux disponibles
            all_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            level_names = {
                1:"1", 2:"2", 3:"3", 4:"4", 5:"5",
                6:"6", 7:"7", 8:"8 (BOWSER)", 9:"9"
            }
            sel = 0
            stdscr.nodelay(False)
            while True:
                stdscr.erase()
                try: stdscr.addstr(sh//2-4, max(0,sw//2-14), "  ── SÉLECTION DE NIVEAU ──  ")
                except curses.error: pass
                for i, lv in enumerate(all_levels):
                    marker = "► " if i == sel else "  "
                    try: stdscr.addstr(sh//2-2+i, max(0,sw//2-10),
                                       f"{marker}Niveau {level_names[lv]}")
                    except curses.error: pass
                try: stdscr.addstr(sh//2+8, max(0,sw//2-14), "  ↑↓=naviguer  Entrée=lancer  Q=annuler  ")
                except curses.error: pass
                stdscr.refresh()
                nk = stdscr.getch()
                if nk == curses.KEY_UP:   sel = (sel - 1) % len(all_levels)
                elif nk == curses.KEY_DOWN: sel = (sel + 1) % len(all_levels)
                elif nk in (ord('\n'), ord('\r'), curses.KEY_ENTER, 10, 13):
                    stdscr.nodelay(True)
                    return 'dev_jump', all_levels[sel], stars_collected, key_collected, cheated
                elif nk == ord('q'): break
            stdscr.nodelay(True)

        # ── Déplacement ───────────────────────────────────────────────
        is_moving = False
        if key == curses.KEY_LEFT:
            x = max(0, x - 1);  facing = -1;  is_moving = True
        elif key == curses.KEY_RIGHT:
            x = min(level_width - 1, x + 1);  facing = 1;  is_moving = True

        # ──Saut ───────────────────────────────────────────────────────
        if (key == ord(' ') or key == curses.KEY_UP) and on_ground:
            velocity_y = jump_power;  velocity_x = facing * 5
            on_ground = False;  curses.beep()
        if not on_ground and velocity_x != 0:
            x = max(0, min(level_width - 1, x + velocity_x));  velocity_x = 0

        # ── Tir : [N] ou [-]  ─────────────────────────────────────────
        if key == ord('n') or key == ord('-'):
             projectiles.append([x + facing, int(y), facing])

        # ── ⬇️ Descente de plateforme (niv 6+) ───────────────────────
        if level_num == 6 and key == curses.KEY_DOWN and on_ground:
            # Trouver la plateforme du dessous la plus proche
            best_drop = None
            for px, py, w in platforms:
                if px <= x < px + w and py > int(y) + 1:
                    if best_drop is None or py < best_drop:
                        best_drop = py
            if best_drop is not None:
                y = float(best_drop - 1);  velocity_y = 0;  on_ground = True
            else:
                # Pas de plateforme en dessous → tombe au sol
                y = float(sol_y - 1);  velocity_y = 0;  on_ground = True

# ── Gravité ───────────────────────────────────────────────────────────
        velocity_y = min(velocity_y + gravity, 4.0)
        new_y = y + velocity_y;  on_ground = False

        # ── Collision plateformes ─────────────────────────────────────
        for px, py, w in platforms:
            if px <= x < px + w:
                # Sol : tombe dessus par le haut
                if y <= py - 1 and new_y >= py - 1:
                    new_y = py - 1;  velocity_y = 0;  on_ground = True
                # Plafond niv5 : saute dedans par le bas (py est petit → plafond)
                elif level_num == 5 and py <= sh // 2 and y >= py and new_y < py:
                    new_y = float(py);  velocity_y = 0
        y = new_y

        # ── Chute ─────────────────────────────────────────────────────
        if int(y) >= sh:
            try: stdscr.addstr(sh//2, max(0,sw//2-5), "GAME OVER", C('gameover'))
            except curses.error: pass
            stdscr.refresh();  time.sleep(2)
            return 'dead', score, stars_collected, key_collected, cheated

        # ── ♨️ Fosses de lave (niveau 8) ─────────────────────────────
        for fx1, fx2 in fire_pits:
            if fx1 <= int(x) <= fx2 and int(y) >= sol_y - 1:
                try: stdscr.addstr(sh//2, max(0,sw//2-8), "BRÛLÉ PAR LA LAVE ♨️", C('gameover'))
                except curses.error: pass
                stdscr.refresh();  time.sleep(2)
                return 'dead', score, stars_collected, key_collected, cheated

        # ── Pièces ───────────────────────────────────────────────────
        for coin in coins[:]:
            if int(x) == coin[0] and int(y) == coin[1]:
                coins.remove(coin);  score += 1;  curses.beep()

        # ── 🗝️ Clé ───────────────────────────────────────────────────
        if key_pos and not key_collected:
            if abs(int(x) - key_pos[0]) <= 1 and int(y) == key_pos[1]:
                key_collected = True;  score += 10
                for _ in range(4): curses.beep();  time.sleep(0.03)

        # ── 💫 Étoiles filantes(+10 pts) ─────────────────────────────
        for star in stars[:]:
            if abs(int(x) - star[0]) <= 1 and int(y) == star[1]:
                stars.remove(star);  stars_collected += 1;  score += 10
                for _ in range(3): curses.beep();  time.sleep(0.02)

        # ── Briques ───────────────────────────────────────────────────
        for brick in bricks[:]:
            bx, by = brick
            if int(x) == bx and int(y) == by + 1:
                bricks.remove(brick);  score += 1
                for _ in range(2): curses.beep();  time.sleep(0.03)

        # ── 🪵 Troncs cassables (niveau 6) — saut par le bas ou tir ──
        if level_num == 6:
            for tb in trunk_bricks[:]:
                tbx, tby = tb
                if int(x) == tbx and int(y) == tby + 1 and velocity_y < 0:
                    trunk_bricks.remove(tb);  score += 1;  curses.beep()
                    for i, (px, py, pw) in enumerate(platforms):
                        if px <= tbx < px + pw and py == tby:
                            platforms[i] = (px, py + 1, pw)
                            for en in enemies:
                                if en[3] == i: en[1] += 1
            for proj in projectiles[:]:
                for tb in trunk_bricks[:]:
                    if abs(int(proj[0]) - tb[0]) <= 1 and proj[1] == tb[1]:
                        trunk_bricks.remove(tb);  score += 1;  curses.beep()
                        if proj in projectiles: projectiles.remove(proj)
                        for i, (px, py, pw) in enumerate(platforms):
                            if px <= tb[0] < px + pw and py == tb[1]:
                                platforms[i] = (px, py + 1, pw)
                                for en in enemies:
                                    if en[3] == i: en[1] += 1
                        break

        frame += 1

        # ── Projectiles joueur ────────────────────────────────────────
        for proj in projectiles[:]:
            proj[0] += proj[2] * 2
            if proj[0] < 0 or proj[0] >= level_width:
                projectiles.remove(proj);  continue
            hit = False
            for enemy in enemies[:]:
                if abs(int(proj[0]) - enemy[0]) <= 1 and proj[1] == enemy[1]:
                    enemies.remove(enemy);  projectiles.remove(proj)
                    score += 2;  curses.beep();  hit = True;  break
            if not hit and level_num == 8 and boss_alive:
                if abs(int(proj[0]) - boss[0]) <= 2 and abs(proj[1] - boss[1]) <= 1:
                    boss[2] -= 1;  projectiles.remove(proj);  score += 5
                    curses.beep();  hit = True
                    if boss[2] <= 0: boss_alive = False;  boss_projs.clear();  score += 20;  curses.beep()
            if not hit:
                for brick in bricks[:]:
                    if abs(int(proj[0]) - brick[0]) <= 1 and proj[1] == brick[1]:
                        bricks.remove(brick);  projectiles.remove(proj)
                        score += 1;  hit = True;  break

        # ── Ennemis normaux ───────────────────────────────────────────
        enemy_acc += enemy_move_step
        if enemy_acc >= 1.0:
            enemy_acc -= 1.0
            for enemy in enemies:
                ex, ey, direction, pf_idx = enemy
                pf_x, pf_y, pf_w = platforms[pf_idx]
                ex += direction
                if ex <= pf_x or ex >= pf_x + pf_w:
                    direction *= -1;  ex += direction
                enemy[0] = ex;  enemy[2] = direction

        for enemy in enemies[:]:
            ex, ey = enemy[0], enemy[1]
            if abs(int(x) - ex) <= 1 and 0 <= ey < sh:
                if int(y) == ey - 1 and velocity_y > 0:
                    enemies.remove(enemy);  score += 3
                    velocity_y = -3.0;  curses.beep()
                elif int(y) == ey:
                    try: stdscr.addstr(sh//2, max(0,sw//2-5), "GAME OVER", C('gameover'))
                    except curses.error: pass
                    stdscr.refresh();  time.sleep(2)
                    return 'dead', score, stars_collected, key_collected, cheated

        # ── Boss Bowser (niveau 6) ────────────────────────────────────
        if level_num == 8 and boss_alive:
            if frame % 3 == 0:
                boss[0] += boss[3]
                if boss[0] <= 89 or boss[0] >= 106: boss[3] *= -1
            boss[4] += 1
            if boss[4] >= 70:  # tirs ralentis 2× (35 → 70)
                boss[4] = 0
                bdir = -1 if x < boss[0] else 1
                boss_projs.append([boss[0] + bdir * 2, boss[1], bdir])
                boss_projs.append([boss[0] + bdir * 3, boss[1] - 1, bdir])
            for bp in boss_projs[:]:
                bp[0] += bp[2]
                if bp[0] < 0 or bp[0] >= level_width:
                    boss_projs.remove(bp);  continue
                if abs(int(x) - bp[0]) <= 1 and abs(int(y) - bp[1]) <= 1:
                    boss_projs.remove(bp)
                    try: stdscr.addstr(sh//2, max(0,sw//2-5), "GAME OVER", C('gameover'))
                    except curses.error: pass
                    stdscr.refresh();  time.sleep(2)
                    return 'dead', score, stars_collected, key_collected, cheated
            if abs(int(x) - boss[0]) <= 2 and int(y) == boss[1]-1 and velocity_y > 0:
                boss[2] -= 1;  velocity_y = -3.0;  score += 5;  curses.beep()
                if boss[2] <= 0: boss_alive = False;  boss_projs.clear();  score += 20;  curses.beep()
            elif abs(int(x) - boss[0]) <= 1 and int(y) == boss[1]:
                try: stdscr.addstr(sh//2, max(0,sw//2-5), "GAME OVER", C('gameover'))
                except curses.error: pass
                stdscr.refresh();  time.sleep(2)
                return 'dead', score, stars_collected, key_collected, cheated

        # ── Drapeau P/U : niveau 6 = mort de Bowser OBLIGATOIRE  ──────
        flag_clear = (level_num == 8 and not boss_alive) or \
                     (level_num not in (8,) and level_num >= 1 and len(enemies) == 0)
        if flag_clear and abs(int(x) - flag_x) <= 1 and int(y) == flag_top_y:
            return 'win', score, stars_collected, key_collected, cheated



# ══════════════════════════════════════════════════════════════════════
#  DESSIN
# ══════════════════════════════════════════════════════════════════════
        offset = max(0, min(x - sw // 4, max(0, level_width - sw)))

        # 🌞 / 🌲 Fond selon le niveau
        if level_num == 6:
            try: stdscr.addstr(3, 3, "🌞")
            except curses.error: pass
            try: stdscr.addstr(3, sw - 6, "🌞")
            except curses.error: pass
        else:
            try: stdscr.addstr(3, 3, "🌞")
            except curses.error: pass

        # ☁️ Nuages (se déplacent avec le scrolling)
        for cx, cy in clouds:
            dx = cx - offset
            if 0 <= dx < sw - 1 and 1 <= cy < sh:
                if level_num == 6:
                    try: stdscr.addstr(cy, dx, "🍃")
                    except curses.error: pass
                else:
                    try: stdscr.addstr(cy, dx, "☁️")
                    except curses.error: pass

        # 🪵 Troncs cassables du Labyrinthe d'Iroshi (niveau 55)
        if level_num == 6:
            for tbx, tby in trunk_bricks:
                dx = tbx - offset
                if 0 <= dx < sw and 0 <= tby < sh:
                    try: stdscr.addstr(tby, dx, "🪵", C('floor'))
                    except curses.error: pass

        # Plateformes
        for px, py, w in platforms[:-1]:
            draw_x = px - offset
            if draw_x + w < 0 or draw_x >= sw or py < 0 or py >= sh: continue
            start = max(0, draw_x);  clip_left = max(0, -draw_x)
            end = min(w - clip_left, sw - start)
            if end <= 0: continue
            col = (C('sol_cyan') if level_num in (3,4) else C('floor')) \
                  if py == sol_y else C('platform')
            plat_char = "#" if level_num == 6 and py != sol_y else "="
            try: stdscr.addstr(py, start, plat_char * end, col)
            except curses.error: pass

        # ♨️ Fosses de lave (niveau 6)
        for fx1, fx2 in fire_pits:
            for fx in range(fx1, fx2 + 1):
                dx = fx - offset
                if 0 <= dx < sw and 0 <= sol_y < sh:
                    try: stdscr.addstr(sol_y, dx, "♨️")
                    except curses.error: pass

        # Pièces
        for coin in coins:
            dx = coin[0] - offset
            if 0 <= dx < sw and 0 <= coin[1] < sh:
                try: stdscr.addstr(coin[1], dx, "🪙", C('coin'))
                except curses.error: pass

        # 🗝️ Clé
        if key_pos and not key_collected:
            dx = key_pos[0] - offset
            if 0 <= dx < sw and 0 <= key_pos[1] < sh:
                try: stdscr.addstr(key_pos[1], dx, "🗝️")
                except curses.error: pass

        # 💫 Étoiles
        for star in stars:
            dx = star[0] - offset
            if 0 <= dx < sw and 0 <= star[1] < sh:
                try: stdscr.addstr(star[1], dx, "💫")
                except curses.error: pass

        # 🦜🦋🐍🌺⚔️💎 Décorations jungle (niveau 6 — Labyrinthe d'Iroshi)
        if level_num == 6:
            for dchar, dx_w, dy in jungle_decos:
                dx = dx_w - offset
                if 0 <= dx < sw - 1 and 0 <= dy < sh:
                    try: stdscr.addstr(dy, dx, dchar)
                    except curses.error: pass

        # Briques
        for bx, by in bricks:
            dx = bx - offset
            if 0 <= dx < sw and 0 <= by < sh:
                try: stdscr.addstr(by, dx, "🧱")
                except curses.error: pass

        # Projectiles joueur
        for proj in projectiles:
            dx = proj[0] - offset
            if 0 <= dx < sw and 0 <= proj[1] < sh:
                try: stdscr.addstr(proj[1], dx, "🟔", C('bullet'))
                except curses.error: pass

        # Ennemis
        for ex, ey, _, _ in enemies:
            dx = ex - offset
            if 0 <= dx < sw and 0 <= ey < sh:
                try: stdscr.addstr(ey, dx, enemy_char, C('enemy'))
                except curses.error: pass

        # Bowser (niveau 8)
        if level_num == 8:
            if boss_alive:
                bx_d = boss[0] - offset
                if 0 <= bx_d < sw and 0 <= boss[1] < sh:
                    hp_bar = "♥" * boss[2] + "♡" * (5 - boss[2])
                    try:
                        stdscr.addstr(boss[1], bx_d, "B", C('enemy'))
                        if boss[1]-1 >= 0:
                            stdscr.addstr(boss[1]-1, max(0, bx_d-1), hp_bar, C('enemy'))
                    except curses.error: pass
            for bp in boss_projs if boss_alive else []:
                dx = bp[0] - offset
                if 0 <= dx < sw and 0 <= bp[1] < sh:
                    try: stdscr.addstr(bp[1], dx, "🔥", C('enemy') | curses.A_BOLD)
                    except curses.error: pass

        # Drapeau P/U
        dx_flag = flag_x - offset
        if 0 <= dx_flag < sw:
            col_flag = C('luigi') if flag_clear else C('enemy')
            p_char   = "P" if flag_clear else "X"
            u_char   = "U" if flag_clear else "="
            try:
                if 0 <= flag_top_y < sh:
                    stdscr.addstr(flag_top_y, dx_flag, p_char, col_flag)
                if 0 <= flag_base_y < sh:
                    stdscr.addstr(flag_base_y, dx_flag, u_char, col_flag)
            except curses.error: pass

        # Joueur : 🌪️ si mouvement ou en l'air, M/L si immobile au sol
        draw_px = x - offset
        if 0 <= draw_px < sw and 0 <= int(y) < sh:
            p_color = C('mario') if player_char == "M" else C('luigi')
            if not on_ground or is_moving:
                sprite = "🌪️"
            else:
                sprite = player_char
            try: stdscr.addstr(int(y), draw_px, sprite, p_color)
            except curses.error: pass

        # HUD
        try:
            if level_num == 8:
                hp_now = boss[2] if boss_alive else 0
                extra = f"  BOWSER: {'♥'*hp_now}{'♡'*(5-hp_now)}" \
                        if boss_alive else "  BOWSER: vaincu! ★ OBLIGATOIRE ✓"
            else:
                extra = f"  Ennemis:{len(enemies)}" if enemies else "  Ennemis:0 ✓"
            key_hud = " 🗝️✓" if key_collected else " 🗝️?"
            stdscr.addstr(0, 2,
                f"Score:{score}  Niv:{level_num}{extra}"  #🛑🟥🟥 ajouter ici l'alias d'affichage du nouveau niveau (ex: if level_num != XX else 'X.X')
                f"  💫{stars_collected}/{TOTAL_STARS}{key_hud}"
                + ("  [⬇️ ]=descendre  " if level_num == 6 else "")
                + f"  [N][-]=pouvoir élémentaire  [SPC][⬆]=saut [Q]=quitter",
C('hud'))
        except curses.error: pass

        stdscr.refresh()
        frame += 1
        time.sleep(0.025)  # ~40fps


# ──────────────────────────────────────────────────────────────────────
def transition(stdscr, sh, sw, lines):
    stdscr.clear()
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(sh//2 - len(lines)//2 + i,
                          max(0, sw//2 - len(line)//2), line)
        except curses.error: pass
    stdscr.refresh()
    stdscr.nodelay(False);  stdscr.getch();  stdscr.nodelay(True)


def ensure_terminal_size(stdscr):
    sh, sw = stdscr.getmaxyx()
    if sh < MIN_TERM_HEIGHT or sw < MIN_TERM_WIDTH:
        stdscr.clear()
        try:
            stdscr.addstr(
                0, 0,
                f"Terminal trop petit ! {sw}x{sh} "
                f"(min {MIN_TERM_WIDTH}x{MIN_TERM_HEIGHT})"
            )
        except curses.error:
            pass
        stdscr.refresh()
        time.sleep(3)
        return None
    return sh, sw


def main(stdscr):
    curses.curs_set(0);  stdscr.keypad(True);  stdscr.nodelay(True)
    stdscr.idlok(True);  stdscr.idcok(True)  # optimise le diff écran
    curses.start_color();  curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW,  -1)
    curses.init_pair(2, curses.COLOR_RED,     -1)
    curses.init_pair(3, curses.COLOR_CYAN,    -1)
    curses.init_pair(4, curses.COLOR_GREEN,   -1)
    curses.init_pair(5, curses.COLOR_GREEN,   -1)
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)
    curses.init_pair(7, curses.COLOR_RED,     -1)
    curses.init_pair(8, curses.COLOR_CYAN,    -1)

    C_MARIO    = curses.color_pair(2) | curses.A_BOLD
    C_LUIGI    = curses.color_pair(4) | curses.A_BOLD
    C_ENEMY    = curses.color_pair(2) | curses.A_BOLD
    C_BULLET   = curses.color_pair(3)
    C_FLAG     = curses.color_pair(4) | curses.A_BOLD
    C_FLOOR    = curses.color_pair(5) | curses.A_BOLD
    C_PLATFORM = curses.color_pair(7) | curses.A_BOLD
    C_SOL_CYAN = curses.color_pair(8) | curses.A_BOLD
    C_COIN     = curses.color_pair(1)
    C_HUD      = curses.color_pair(6) | curses.A_BOLD
    C_GAMEOVER = curses.color_pair(2) | curses.A_BOLD

    dims = ensure_terminal_size(stdscr)
    if dims is None:
        return
    sh, sw = dims

    colors = {
        'mario': C_MARIO, 'luigi': C_LUIGI, 'enemy': C_ENEMY,
        'bullet': C_BULLET, 'flag': C_FLAG, 'floor': C_FLOOR,
        'platform': C_PLATFORM, 'sol_cyan': C_SOL_CYAN,
        'coin': C_COIN, 'hud': C_HUD, 'gameover': C_GAMEOVER,
    }

    score = 0;  stars_collected = 0;  key_collected = False;  cheated = False

    seq = [
        (1,  "M", "  NIVEAU 2 — Luigi !  (👻, trous larges, vitesse ↑)"),
        (2,  "L", "  NIVEAU 3 — Mario sur sol surélevé !  (👾, 🗝️ cachée)"),
        (3,  "M", "  NIVEAU 4 — Luigi face au chaos !  (👻 rapides, 💫 cachées)"),
        (4,  "L", "  NIVEAU 5 — SOUTERRAIN : Luigi vs les robots de Bowser !"),
        (5,  "L", "  NIVEAU 6 — LE LABYRINTHE D'IROSHI 🌳 Forêt danse Ninjago !"),
        (6,  "L", "  NIVEAU 7 — LA CITADELLE AÉRIENNE ☁️ !"),
        (7,  "M", "  NIVEAU 8 — VAINC LE BOSS BOWSER !  "),
        (8,  "M", "  NIVEAU 9 — LA FUITE DU CHÂTEAU 🏰 !"),
        (9,  "L", None),
    ]

    all_levels_seq = {lv: (pc, nh) for lv, pc, nh in seq}
    seq_order = [lv for lv, _, _ in seq]
    cur_idx = 0

    while cur_idx < len(seq_order):
        lnum = seq_order[cur_idx]
        pchar, next_hint = all_levels_seq[lnum]
        while True:
            sb = score;  sc = stars_collected;  kc = key_collected
            result, val, stars_collected, key_collected, cheated = run_level(
                stdscr, lnum, sb, sh, sw,
                player_char=pchar, colors=colors,
                stars_collected=sc, key_collected=kc, cheated=cheated)
            if result == 'quit': return
            if result == 'resize':
                dims = ensure_terminal_size(stdscr)
                if dims is None:
                    return
                sh, sw = dims
                continue
            if result == 'dev_jump':
                # val contient le numéro de niveau cible
                score = sb
                if val in seq_order:
                    cur_idx = seq_order.index(val)
                break
            score = val
            if result == 'win':  break
            score = sb;  stars_collected = sc;  key_collected = kc

        if result == 'win' and next_hint:
            cheat_warn = "  ⚠️  GLITCH DÉTECTÉ !" if cheated else ""
            transition(stdscr, sh, sw, [
                f"  ★  NIVEAU {lnum} TERMINÉ !  ★  " + cheat_warn,
                f"  Score : {score}   💫 {stars_collected}/{TOTAL_STARS}"
                + ("  🗝️✓" if key_collected else "  🗝️ pas encore !"), "",
                next_hint, "",
                "  Appuie sur une touche pour continuer",
            ])
        if result == 'win':
            cur_idx += 1
        elif result == 'dev_jump':
            pass  # cur_idx already set above

    # Écran de fin
    stdscr.clear()
    parfait = stars_collected == TOTAL_STARS
    if cheated:
        lines = [
            "  ⚠️  DEV GLITCH UTILISÉ ! ⚠️  ",
            "  Bien joué... mais c'est triché !  ",
            "  DISQUALIFIÉ — Dev mode only  ",
            f"  Score : {score}   💫 {stars_collected}/{TOTAL_STARS}",
        ]
    elif key_collected:
        lines = [
            "  🏆  FÉLICITATIONS !  🏆  ",
            f"  Tu as sauvé la princesse Apple 👸🏼 !  ",
            f"  Score final : {score}  ",
            f"  💫 {stars_collected}/{TOTAL_STARS}" + ("  🌟 PARFAIT !" if parfait else ""),
        ]
        print('Gagné')
    else:
        lines = [
            "  ❌  DISQUALIFIÉ !  ❌  ",
            "  Tu n'as pas récupéré la 🗝️ !  ",
            "  La princesse Apple reste prisonnière...  ",
            "  _____________  ",
            "  ||||||||👸🏼|||||||  ",
            f"  Score : {score}   💫 {stars_collected}/{TOTAL_STARS}",
        ]
        print('Perdu')
    for i, line in enumerate(lines):
        try: stdscr.addstr(sh//2 - 2 + i, max(0, sw//2 - len(line)//2), line)
        except curses.error: pass
    stdscr.addstr(sh - 2, max(0, sw//2 - 16), "  Appuie sur une touche...  ", 0)
    stdscr.refresh()
    stdscr.nodelay(False);  stdscr.getch();  stdscr.nodelay(True)

    # Écran de crédits
    stdscr.clear()
    credits = [
        "  Thank you for playing !  ",
        "",
        "  The game was inspired by :",
        "  Aywen, Xenoks (YouTubers), Super Mario🅫,",
        "  Vivaldia (Vivaldi Browser offline Game),",
        "  Ninjago ®️, Minecraft🅪",
        "",
        "  ─────────────────────────────────  ",
        "",

        "  Created by :",
        "",
        "  LEGOTechBuilder (Brick-linux-desiner)",
        "  Conception, Chief of Project, bug fixing & tuning",
        "",
        "  Claude Sonnet 4.6 (expended)",
        "  Realisation",
        "",
        "  ChatGPT 4mini",
        "  No working base of the first level",
        "",
        "  Codex (GPT5)",
        "  Extra levels, bug fixes",
        "",
        "  OréoPMA/SQL",
        "  For obsolet version velocity adjustments",
        "",
        "  ─────────────────────────────────  ",
        "",
        "Super Mario🅪 characters & concepts are using under licence of Nintendo",
        "©2026 Nintendo",
        "Ninjago® spinjitzu & spinjitzu is using under licence of LEGO🅬",
        "©2026 LEGO",
        "Vivaldia concepts from vivaldi browser are using under licence of vivaldi-technologies",
        "©2026 Vivaldi Technologies ",
        "",
        "  🌪️  Thank's for spinning !  🌪️  "
    ]
    for i, line in enumerate(credits):
        try:
            stdscr.addstr(max(0, sh//2 - len(credits)//2 + i),
                          max(0, sw//2 - len(line)//2), line)
        except curses.error: pass
    stdscr.refresh();  time.sleep(15)


curses.wrapper(main)
