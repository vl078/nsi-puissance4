import tkinter as tk
from tkinter import messagebox, font
import random
import math
import time

# Constantes globales
ROWS = 6
COLS = 7
CELL_SIZE = 90
JETON_BORDER = 6
COULEURS = {'red': '#e74c3c', 'yellow': '#f1c40f'}

# Classe pour les confettis (effet visuel)
def creer_confetti(canvas, x, y, color):
    confetti = {
        'canvas': canvas,
        'x': x,
        'y': y,
        'color': color,
        'size': random.randint(8, 16),
        'dy': random.uniform(2, 5),
        'dx': random.uniform(-2, 2),
        'angle': random.uniform(0, 2*math.pi),
        'spin': random.uniform(-0.2, 0.2),
        'oval': None
    }
    confetti['oval'] = canvas.create_oval(
        x, y, x + confetti['size'], y + confetti['size'],
        fill=color, outline='')
    return confetti

def move_confetti(confetti):
    confetti['x'] = confetti['x'] + confetti['dx']
    confetti['y'] = confetti['y'] + confetti['dy']
    confetti['angle'] = confetti['angle'] + confetti['spin']
    confetti['canvas'].move(confetti['oval'], confetti['dx'], confetti['dy'])
    if confetti['y'] < ROWS * CELL_SIZE:
        confetti['canvas'].after(20, lambda: move_confetti(confetti))
    else:
        confetti['canvas'].delete(confetti['oval'])

# Classe principale du jeu Puissance 4
# Remplacée par des fonctions et dictionnaires

def creer_jeu(root):
    jeu = {}
    jeu['root'] = root
    root.title("Puissance 4 - Hacker Edition")
    root.configure(bg='#101010')
    jeu['custom_font'] = font.Font(family="Consolas", size=18, weight="bold")
    jeu['frame'] = tk.Frame(root, bg='#101010')
    jeu['frame'].pack(padx=20, pady=20)
    jeu['label_tour'] = tk.Label(jeu['frame'], text="Au tour du joueur Rouge", font=jeu['custom_font'], fg='#00FF41', bg='#101010')
    jeu['label_tour'].pack(pady=(0,10))
    jeu['canvas'] = tk.Canvas(jeu['frame'], width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='#101010', highlightthickness=0)
    jeu['canvas'].pack()
    jeu['canvas'].bind('<Button-1>', lambda event: jouer_coup(jeu, event))
    jeu['bouton_restart'] = tk.Button(jeu['frame'], text="Recommencer", command=lambda: reinitialiser(jeu), font=jeu['custom_font'], bg='#222', fg='#00FF41', activebackground='#00FF41', activeforeground='#101010', borderwidth=2, relief='ridge')
    jeu['bouton_restart'].pack(pady=10)
    jeu['bouton_score'] = tk.Button(jeu['frame'], text="Score", command=lambda: afficher_score_avec_animation(jeu), font=jeu['custom_font'], bg='#00FF41', fg='#101010', activebackground='#222', activeforeground='#00FF41', borderwidth=2, relief='ridge')
    jeu['bouton_score'].pack(pady=(0,10))
    jeu['style_var'] = tk.StringVar(value="normal")
    jeu['bouton_style'] = tk.Menubutton(jeu['frame'], text="Style", font=jeu['custom_font'], bg='#222', fg='#00FF41', activebackground='#00FF41', activeforeground='#101010', borderwidth=2, relief='ridge')
    jeu['menu_style'] = tk.Menu(jeu['bouton_style'], tearoff=0)
    for style in ["normal", "jungle", "ete", "mythique"]:
        jeu['menu_style'].add_radiobutton(label=style.capitalize(), variable=jeu['style_var'], value=style, command=lambda: changer_style(jeu))
    jeu['bouton_style'].config(menu=jeu['menu_style'])
    jeu['bouton_style'].pack(pady=(0,10))
    jeu['vs_ia'] = False
    def activer_ia():
        jeu['vs_ia'] = not jeu['vs_ia']
        if jeu['vs_ia']:
            jeu['bouton_ia'].config(text="Mode 2 joueurs")
            if jeu['tour'] == 'yellow' and not jeu['animating']:
                jouer_coup_ia(jeu)
        else:
            jeu['bouton_ia'].config(text="Jouer contre l'IA")
    jeu['bouton_ia'] = tk.Button(jeu['frame'], text="Jouer contre l'IA", command=activer_ia, font=jeu['custom_font'], bg='#222', fg='#00FF41', activebackground='#00FF41', activeforeground='#101010', borderwidth=2, relief='ridge')
    jeu['bouton_ia'].pack(pady=(0,10))
    creer_grille(jeu)
    jeu['tour'] = 'red'
    jeu['animating'] = False
    jeu['score'] = {'red': 0, 'yellow': 0}
    jeu['current_style'] = None
    dessiner_grille(jeu)
    return jeu

