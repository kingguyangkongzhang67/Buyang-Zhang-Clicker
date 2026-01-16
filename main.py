import pygame, random, sys, math, time, os, threading

pygame.init()
pygame.mixer.init()

# setup 
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Charlie Clicker 5000")

# FONT
h1 = pygame.font.SysFont("Comic Sans MS", 72)
h2 = pygame.font.SysFont("Comic Sans MS", 60)
h3 = pygame.font.SysFont("Comic Sans MS", 48)

t1 = pygame.font.SysFont("Comic Sans MS", 32)
t2 = pygame.font.SysFont("Comic Sans MS", 24)

# load sprites / assets

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

beewu = pygame.image.load(os.path.join(ASSETS, "beewu.png")).convert_alpha()
beewu_rect = beewu.get_rect(center=(WIDTH / 2, HEIGHT / 2))

noodleBg = pygame.image.load(os.path.join(ASSETS, "noodlebg.png")).convert_alpha()
noodleBg_rect = noodleBg.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# sounds

SOUND = os.path.join(BASE, "sounds")

monk = pygame.mixer.Sound(SOUND + "\monkey.mp3")
monk.play(-1)

lugas = pygame.mixer.Sound(SOUND + "\lugas.mp3")

tada = pygame.mixer.Sound(SOUND + "\yipe.mp3")
tadant = pygame.mixer.Sound(SOUND + "\yipent.mp3")


# other shit

clock = pygame.time.Clock()
die = 0

gameState = 0
'''
important

0 = menu screen
1 = clicker ui
2 = shop nps
3 = shop rate
'''
noodles = 0.0
nps = 0
rate = 1

# text rendering
PULSE = 1.4  # cycles per second
SPEDD = 240  # degrees per second
SPINNY = 1.0
spinnyStart = None


text = "I like noodles"
texts = ["I like noodles", "No grapefruit emoji :("]

def updText():
    global text 
    global texts
    while True:
        text = texts[random.randint(0,len(texts)-1)]
        time.sleep(30)
th3 = threading.Thread(target=updText, daemon=True)
th3.start()

def rainbowTitle(now: float, titleText: str, baseSize: int, pulseSize: int) -> pygame.Surface:
    pulse = math.sin(now * PULSE * 2 * math.pi)
    size = max(12, int(baseSize + pulseSize * pulse))
    font = pygame.font.SysFont("Comic Sans MS", size)

    hue = (now * SPEDD) % 360
    color = pygame.Color(0)
    color.hsva = (hue, 100, 100, 100)
    return font.render(titleText, True, color)

def spinnySpinSpin(now: float) -> pygame.Surface:
    global text
    return rainbowTitle(now, text, 72, 24)

def formatCount(value: float):
    n = int(value)
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 10_000:
        return f"{n / 1_000:.1f}K"
    return str(n)

shopNpsItems = [
    {"name": "Basic Bee", "desc": "+1 noodles/sec", "base_cost": 75, "cost_mult": 1.8, "rate": 0, "nps": 1, "owned": 0},
    {"name": "Honey Bee", "desc": "+7 noodles/sec", "base_cost": 875, "cost_mult": 1.6, "rate": 0, "nps": 10, "owned": 0},
    {"name": "Bee Wu", "desc": "+15 noodles/sec", "base_cost": 1835, "cost_mult": 1.6, "rate": 0, "nps": 50, "owned": 0},
    {"name": "Super Bee Wu", "desc": "+60 noodles/sec", "base_cost": 6875, "cost_mult": 1.5, "rate": 0, "nps": 60, "owned": 0},
    {"name": "Mega Bee Wu", "desc": "+200 noodles/sec", "base_cost": 19900, "cost_mult": 1.5, "rate": 0, "nps": 200, "owned": 0},
    {"name": "Super Mega Bee Wu", "desc": "+525 noodles/sec", "base_cost": 36750, "cost_mult": 1.5, "rate": 0, "nps": 525, "owned": 0},
    {"name": "Giga Bee Wu", "desc": "+1225 noodles/sec", "base_cost": 105395, "cost_mult": 1.5, "rate": 0, "nps": 1225, "owned": 0},
    {"name": "Super Giga Mega Bee Wu", "desc": "+3000 noodles/sec", "base_cost": 375125, "cost_mult": 1.4, "rate": 0, "nps": 3000, "owned": 0},
    {"name": "Super Giga Ultra Mega Bee Wu", "desc": "+8500 noodles/sec", "base_cost": 875925, "cost_mult": 1.4, "rate": 0, "nps": 8500, "owned": 0},
    {"name": "Colossal Bee Wu", "desc": "+21250 noodles/sec", "base_cost": 1650000, "cost_mult": 1.4, "rate": 0, "nps": 21250, "owned": 0},
    {"name": "Ultra Colossal Bee Wu", "desc": "+45000 noodles/sec", "base_cost": 2900000, "cost_mult": 1.4, "rate": 0, "nps": 45000, "owned": 0},
    {"name": "Beidi Gu", "desc": "+100000 noodles/sec", "base_cost": 5000000, "cost_mult": 1.3, "rate": 0, "nps": 100000, "owned": 0},
]

