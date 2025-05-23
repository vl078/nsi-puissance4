import tkinter as tk
from tkinter import messagebox, font
import random
import math

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
    jeu['style_var'] = tk.StringVar(value="matrix")
    jeu['bouton_style'] = tk.Menubutton(jeu['frame'], text="Style", font=jeu['custom_font'], bg='#222', fg='#00FF41', activebackground='#00FF41', activeforeground='#101010', borderwidth=2, relief='ridge')
    jeu['menu_style'] = tk.Menu(jeu['bouton_style'], tearoff=0)
    for style in ["matrix", "glitch", "normal", "jungle", "ocean"]:
        jeu['menu_style'].add_radiobutton(label=style.capitalize(), variable=jeu['style_var'], value=style, command=lambda: changer_style(jeu))
    jeu['bouton_style'].config(menu=jeu['menu_style'])
    jeu['bouton_style'].pack(pady=(0,10))
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
    if style == "matrix":
        appliquer_style(jeu, bg='#101010', fg='#00FF41', jeton1='#00FF41', jeton2='#FF00C8', plateau='#181818', outline='#00FF41', arc='#39ff14', trou='#101010', fontfam="Consolas")
    elif style == "glitch":
        appliquer_style(jeu, bg='#1a0033', fg='#ff00cc', jeton1='#ff00cc', jeton2='#00fff7', plateau='#2d0036', outline='#ff00cc', arc='#00fff7', trou='#0a001a', fontfam="Courier New")
    elif style == "normal":
        appliquer_style(jeu, bg='#2471a3', fg='#e74c3c', jeton1='#e74c3c', jeton2='#f1c40f', plateau='#2471a3', outline='#154360', arc='#fff', trou='#eaf6fb', fontfam="Arial")
    elif style == "jungle":
        appliquer_style(jeu, bg='#184d27', fg='#f1c40f', jeton1='#27ae60', jeton2='#f1c40f', plateau='#145a32', outline='#229954', arc='#f7ca18', trou='#d4efdf', fontfam="Comic Sans MS")
    elif style == "ocean":
        appliquer_style(jeu, bg='#0e4d92', fg='#00fff7', jeton1='#00fff7', jeton2='#0055ff', plateau='#0e4d92', outline='#00fff7', arc='#fff', trou='#eaf6fb', fontfam="Verdana")
    dessiner_grille(jeu)

def appliquer_style(jeu, bg, fg, jeton1, jeton2, plateau, outline, arc, trou, fontfam):
    jeu['root'].configure(bg=bg)
    jeu['frame'].configure(bg=bg)
    jeu['label_tour'].configure(bg=bg, fg=fg, font=font.Font(family=fontfam, size=18, weight="bold"))
    jeu['bouton_restart'].configure(bg=outline, fg=fg, activebackground=fg, activeforeground=bg)
    jeu['bouton_score'].configure(bg=fg, fg=bg, activebackground=outline, activeforeground=fg)
    jeu['bouton_style'].configure(bg=outline, fg=fg, activebackground=fg, activeforeground=bg)
    jeu['custom_font'] = font.Font(family=fontfam, size=18, weight="bold")
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
    if jeu['style_var'].get() == "ocean":
        jeu['canvas'].create_rectangle(0, 0, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=style['plateau'], outline=style['outline'], width=12)
        for i in range(0, COLS*CELL_SIZE, 40):
            jeu['canvas'].create_arc(i-40, ROWS*CELL_SIZE-40, i+80, ROWS*CELL_SIZE+40, start=0, extent=180, style='arc', outline='#00fff7', width=8)
        jeu['canvas'].create_arc(0, -ROWS*CELL_SIZE//2, COLS*CELL_SIZE, ROWS*CELL_SIZE, start=0, extent=180, style='arc', outline=style['outline'], width=10)
    elif jeu['style_var'].get() == "jungle":
        jeu['canvas'].create_rectangle(0, 0, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=style['plateau'], outline=style['outline'], width=12)
        for i in range(0, COLS*CELL_SIZE, 60):
            jeu['canvas'].create_rectangle(i+25, ROWS*CELL_SIZE-40, i+35, ROWS*CELL_SIZE, fill='#784421', outline='')
            jeu['canvas'].create_oval(i+10, ROWS*CELL_SIZE-70, i+50, ROWS*CELL_SIZE-30, fill='#229954', outline='')
        jeu['canvas'].create_arc(0, -ROWS*CELL_SIZE//2, COLS*CELL_SIZE, ROWS*CELL_SIZE, start=0, extent=180, style='arc', outline=style['outline'], width=10)
    elif jeu['style_var'].get() == "glitch":
        jeu['canvas'].create_rectangle(0, 0, COLS*CELL_SIZE, ROWS*CELL_SIZE, fill=style['plateau'], outline=style['outline'], width=12)
        for i in range(0, ROWS*CELL_SIZE, 18):
            jeu['canvas'].create_line(0, i, COLS*CELL_SIZE, i, fill=random.choice(['#ff00cc', '#00fff7', '#fff']), width=2)
        jeu['canvas'].create_arc(0, -ROWS*CELL_SIZE//2, COLS*CELL_SIZE, ROWS*CELL_SIZE, start=0, extent=180, style='arc', outline=style['outline'], width=10)
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
            if couleur is not None:
                jeu['canvas'].create_oval(x1+JETON_BORDER, y1+JETON_BORDER, x2+JETON_BORDER, y2+JETON_BORDER, fill='#636e72', outline='')
                if couleur == 'red':
                    fill_color = style['jeton1']
                else:
                    fill_color = style['jeton2']
                jeu['canvas'].create_oval(x1, y1, x2, y2, fill=fill_color, outline=style['outline'], width=5)
                jeu['canvas'].create_arc(x1+10, y1+10, x2-10, y2-10, start=120, extent=120, style='arc', outline=style['arc'], width=7)
            else:
                jeu['canvas'].create_oval(x1, y1, x2, y2, fill=style['trou'], outline=style['outline'], width=2)

def jouer_coup(jeu, event):
    if jeu['animating']:
        return
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

def animer_jeton(jeu, row_final, col, couleur):
    jeu['animating'] = True
    def animation(etape):
        if etape > row_final:
            jeu['grille'][row_final][col] = couleur
            dessiner_grille(jeu)
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
    couleurs_confetti = ['#00FF41', '#FF00C8', '#39ff14', '#00fff7', '#fff', '#222']
    for i in range(100):
        x = random.randint(0, COLS*CELL_SIZE)
        y = random.randint(0, 40)
        color = random.choice(couleurs_confetti)
        confetti = creer_confetti(jeu['canvas'], x, y, color)
        confetti['size'] = random.randint(8, 22)
        jeu['canvas'].itemconfig(confetti['oval'], width=0)
        confetti.move()

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
    creer_grille(jeu)
    jeu['tour'] = 'red'
    jeu['label_tour'].config(text="Au tour du joueur Rouge", fg=COULEURS['red'])
    dessiner_grille(jeu)
    jeu['animating'] = False

if __name__ == "__main__":
    root = tk.Tk()
    jeu = creer_jeu(root)
    root.mainloop()