def creer_grille(jeu):
    jeu['grille'] = []
    for i in range(ROWS):
        ligne = []
        for j in range(COLS):
            ligne.append(None)
        jeu['grille'].append(ligne)

def changer_style(jeu):
    style = jeu['style_var'].get()
    if style == "normal":
        appliquer_style(jeu, bg='#2471a3', fg='#e74c3c', jeton1='#e74c3c', jeton2='#f1c40f', plateau='#2471a3', outline='#154360', arc='#fff', trou='#eaf6fb', fontfam="Arial")
    elif style == "jungle":
        appliquer_style(jeu, bg='#184d27', fg='#f1c40f', jeton1='#27ae60', jeton2='#f1c40f', plateau='#145a32', outline='#229954', arc='#f7ca18', trou='#d4efdf', fontfam="Comic Sans MS")
    elif style == "ete":
        appliquer_style(jeu, bg='#ffe066', fg='#ff5733', jeton1='#ff5733', jeton2='#ffe066', plateau='#ffe066', outline='#ffb347', arc='#fff', trou='#fffbe6', fontfam="Comic Sans MS")
    elif style == "mythique":
        appliquer_style(jeu, bg='#2d014d', fg='#ffd700', jeton1='#ffd700', jeton2='#a259e6', plateau='#2d014d', outline='#a259e6', arc='#fff', trou='#3d1a5a', fontfam="Papyrus")
    dessiner_grille(jeu)

def appliquer_style(jeu, bg, fg, jeton1, jeton2, plateau, outline, arc, trou, fontfam):
    # Création de la police personnalisée
    jeu['custom_font'] = font.Font(family=fontfam, size=20, weight="bold")
    jeu['root'].configure(bg=bg)
    jeu['frame'].configure(bg=bg)
    jeu['label_tour'].configure(bg=bg, fg=fg, font=jeu['custom_font'])

    # Configuration unifiée des boutons (police + couleurs explicites, sans effet de survol)
    bouton_params = {
        'font': jeu['custom_font'],
        'borderwidth': 3,
        'relief': 'groove',
        'highlightthickness': 2,
        'highlightbackground': fg,
        'highlightcolor': fg,
        'cursor': 'hand2',
        'activebackground': outline,  # même couleur que bg pour supprimer effet hover
        'activeforeground': fg,       # même couleur que fg pour supprimer effet hover
    }
    jeu['bouton_restart'].configure(
        bg=outline, fg=fg, **bouton_params
    )
    jeu['bouton_score'].configure(
        bg=fg, fg=bg, activebackground=fg, activeforeground=bg, font=jeu['custom_font'], borderwidth=3, relief='groove', highlightthickness=2, highlightbackground=fg, highlightcolor=fg, cursor='hand2'
    )
    jeu['bouton_style'].configure(
        bg=outline, fg=fg, **bouton_params
    )
    jeu['bouton_ia'].configure(
        bg=outline, fg=fg, **bouton_params
    )

    # Appliquer la police et les couleurs au menu du Menubutton
    try:
        jeu['menu_style'].config(font=jeu['custom_font'], bg=outline, fg=fg, activebackground=outline, activeforeground=fg)
        end = jeu['menu_style'].index('end')
        if end is not None:
            for i in range(end+1):
                jeu['menu_style'].entryconfig(i, font=jeu['custom_font'], fg=fg, bg=outline, activeforeground=fg, activebackground=outline)
    except Exception:
        pass

    jeu['current_style'] = {
        'plateau': plateau, 'outline': outline, 'arc': arc, 'trou': trou,
        'jeton1': jeton1, 'jeton2': jeton2, 'fg': fg
    }