shopRateItems = [
    {"name": "Maruchan", "desc": "+1 per click", "base_cost": 15, "cost_mult": 2, "rate": 1, "nps": 0, "owned": 0},
    {"name": "Shin Ramen", "desc": "+5 per click", "base_cost": 125, "cost_mult": 1.5, "rate": 5, "nps": 0, "owned": 0},
    {"name": "Grapefruit", "desc": "+25 per click", "base_cost": 900, "cost_mult": 1.5, "rate": 25, "nps": 0, "owned": 0},
]

def getCost(item: dict) -> int:
    return int(item["base_cost"] * (item["cost_mult"] ** item["owned"]))

def buildShopRects(items: list, area: pygame.Rect, card_w: int, card_h: int, gap: int) -> list:
    count = len(items)
    if count == 0:
        return []
    cols = max(1, (area.width + gap) // (card_w + gap))
    rows = math.ceil(count / cols)

    max_w = (area.width - gap * (cols - 1)) // cols
    max_h = (area.height - gap * (rows - 1)) // rows
    card_w = max(220, min(card_w, max_w))
    card_h = max(80, min(card_h, max_h))

    rects = []
    for idx in range(count):
        row = idx // cols
        col = idx % cols
        x = area.x + col * (card_w + gap)
        y = area.y + row * (card_h + gap)
        rects.append(pygame.Rect(x, y, card_w, card_h))
    return rects

shopArea = pygame.Rect(60, 150, WIDTH - 120, HEIGHT - 230)
shopCardW = 300
shopCardH = 120
shopCardGap = 12
npsButton_rect = pygame.Rect(40, HEIGHT - 150, 320, 52)
rateButton_rect = pygame.Rect(40, HEIGHT - 90, 320, 52)
backButton_rect = pygame.Rect(40, 30, 180, 50)
shopRects = []
lastShopMessage = ""
lastShopMessageTime = 0.0

# THREADING
def test1():
    while True:
        print("FPS: " + str(math.floor(clock.get_fps())))
        time.sleep(1)
th1 = threading.Thread(target=test1, daemon=True)
th1.start()

# keeps track of running time
def counter():
    global spinnyStart
    num = 1
    while True:
        if num % 3 == 0 and num % 5 == 0:
            print("FizzBuzz!")
            spinnyStart = time.time()
        elif num % 3 == 0:
            print("Fizz")
        elif num % 5 == 0:
            print("buzz")
        else:
            print(num)
        num += 1
        time.sleep(1)

th2 = threading.Thread(target=counter, daemon=True)
th2.start()

def collision(rec: pygame.Rect, x: int, y: int):
    return rec.collidepoint(x, y)

def addNoodles():
    global noodles
    noodles += rate 

def addRate(ratte: int):
    global rate 
    rate += ratte 

def addNps(npss: int):
    global nps
    nps += npss
    

# main running loop type shiiiittt
while not die:
    now = time.time()
    dt = clock.tick(120) / 1000
    noodles += nps * dt

    currentShopItems = []
    if gameState == 2:
        currentShopItems = shopNpsItems
    elif gameState == 3:
        currentShopItems = shopRateItems
    shopRects = buildShopRects(currentShopItems, shopArea, shopCardW, shopCardH, shopCardGap)
    # RECOGNIZE QUIT
    for event in pygame.event.get():
        # DIE
        if event.type == pygame.QUIT:
            die = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            # button 1 = left mouse
            if event.button == 1:
                mouse_pos = event.pos  # pos xy
                print(f"THIS IS A TEST FUNCTION. your cursor has been clicked at: {mouse_pos}")
                (x, y) = mouse_pos
                print(str(x) + "\n" + str(y))
                if gameState == 0:
                    gameState = 1
                elif gameState == 1:
                    if collision(beewu_rect, x, y):
                        print("Detected click. " + str(rate) + " noodles added.")
                        lugas.play()
                        addNoodles()
                    elif npsButton_rect.collidepoint(x, y):
                        gameState = 2
                    elif rateButton_rect.collidepoint(x, y):
                        gameState = 3
                elif gameState in (2, 3):
                    if backButton_rect.collidepoint(x, y):
                        gameState = 1
                    else:
                        for idx, rect in enumerate(shopRects):
                            if rect.collidepoint(x, y):
                                item = currentShopItems[idx]
                                cost = getCost(item)
                                if noodles >= cost:
                                    noodles -= cost
                                    item["owned"] += 1
                                    rate += item["rate"]
                                    nps += item["nps"]
                                    lastShopMessage = f"Yayyyyyy you bought {item['name']} so sugoi twin"
                                    tada.play()
                                    lastShopMessageTime = now
                                else:
                                    lastShopMessage = "You are POOR"
                                    tadant.play()
                                    lastShopMessageTime = now
                                break
    
    # BACKGROUND
    screen.blit(noodleBg, noodleBg_rect)

    # starting 
    if gameState == 0:
        title_surface = rainbowTitle(now, "Buyang Zhang Clicker 5000", 84, 18)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 60))
        screen.blit(title_surface, title_rect)
        hint_text = t1.render("Click anywhere to play", True, (0, 0, 0))
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60)))
    elif gameState == 1:
        screen.blit(beewu, beewu_rect)
        title_surface = spinnySpinSpin(now)
        if spinnyStart != None:
            elapsed = now - spinnyStart
            if elapsed <= SPINNY:
                angle = 360 * (elapsed / SPINNY)
                title_surface = pygame.transform.rotate(title_surface, angle)
            else:
                spinnyStart = None
        title_rect = title_surface.get_rect(center=(WIDTH / 2, 100))
        screen.blit(title_surface, title_rect)
        noodles_text = h2.render(f"Noodles: {formatCount(noodles)}", True, (255, 255, 0))
        nps_text = t1.render(f"Noodles/s: {formatCount(nps)}", True, (0, 255, 255))
        rate_text = t1.render(f"Noodles per click: {formatCount(rate)}", True, (255, 120, 0))
        screen.blit(noodles_text, (40, 20))
        screen.blit(nps_text, (40, 90))
        screen.blit(rate_text, (40, 130))

        pygame.draw.rect(screen, (0, 255, 0), npsButton_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 255), rateButton_rect, border_radius=10)
        nps_btn_text = t1.render("Labor Market", True, (0, 0, 0))
        rate_btn_text = t1.render("Taco Bell", True, (0, 0, 0))
        screen.blit(nps_btn_text, nps_btn_text.get_rect(center=npsButton_rect.center))
        screen.blit(rate_btn_text, rate_btn_text.get_rect(center=rateButton_rect.center))
    elif gameState in (2, 3):
        pygame.draw.rect(screen, (255, 255, 0), (30, 20, WIDTH - 60, HEIGHT - 40), border_radius=14)
        shop_title = "Labor Market" if gameState == 2 else "Taco bell"
        title_text = h2.render(shop_title, True, (0, 0, 0))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH / 2, 70)))

        pygame.draw.rect(screen, (50, 50, 50), backButton_rect, border_radius=10)
        back_text = t1.render("Back", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=backButton_rect.center))

        for idx, item in enumerate(currentShopItems):
            rect = shopRects[idx]
            cost = getCost(item)
            can_buy = noodles >= cost
            color = (0, 230, 0) if can_buy else (230, 40, 40)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            name_text = t1.render(item["name"], True, (0, 0, 0))
            desc_text = t2.render(item["desc"], True, (0, 0, 0))
            cost_text = t2.render(f"Cost: {formatCount(cost)} | Owned: {item['owned']}", True, (0, 0, 0))
            name_y = rect.y + 10
            desc_y = rect.y + 46
            cost_y = rect.y + rect.h - 40
            screen.blit(name_text, (rect.x + 10, name_y))
            screen.blit(desc_text, (rect.x + 10, desc_y))
            screen.blit(cost_text, (rect.x + 10, cost_y))

        if lastShopMessage and now - lastShopMessageTime <= 2.0:
            msg = t1.render(lastShopMessage, True, (255, 0, 0))
            screen.blit(msg, (40, HEIGHT - 60))

    pygame.display.flip()
