import globals

import pygame
import random

class Vector2D:
    def __init__(self, x, y) -> None:
        self.X = x
        self.Y = y

    def __str__(self):
        return f"X:{self.X}, Y:{self.Y}"

    def Clone(self):
        return Vector2D(self.X, self.Y)

    def ToTuple(self):
        return (self.X, self.Y)

class Flake:
    def __init__(self, init = False) -> None:
        self.Pos = Vector2D(random.randrange(0, globals.ScreenWidth), 
                            random.randrange(0, globals.ScreenHeight / 1.5) if init else 0)
        self.Size = random.randrange(3, 6)
        self.Color = globals.ColorSnow if not globals.Disco else (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.Valid = True
    
    def Debug (self) -> None:
        print(f"Pos:      {self.Pos}")
        print(f"Size:     {self.Size}")
        print(f"Validity: {self.Valid}")

    def GetRect(self) -> pygame.Rect:
        return pygame.Rect(self.Pos.X - self.Size, self.Pos.Y - self.Size, self.Size * 2, self.Size * 2)

    def Move (self) -> None:
        self.Pos = Vector2D(self.Pos.X + random.randint(-1, 1) if random.randint(0, 100) > 98 else self.Pos.X, 
                            self.Pos.Y + (2 if self.Size == 5 and random.randint(0, 100) > 80 else 1))
                  
    def Draw (self, surface) -> None:    
        if self.Valid:
            pygame.draw.circle(surface, self.Color, self.Pos.ToTuple(), self.Size)
            if globals.DisplayColliders: 
                pygame.draw.rect(surface, globals.ColorCollider, self.GetRect())

    def IsValid (self) -> bool:
        if ((self.Pos.X < 0 or self.Pos.X > globals.ScreenWidth)
            or (self.Pos.Y < 0 or self.Pos.Y > globals.ScreenHeight)):
            return False
        else:
            return True

class FlakeCollection:
    def __init__(self, minCount, maxCount) -> None:
        self.List = [Flake(True) for i in range(0, random.randint(minCount, maxCount))]

    def Debug(self) -> None:
        for i in self.List:
            print()
            i.Debug()

    def GetRects(self) -> list[pygame.Rect]:
        return [item.GetRect() for item in self.List]

    def UpdatePositions(self) -> None:
        for i in range(0, len(self.List)):
            self.List[i].Move()
            if not self.List[i].IsValid():
                self.List[i] = Flake()

    def Draw(self, surface) -> None:
        for item in self.List:
            item.Draw(surface)

class Projectile:
    def __init__(self, pos) -> None:
        self.Size = Vector2D(5, 10)
        self.Pos = Vector2D(pos.X - self.Size.X // 2, pos.Y)
        self.Color = (0, 255, 0)
        self.Valid = True
        self.Speed = 1
    
    def Debug(self) -> None:
        print(f"Pos:      {self.Pos}")
        print(f"Size:     {self.Size}")
        print(f"Validity: {self.Valid}")
        print(f"Speed:    {self.Speed}")

    def GetRect(self) -> tuple:
        return pygame.Rect(self.Pos.X, self.Pos.Y, self.Size.X, self.Size.Y)

    def Draw (self, surface) -> None:    
        if self.Valid:
            pygame.draw.rect(surface, self.Color, self.GetRect())
            if globals.DisplayColliders: 
                pygame.draw.rect(surface, globals.ColorCollider, self.GetRect())

    def ClampCoordinates(self) -> None:
        if self.Pos.Y < 0:
            self.Valid = False

    def Move(self, amount):
        self.Pos.Y -= amount
        self.ClampCoordinates()

class ProjectileCollection:
    def __init__(self) -> None:
        self.List = []

    def Debug(self) -> None:
        for i in self.List:
            print()
            i.Debug()

    def GetRects(self) -> list[pygame.Rect]:
        return [item.GetRect() for item in self.List]

    def UpdatePositions(self) -> None:
        for i in range(0, len(self.List)):
            self.List[i].Move(1)

        self.List = list(filter(lambda x: x.Valid, self.List))
        
    def Draw(self, surface) -> None:
        for i in self.List:
            i.Draw(surface)

    def TryAdd(self, pos) -> None: 
        if len(self.List) < globals.MaxNumOfProjectiles:
            self.List.append(Projectile(pos))

class Santa:
    def __init__(self) -> None:
        self.Size = Vector2D(globals.SantaWidth, globals.SantaWidth)
        self.Pos = Vector2D(globals.ScreenWidth // 2, (globals.ScreenHeight * 0.975) - (self.Size.Y / 2))
    
    def Debug(self) -> None:
        print(f"Pos:      {self.Pos}")
        print(f"Size:     {self.Size}")

    def GetRect(self) -> pygame.Rect:
        return pygame.Rect(self.Pos.X - (self.Size.X // 2), self.Pos.Y, self.Size.X, self.Size.Y)

    def Draw(self, surface) -> None:
        pygame.draw.rect(surface, globals.ColorSanta, self.GetRect(), border_radius = 4)
        if globals.DisplayColliders: 
            pygame.draw.rect(surface, globals.ColorCollider, self.GetRect())

    def ClampCoordinates(self) -> None:
        if(self.Pos.X - (self.Size.X // 2) < 0):
            self.Pos.X = self.Size.X // 2
        elif(self.Pos.X + (self.Size.X // 2) > globals.ScreenWidth):
            self.Pos.X = globals.ScreenWidth - (self.Size.X // 2)

    def Move(self, amount):
        self.Pos.X += amount
        self.ClampCoordinates()