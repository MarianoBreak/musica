import pygame
import os

# Inicializar Pygame y el reproductor de audio
pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((900, 650))
pygame.display.set_caption("ROCOLA PROFESIONAL V2 - PNG EDITION")
font = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 14, bold=True)

# --- CARGAR FONDO (PNG) ---
fondo_img = None
if os.path.exists("fondo.png"):
    try:
        img_bg = pygame.image.load("fondo.png").convert_alpha()
        fondo_img = pygame.transform.scale(img_bg, (900, 650))
    except Exception as e:
        print("Error al cargar fondo.png:", e)

#  CONFIGURACION DE CANCIONES Y DATOS 
RUTA_SODA_AUDIO = "Soda Stereo - De musica ligera.mp3"

ROCOLA_DATA = {
    "Soda Stereo": {
        "temas": ["De música ligera"] + [f"Tema Soda {i}" for i in range(2, 21)],
        "archivos": [RUTA_SODA_AUDIO] + [None]*19,
        "png": "Soda Stereo.png"  # Imagen para el panel derecho
    },
    "Los Redondos": {"temas": [f"Tema Redondos {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/redondos.png"},
    "La Renga": {"temas": [f"Tema Renga {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/larenga.png"},
    "Divididos": {"temas": [f"Tema Divididos {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/divididos.png"},
    "Las Pelotas": {"temas": [f"Tema Pelotas {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/pelotas.png"},
    "Babasónicos": {"temas": [f"Tema Baba {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/baba.png"},
    "Catupecu": {"temas": [f"Tema Catu {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/catu.png"},
    "Guasones": {"temas": [f"Tema Guasones {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/guasones.png"},
    "Andando Descalzo": {"temas": [f"Tema AD {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/ad.png"},
    "Eruca Sativa": {"temas": [f"Tema Eruca {i}" for i in range(1, 21)], "archivos": [None]*20, "png": "bandas/eruca.png"},
}

lista_bandas = list(ROCOLA_DATA.keys())
banda_actual = 0
tema_actual = 0
estado = "STOP"
velocidad = 1.0
busqueda = ""
input_activo = False
mostrar_info = False

# Botones de control inferiores
botones = [
    {"id": "prev", "icon": "|<", "x": 15, "y": 580, "w": 65},
    {"id": "play", "icon": "PLAY", "x": 85, "y": 580, "w": 75},
    {"id": "pause", "icon": "PAUSE", "x": 165, "y": 580, "w": 75},
    {"id": "stop", "icon": "STOP", "x": 245, "y": 580, "w": 65},
    {"id": "next", "icon": ">|", "x": 315, "y": 580, "w": 65},
    {"id": "slow", "icon": "0.5x", "x": 385, "y": 580, "w": 65},
    {"id": "fast", "icon": "2.0x", "x": 455, "y": 580, "w": 65},
    {"id": "search", "icon": "BUSCAR", "x": 525, "y": 580, "w": 85},
    {"id": "info", "icon": "INFO", "x": 615, "y": 580, "w": 75},
]

def reproducir_tema():
    global estado
    banda_nombre = lista_bandas[banda_actual]
    archivos = ROCOLA_DATA[banda_nombre].get("archivos", [])
    
    if tema_actual < len(archivos) and archivos[tema_actual] and os.path.exists(archivos[tema_actual]):
        pygame.mixer.music.load(archivos[tema_actual])
        pygame.mixer.music.play()
        estado = "PLAY"
    else:
        pygame.mixer.music.stop()
        estado = "PLAY (Sin audio)"

def get_filtro():
    if not busqueda: return lista_bandas
    return [b for b in lista_bandas if busqueda.lower() in b.lower()]

clock = pygame.time.Clock()
corriendo = True

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            filtro = get_filtro()
            for i, b in enumerate(filtro):
                y = 80 + i*42
                if 30 <= mx <= 400 and y <= my <= y+38:
                    banda_actual = lista_bandas.index(b)
                    tema_actual = 0
                    pygame.mixer.music.stop()
                    estado = "STOP"

            for btn in botones:
                if pygame.Rect(btn["x"], btn["y"], btn["w"], 45).collidepoint(mx, my):
                    if btn["id"] == "play":
                        if estado == "PAUSE":
                            pygame.mixer.music.unpause()
                            estado = "PLAY"
                        else:
                            reproducir_tema()
                    elif btn["id"] == "pause":
                        if estado == "PLAY":
                            pygame.mixer.music.pause()
                            estado = "PAUSE"
                    elif btn["id"] == "stop":
                        pygame.mixer.music.stop()
                        estado = "STOP"
                    elif btn["id"] == "next": 
                        tema_actual = (tema_actual + 1) % 20
                        reproducir_tema()
                    elif btn["id"] == "prev": 
                        tema_actual = (tema_actual - 1) % 20
                        reproducir_tema()
                    elif btn["id"] == "fast": velocidad = min(2.0, velocidad + 0.25)
                    elif btn["id"] == "slow": velocidad = max(0.25, velocidad - 0.25)
                    elif btn["id"] == "search": input_activo = not input_activo
                    elif btn["id"] == "info": mostrar_info = not mostrar_info

        if event.type == pygame.KEYDOWN and input_activo:
            if event.key == pygame.K_BACKSPACE:
                busqueda = busqueda[:-1]
            elif event.key == pygame.K_RETURN:
                input_activo = False
            else:
                busqueda += event.unicode

    # fondo PNG
    if fondo_img:
        ventana.blit(fondo_img, (0, 0))
    else:
        ventana.fill((10, 10, 10))

    filtro = get_filtro()

    # LISTA DE BANDAS 
    if not filtro:
        ventana.blit(font_small.render("No se encontró", True, (255, 80, 80)), (30, 80))
    else:
        for i, b in enumerate(filtro):
            y = 80 + i*42
            if y < 560:
                es_actual = (lista_bandas[banda_actual] == b)
                box_rect = pygame.Rect(30, y, 370, 38)
                
                if es_actual:
                    color_fondo = (30, 90, 50)  # Verde elegante y atenuado
                    color_borde = (29, 185, 84)
                    texto_color = (255, 255, 255)
                else:
                    color_fondo = (35, 35, 35)  # Gris oscuro sólido para los demás
                    color_borde = (60, 60, 60)
                    texto_color = (200, 200, 200)
                
                # Dibujar caja del botón de banda
                s_box = pygame.Surface((370, 38), pygame.SRCALPHA)
                s_box.fill(color_fondo)
                ventana.blit(s_box, (30, y))
                pygame.draw.rect(ventana, color_borde, box_rect, width=1, border_radius=8)
                
                # Nombre de la banda visible
                ventana.blit(font_small.render(b, True, texto_color), (45, y + 10))

    # Panel derecho con info de la banda actual
    banda_nombre = lista_bandas[banda_actual]
    
    panel_rect = pygame.Rect(450, 80, 410, 480)
    panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    panel_surf.fill((0, 0, 0, 160))
    ventana.blit(panel_surf, (panel_rect.x, panel_rect.y))

    # Mostrar la imagen grande del álbum en el panel derecho (ÚNICAMENTE AQUÍ)
    ruta_img_banda = ROCOLA_DATA[banda_nombre]["png"]
    if os.path.exists(ruta_img_banda):
        try:
            img_grande = pygame.transform.scale(pygame.image.load(ruta_img_banda).convert_alpha(), (370, 160))
            ventana.blit(img_grande, (470, 100))
        except Exception:
            pass

    tema_nombre = ROCOLA_DATA[banda_nombre]["temas"][tema_actual]
    ventana.blit(font.render(banda_nombre, True, (255, 255, 255)), (470, 280))
    ventana.blit(font_small.render(f"Tema: {tema_nombre}", True, (200, 200, 200)), (470, 320))
    ventana.blit(font_small.render(f"Estado: {estado} | Velocidad: {velocidad}x", True, (29, 185, 84)), (470, 360))
    
    if input_activo:
        ventana.blit(font_small.render(f"Buscando: {busqueda}_", True, (255, 255, 0)), (470, 410))

    # ENTORNO GRAFICO DE BOTONES INFERIORES
    for btn in botones:
        btn_rect = pygame.Rect(btn["x"], btn["y"], btn["w"], 45)
        color_fondo = (0, 120, 215) if btn["id"] == "search" and input_activo else (40, 40, 40)
        
        pygame.draw.rect(ventana, color_fondo, btn_rect, border_radius=8)
        pygame.draw.rect(ventana, (100, 100, 100), btn_rect, width=2, border_radius=8)
        
        text_surf = font_small.render(btn["icon"], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=btn_rect.center)
        ventana.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
