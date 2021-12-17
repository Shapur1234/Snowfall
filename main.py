import globals
import gameobjects

from pygame import time
import time
import pygame


def main():
    pygame.init()
    pygame.display.set_caption("🎅 🎅 🎅 🎅 🎅")
    pygame.display.set_icon(pygame.image.load("Textures/Icon.png"))

    pygame.time.set_timer(pygame.USEREVENT + 1, globals.PhysicsTimescale)
    pygame.time.set_timer(pygame.USEREVENT + 2, 2)

    screen = pygame.display.set_mode((globals.ScreenWidth, globals.ScreenHeight))
    
    while True:
        Play(screen)
 
def Play(surface) -> None:
    GameState = 1
    ResetGlobals()

    startTime = time.time()

    smallFont = pygame.font.SysFont(None, 24)
    mediumFont = pygame.font.SysFont(None, 32)
    largeFont = pygame.font.SysFont(None, 48)

    pygame.mixer.music.load("Sound/Banger.mp3")
    pygame.mixer.music.play()

    santa = gameobjects.Santa()
    snowFlakes = gameobjects.FlakeCollection(globals.SnowflakesMinAmount, globals.SnowflakesMaxAmount)
    projectiles = gameobjects.ProjectileCollection()

    snowFlakes.Debug()

    inputMovement = 0
    while True:
        displayUpdated = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("Game Reset")
                    return True
                if GameState == 1:
                    if event.key == pygame.K_1:
                        globals.Disco = not globals.Disco
                        print(f"Disco:              {globals.Disco}")
                    if event.key == pygame.K_2:
                        globals.DisplayColliders = not globals.DisplayColliders
                        print(f"DisplayColliders:   {globals.DisplayColliders}")
                    if event.key == pygame.K_3:
                        globals.FreezePhysics = not globals.FreezePhysics
                        print(f"FreezePhysics:      {globals.FreezePhysics}")
                    if event.key == pygame.K_4:
                        globals.DetectCollisions = not globals.DetectCollisions
                        print(f"DetectCollisions:   {globals.DetectCollisions}")
                    if event.key == pygame.K_SPACE:
                        if len(projectiles.List) < globals.MaxNumOfProjectiles:
                            projectiles.Add(santa.Pos)
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Sound/Blast.mp3"))
            
            if GameState == 1:
                if not globals.FreezePhysics and event.type == pygame.USEREVENT + 1:
                    snowFlakes.UpdatePositions()
                    projectiles.UpdatePositions()
                    
                    displayUpdated = True
                if event.type == pygame.USEREVENT + 2:
                    santa.Move(inputMovement)
                    inputMovement = 0
                    displayUpdated = True
        
        if GameState == 1:
            inputMovement = PosChangeFromInput()
            if displayUpdated:
                surface.fill(globals.ColorBackground)
                santa.Draw(surface)
                snowFlakes.Draw(surface)
                projectiles.Draw(surface)

                DrawTimer(surface, smallFont, startTime, globals.ColorSnow)
                pygame.display.update()

                GameState = 2 if globals.DetectCollisions and santa.GetRect().collidelist(snowFlakes.GetRects()) > 0 else GameState

                projectiles.List, snowFlakes.List = DetectLaserCollision(projectiles, snowFlakes)

        elif GameState == 2:
            pygame.mixer.music.load("Sound/EndScreen.mp3")
            pygame.mixer.music.play()

            DrawEndScreenGraphics(surface, [smallFont, mediumFont, largeFont], startTime)

            pygame.display.flip()
            GameState = 0 

def DetectLaserCollision(projectileArray, snowArray) -> tuple:
    collidedFlakes, collidedProjectiles = [], []

    for i in range(len(projectileArray.List)):
        temp = projectileArray.List[i].GetRect().collidelistall(snowArray.GetRects())
        if temp:
            collidedFlakes += temp
            collidedProjectiles += [i]

    snowArray.List = list(map(lambda x: gameobjects.Flake() if snowArray.List.index(x) in collidedFlakes else x, snowArray.List))
    projectileArray.List = list(filter(lambda x: not projectileArray.List.index(x) in collidedProjectiles, projectileArray.List))
    
    return projectileArray.List, snowArray.List

def ResetGlobals() -> None:
    globals.Disco               = False
    globals.DisplayColliders    = False
    globals.DetectCollisions    = True
    globals.FreezePhysics       = False

def DrawTimer(surface, font, timeElapsed, color) -> None:
    surface.blit(font.render(f"{(time.time() - timeElapsed):.1f} s", True, color), (16, 16))

def DrawEndScreenGraphics(surface, fonts, timeElapsed) -> None:
    surface.blit(pygame.image.load("Textures/EndScreen.jpeg"), (0, 0, globals.ScreenWidth, globals.ScreenHeight))
    
    DrawTimer(surface, fonts[0], timeElapsed, globals.ColorBackground)

    tryAgain = fonts[1].render(f"Press [R] to try again", True, globals.ColorBackground)
    surface.blit(tryAgain, (globals.ScreenWidth / 2 - (tryAgain.get_width() / 2), globals.ScreenHeight / 2))

    scoreImage = fonts[2].render(f"YOU DIED", True, globals.ColorSanta)
    surface.blit(scoreImage, (globals.ScreenWidth / 2 - (scoreImage.get_width() / 2), globals.ScreenHeight / 3))

def PosChangeFromInput() -> int:
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_RIGHT]:
        return 1
    elif pressedKeys[pygame.K_LEFT]:
        return -1
    
    return 0

main()