def dessiner_grille(jeu):
    jeu['canvas'].delete('all')
    style = jeu['current_style']
    if style is None:
        style = {
            'plateau': '#181818', 'outline': '#00FF41', 'arc': '#39ff14', 'trou': '#101010',
            'jeton1': '#00FF41', 'jeton2': '#FF00C8', 'fg': '#00FF41'
        }
    # Amélioration esthétique : ombre portée et reflets sur le plateau
    jeu['canvas'].create_rectangle(8, 8, COLS*CELL_SIZE+8, ROWS*CELL_SIZE+8, fill='#222', outline='', width=0)
    jeu['canvas'].create_rectangle(0, 0, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=style['plateau'], outline=style['outline'], width=14)
    # Reflet sur le plateau
    jeu['canvas'].create_arc(0, -ROWS*CELL_SIZE//2, COLS*CELL_SIZE, ROWS*CELL_SIZE//1.5, start=0, extent=180, style='arc', outline='#fff', width=4)
    # Animation des arbres (jungle)
    if jeu['style_var'].get() == "jungle":
        jeu['canvas'].create_rectangle(0, 0, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=style['plateau'], outline=style['outline'], width=12)
        if 'arbre_offset' not in jeu:
            jeu['arbre_offset'] = 0
        jeu['arbre_offset'] = (jeu['arbre_offset'] + 4) % 360  # Ralentir l'animation des arbres
        # Arbres en haut
        for i in range(0, COLS*CELL_SIZE, 60):
            sway = int(8 * math.sin((i + jeu['arbre_offset'])/30))
            jeu['canvas'].create_rectangle(i+25+sway, 0, i+35+sway, 40, fill='#784421', outline='')
            jeu['canvas'].create_oval(i+10+sway, -30, i+50+sway, 30, fill='#229954', outline='')
        # Arbres en bas
        for i in range(0, COLS*CELL_SIZE, 60):
            sway = int(8 * math.sin((i + jeu['arbre_offset'])/30))
            jeu['canvas'].create_rectangle(i+25+sway, ROWS*CELL_SIZE-40, i+35+sway, ROWS*CELL_SIZE, fill='#784421', outline='')
            jeu['canvas'].create_oval(i+10+sway, ROWS*CELL_SIZE-70, i+50+sway, ROWS*CELL_SIZE-30, fill='#229954', outline='')
        jeu['canvas'].create_arc(0, -ROWS*CELL_SIZE//2, COLS*CELL_SIZE, ROWS*CELL_SIZE, start=0, extent=180, style='arc', outline=style['outline'], width=10)
        jeu['canvas'].after(160, lambda: dessiner_grille(jeu))  # Ralentir le rafraîchissement
    # Animation été : soleil en haut à droite
    elif jeu['style_var'].get() == "ete":
        jeu['canvas'].create_oval(COLS*CELL_SIZE-80, -40, COLS*CELL_SIZE+40, 80, fill='#fff700', outline='')
        for i in range(12):
            angle = i * 30
            x1 = COLS*CELL_SIZE-20 + 60*math.cos(math.radians(angle))
            y1 = 40 + 60*math.sin(math.radians(angle))
            x2 = COLS*CELL_SIZE-20 + 80*math.cos(math.radians(angle))
            y2 = 40 + 80*math.sin(math.radians(angle))
            jeu['canvas'].create_line(x1, y1, x2, y2, fill='#fff700', width=4)
    # Animation mythique : éclairs animés en haut du plateau
    elif jeu['style_var'].get() == "mythique":
        # Eclairs animés
        if 'eclair_offset' not in jeu:
            jeu['eclair_offset'] = 0
        jeu['eclair_offset'] = (jeu['eclair_offset'] + 1) % 40
        for i in range(3):
            base_x = 60 + i*180 + random.randint(-10, 10)
            base_y = 10 + random.randint(-5, 5)
            points = [base_x, base_y]
            for j in range(5):
                points.append(base_x + random.randint(-20, 20))
                points.append(base_y + 20 + j*12 + random.randint(-8, 8))
            jeu['canvas'].create_line(points, fill='#ffd700', width=5, smooth=True)
            jeu['canvas'].create_line(points, fill='#fff', width=2, smooth=True)
        jeu['canvas'].after(80, lambda: dessiner_grille(jeu))
    # Animation glitch (lignes qui bougent) et ocean supprimés
    else:
        jeu['canvas'].create_rectangle(0, 0, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=style['plateau'], outline=style['outline'], width=12)
        jeu['canvas'].create_arc(0, -ROWS*CELL_SIZE//2, COLS*CELL_SIZE, ROWS*CELL_SIZE, start=0, extent=180, style='arc', outline=style['outline'], width=10)
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * CELL_SIZE + 12
            y1 = row * CELL_SIZE + 12
            x2 = x1 + CELL_SIZE - 24
            y2 = y1 + CELL_SIZE - 24
            couleur = jeu['grille'][row][col]
            # Effet d'ombre sous chaque jeton
            jeu['canvas'].create_oval(x1+JETON_BORDER+4, y1+JETON_BORDER+4, x2+JETON_BORDER+4, y2+JETON_BORDER+4, fill='#222', outline='')
            if couleur is not None:
                jeu['canvas'].create_oval(x1+JETON_BORDER, y1+JETON_BORDER, x2+JETON_BORDER, y2+JETON_BORDER, fill='#636e72', outline='')
                if couleur == 'red':
                    fill_color = style['jeton1']
                else:
                    fill_color = style['jeton2']
                jeu['canvas'].create_oval(x1, y1, x2, y2, fill=fill_color, outline=style['outline'], width=5)
                # Reflet sur le jeton
                jeu['canvas'].create_arc(x1+10, y1+10, x2-10, y2-10, start=120, extent=120, style='arc', outline=style['arc'], width=7)
                jeu['canvas'].create_oval(x1+18, y1+18, x1+32, y1+32, fill='#fff', outline='')
            else:
                jeu['canvas'].create_oval(x1, y1, x2, y2, fill=style['trou'], outline=style['outline'], width=2)

def jouer_coup(jeu, event):
    if jeu['animating']:
        return
    # Annule le timer d'inactivité si présent
    if 'inactivity_timer' in jeu and jeu['inactivity_timer'] is not None:
        jeu['root'].after_cancel(jeu['inactivity_timer'])
        jeu['inactivity_timer'] = None
    col = event.x // CELL_SIZE
    if col < 0 or col >= COLS:
        return
    ligne = -1
    for row in range(ROWS-1, -1, -1):
        if jeu['grille'][row][col] is None:
            ligne = row
            break
    if ligne != -1:
        animer_jeton(jeu, ligne, col, jeu['tour'])

def jouer_coup_ia(jeu):
    if jeu['animating']:
        return
    # IA intelligente : 1. Cherche à gagner, 2. Bloque l'adversaire, 3. Sinon joue au hasard
    colonnes_valides = [col for col in range(COLS) if jeu['grille'][0][col] is None]
    if not colonnes_valides:
        return
    # 1. Cherche un coup gagnant pour l'IA
    for col in colonnes_valides:
        row = -1
        for r in range(ROWS-1, -1, -1):
            if jeu['grille'][r][col] is None:
                row = r
                break
        if row != -1:
            jeu['grille'][row][col] = 'yellow'
            if verifier_victoire(jeu, row, col):
                jeu['grille'][row][col] = None
                animer_jeton(jeu, row, col, 'yellow')
                return
            jeu['grille'][row][col] = None
    # 2. Bloque un coup gagnant du joueur humain
    for col in colonnes_valides:
        row = -1
        for r in range(ROWS-1, -1):
            if jeu['grille'][r][col] is None:
                row = r
                break
        if row != -1:
            jeu['grille'][row][col] = 'red'
            if verifier_victoire(jeu, row, col):
                jeu['grille'][row][col] = None
                animer_jeton(jeu, row, col, 'yellow')
                return
            jeu['grille'][row][col] = None
    # 3. Sinon, joue au hasard
    col = random.choice(colonnes_valides)
    row = -1
    for r in range(ROWS-1, -1, -1):
        if jeu['grille'][r][col] is None:
            row = r
            break
    if row != -1:
        animer_jeton(jeu, row, col, 'yellow')

def jouer_coup_ia_rouge(jeu):
    # IA joue pour le joueur rouge après 15s d'inactivité
    if jeu['animating'] or jeu['tour'] != 'red':
        return
    colonnes_valides = [col for col in range(COLS) if jeu['grille'][0][col] is None]
    if not colonnes_valides:
        return
    # 1. Cherche un coup gagnant pour l'IA
    for col in colonnes_valides:
        row = -1
        for r in range(ROWS-1, -1, -1):
            if jeu['grille'][r][col] is None:
                row = r
                break
        if row != -1:
            jeu['grille'][row][col] = 'red'
            if verifier_victoire(jeu, row, col):
                jeu['grille'][row][col] = None
                animer_jeton(jeu, row, col, 'red')
                return
            jeu['grille'][row][col] = None
    # 2. Bloque un coup gagnant du jaune
    for col in colonnes_valides:
        row = -1
        for r in range(ROWS-1, -1):
            if jeu['grille'][r][col] is None:
                row = r
                break
        if row != -1:
            jeu['grille'][row][col] = 'yellow'
            if verifier_victoire(jeu, row, col):
                jeu['grille'][row][col] = None
                animer_jeton(jeu, row, col, 'red')
                return
            jeu['grille'][row][col] = None
    # 3. Sinon, joue au hasard
    col = random.choice(colonnes_valides)
    row = -1
    for r in range(ROWS-1, -1, -1):
        if jeu['grille'][r][col] is None:
            row = r
            break
    if row != -1:
        animer_jeton(jeu, row, col, 'red')

def animer_jeton(jeu, row_final, col, couleur):
    jeu['animating'] = True
    # Annule le timer d'inactivité si un jeton est en animation
    if 'inactivity_timer' in jeu and jeu['inactivity_timer'] is not None:
        jeu['root'].after_cancel(jeu['inactivity_timer'])
        jeu['inactivity_timer'] = None
    def animation(etape):
        if etape > row_final:
            jeu['grille'][row_final][col] = couleur
            dessiner_grille(jeu)
            # (Suppression de l'effet sonore)
            positions = verifier_victoire(jeu, row_final, col)
            if positions is not None:
                if couleur == 'red':
                    jeu['label_tour'].config(text="Le joueur Rouge a gagné !", fg=COULEURS['red'])
                else:
                    jeu['label_tour'].config(text="Le joueur Jaune a gagné !", fg=COULEURS['yellow'])
                animer_victoire(jeu, positions, couleur)
            else:
                if couleur == 'red':
                    jeu['tour'] = 'yellow'
                else:
                    jeu['tour'] = 'red'
                if jeu['tour'] == 'red':
                    jeu['label_tour'].config(text="Au tour du joueur Rouge", fg=COULEURS['red'])
                else:
                    jeu['label_tour'].config(text="Au tour du joueur Jaune", fg=COULEURS['yellow'])
                jeu['animating'] = False
                # Timer d'inactivité pour tous les modes, à chaque tour
                def auto_joue():
                    if not jeu['animating']:
                        if jeu['tour'] == 'red':
                            jouer_coup_ia_rouge(jeu)
                        elif jeu['tour'] == 'yellow':
                            jouer_coup_ia(jeu)
                jeu['inactivity_timer'] = jeu['root'].after(15000, auto_joue)
            return
        dessiner_grille(jeu)
        x1 = col * CELL_SIZE + 12
        y1 = etape * CELL_SIZE + 12
        x2 = x1 + CELL_SIZE - 24
        y2 = y1 + CELL_SIZE - 24
        jeu['canvas'].create_oval(x1+JETON_BORDER, y1+JETON_BORDER, x2+JETON_BORDER, y2+JETON_BORDER, fill='#636e72', outline='')
        jeu['canvas'].create_oval(x1, y1, x2, y2, fill=COULEURS[couleur], outline='#b7950b' if couleur=='yellow' else '#922b21', width=5)
        jeu['canvas'].create_arc(x1+10, y1+10, x2-10, y2-10, start=120, extent=120, style='arc', outline='#fff', width=7)
        jeu['canvas'].create_oval(x1+18, y1+18, x1+32, y1+32, fill='#fff', outline='')
        jeu['root'].after(30, lambda: animation(etape+1))
    animation(0)

def afficher_score_avec_animation(jeu):
    top = tk.Toplevel(jeu['root'])
    top.title("Score - Hacker Edition")
    top.geometry("1x1+400+200")
    top.configure(bg='#101010')
    couleurs_confetti = ['#00FF41', '#FF00C8', '#39ff14', '#00fff7', '#fff', '#222']
    canvas_confetti = tk.Canvas(top, width=340, height=220, bg='#101010', highlightthickness=0)
    canvas_confetti.place(x=0, y=0)
    label_rouge = tk.Label(top, text="Rouge : " + str(jeu['score']['red']), font=jeu['custom_font'], fg='#00FF41', bg='#101010')
    label_jaune = tk.Label(top, text="Jaune : " + str(jeu['score']['yellow']), font=jeu['custom_font'], fg='#FF00C8', bg='#101010')
    label_rouge.place(relx=0.5, rely=0.3, anchor='center')
    label_jaune.place(relx=0.5, rely=0.6, anchor='center')
    def reset_score():
        jeu['score']['red'] = 0
        jeu['score']['yellow'] = 0
        label_rouge.config(text="Rouge : 0")
        label_jaune.config(text="Jaune : 0")
    bouton_reset = tk.Button(top, text="Réinitialiser le score", command=reset_score, font=jeu['custom_font'], bg='#222', fg='#00FF41', activebackground='#00FF41', activeforeground='#101010', borderwidth=2, relief='ridge')
    bouton_reset.place(relx=0.5, rely=0.85, anchor='center')
    def grow(w, h):
        if w < 340:
            w = w + 34
        if h < 220:
            h = h + 22
        top.geometry(str(w) + "x" + str(h) + "+400+200")
        if w < 340 or h < 220:
            top.after(10, lambda: grow(w, h))
        else:
            top.geometry("340x220+400+200")
    grow(1, 1)
    def confetti_anim():
        for i in range(12):
            x = random.randint(0, 340)
            y = random.randint(0, 40)
            size = random.randint(8, 18)
            color = random.choice(couleurs_confetti)
            oval = canvas_confetti.create_oval(x, y, x+size, y+size, fill=color, outline='')
            def move_confetti(oval=oval, dy=random.uniform(2, 4)):
                canvas_confetti.move(oval, 0, dy)
                coords = canvas_confetti.coords(oval)
                if coords != [] and coords[3] < 220:
                    canvas_confetti.after(30, lambda: move_confetti(oval, dy))
                else:
                    canvas_confetti.delete(oval)
            move_confetti()
        canvas_confetti.after(300, confetti_anim)
    confetti_anim()

def animer_victoire(jeu, positions, couleur):
    def blink(etape):
        dessiner_grille(jeu)
        if etape % 2 == 0:
            for pos in positions:
                r = pos[0]
                c = pos[1]
                x1 = c * CELL_SIZE + 12
                y1 = r * CELL_SIZE + 12
                x2 = x1 + CELL_SIZE - 24
                y2 = y1 + CELL_SIZE - 24
                jeu['canvas'].create_oval(x1, y1, x2, y2, fill='#101010', outline='#00FF41', width=8)
        if etape == 2:
            lancer_confettis(jeu, positions, couleur)
        if etape < 8:
            jeu['root'].after(120, lambda: blink(etape+1))
        else:
            jeu['root'].after(900, lambda: reinitialiser(jeu))
            jeu['animating'] = False
    jeu['score'][couleur] = jeu['score'][couleur] + 1
    blink(0)

def lancer_confettis(jeu, positions, couleur):
    # Empêche de lancer plusieurs animations de confettis en même temps
    if getattr(jeu, 'confetti_animating', False):
        return
    jeu.confetti_animating = True
    couleurs_confetti = ['#00FF41', '#FF00C8', '#39ff14', '#00fff7', '#fff', '#222']
    confetti_count = 30  # Limite le nombre de confettis
    confetti_restants = {'count': confetti_count}
    def confetti_callback():
        confetti_restants['count'] -= 1
        if confetti_restants['count'] <= 0:
            jeu.confetti_animating = False
    for i in range(confetti_count):
        x = random.randint(0, COLS*CELL_SIZE)
        y = random.randint(0, 40)
        color = random.choice(couleurs_confetti)
        confetti = creer_confetti(jeu['canvas'], x, y, color)
        confetti['size'] = random.randint(8, 22)
        jeu['canvas'].itemconfig(confetti['oval'], width=0)
        def move_and_callback(confetti=confetti):
            move_confetti(confetti)
            confetti_callback()
        move_and_callback()

def verifier_victoire(jeu, row, col):
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    couleur = jeu['grille'][row][col]
    for direction in directions:
        dr = direction[0]
        dc = direction[1]
        count = 1
        positions = [(row, col)]
        for d in [1, -1]:
            r = row
            c = col
            while True:
                r = r + dr * d
                c = c + dc * d
                if r >= 0 and r < ROWS and c >= 0 and c < COLS and jeu['grille'][r][c] == couleur:
                    count = count + 1
                    positions.append((r, c))
                else:
                    break
        if count >= 4:
            return positions[:4]
    return None

def reinitialiser(jeu):
    # Annule le timer d'inactivité si présent
    if 'inactivity_timer' in jeu and jeu['inactivity_timer'] is not None:
        jeu['root'].after_cancel(jeu['inactivity_timer'])
        jeu['inactivity_timer'] = None
    creer_grille(jeu)
    jeu['tour'] = 'red'
    jeu['label_tour'].config(text="Au tour du joueur Rouge", fg=COULEURS['red'])
    dessiner_grille(jeu)
    jeu['animating'] = False
    # Redémarre le timer d'inactivité pour le premier tour
    def auto_joue():
        if not jeu['animating']:
            if jeu['tour'] == 'red':
                jouer_coup_ia_rouge(jeu)
            elif jeu['tour'] == 'yellow':
                jouer_coup_ia(jeu)
    jeu['inactivity_timer'] = jeu['root'].after(15000, auto_joue)

if __name__ == "__main__":
    root = tk.Tk()
    jeu = creer_jeu(root)
    root.mainloop()
