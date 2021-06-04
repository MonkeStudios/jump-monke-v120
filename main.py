@namespace
class SpriteKind:
    Bumper = SpriteKind.create()
    Goal = SpriteKind.create()
    Coin = SpriteKind.create()
    Flier = SpriteKind.create()
    Energy = SpriteKind.create()

def on_on_overlap(sprite, otherSprite):
    if sprite.vy > 0 and not (sprite.is_hitting_tile(CollisionDirection.BOTTOM)) or sprite.y < otherSprite.top:
        otherSprite.destroy(effects.ashes, 250)
        otherSprite.vy = -50
        sprite.vy = -2 * pixelsToMeters
        info.change_score_by(1)
        music.power_up.play()
    else:
        info.change_life_by(-1)
        sprite.say("Ow!", invincibilityPeriod)
        music.power_down.play()
    pause(invincibilityPeriod)
sprites.on_overlap(SpriteKind.player, SpriteKind.Bumper, on_on_overlap)

def on_overlap_tile(sprite, location):
    global jumpHeight, doubleJump1, doubleJump2, canLaunch, currentLevel
    jumpHeight = -4
    doubleJump1 = -3
    doubleJump2 = -4.5
    canLaunch = 0
    currentLevel += 7
    game.splash("Good Luck! You're going to the last level")
    setLevelTileMap(currentLevel)
    info.change_life_by(7)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile1
    """),
    on_overlap_tile)

def initializeAnimations():
    initializeCoinAnimation()
    initializeFlierAnimations()
def giveIntroduction():
    global startTime
    game.set_dialog_frame(img("""
        . 2 2 2 2 2 2 2 2 2 2 2 2 2 . . 
                2 2 1 1 1 1 1 1 1 1 1 1 1 2 2 . 
                2 1 1 2 2 2 2 2 2 2 2 2 1 1 2 . 
                2 1 2 2 1 1 1 1 1 1 1 2 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 1 1 1 1 1 1 1 1 1 2 1 2 . 
                2 1 2 2 1 1 1 1 1 1 1 2 2 1 2 . 
                2 1 1 2 2 2 2 2 2 2 2 2 1 1 2 . 
                2 2 1 1 1 1 1 1 1 1 1 1 1 2 2 . 
                . 2 2 2 2 2 2 2 2 2 2 2 2 2 . . 
                . . . . . . . . . . . . . . . .
    """))
    game.set_dialog_cursor(img("""
        . . . . . . . . . . . . . . . . 
                . . . . . . . . . . . . . . . . 
                . . . . . . . . . . . . . . . . 
                . . . . . . f f f f . . . . . . 
                . . . . f f 5 5 5 5 f f . . . . 
                . . . . f 5 5 5 5 5 5 f . . . . 
                . . . f 5 5 5 4 4 5 5 5 f . . . 
                . . . f 5 5 5 4 4 5 5 5 f . . . 
                . . . f 5 5 5 4 4 5 5 5 f . . . 
                . . . f 5 5 5 4 4 5 5 5 f . . . 
                . . . . f 5 5 5 5 5 5 f . . . . 
                . . . . f f 5 5 5 5 f f . . . . 
                . . . . . . f f f f . . . . . . 
                . . . . . . . . . . . . . . . . 
                . . . . . . . . . . . . . . . . 
                . . . . . . . . . . . . . . . .
    """))
    showInstruction("Move with the left and right buttons.")
    showInstruction("Jump with the up or A button.")
    showInstruction("Double jump by pressing jump again.")
    startTime = game.runtime()

def on_up_pressed():
    attemptJump()
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def initializeCoinAnimation():
    pass

def on_on_overlap2(sprite, otherSprite):
    otherSprite.destroy(effects.trail, 250)
    otherSprite.y += -3
    info.change_score_by(3)
    music.ba_ding.play()
sprites.on_overlap(SpriteKind.player, SpriteKind.Coin, on_on_overlap2)

def attemptJump():
    global doubleJumpSpeed, canDoubleJump
    # else if: either fell off a ledge, or double jumping
    if hero.is_hitting_tile(CollisionDirection.BOTTOM):
        hero.vy = jumpHeight * pixelsToMeters
    elif canDoubleJump:
        doubleJumpSpeed = doubleJump1 * pixelsToMeters
        # Good double jump
        if hero.vy >= -40:
            doubleJumpSpeed = doubleJump2 * pixelsToMeters
            hero.start_effect(effects.trail, 500)
            scene.camera_shake(2, 250)
        hero.vy = doubleJumpSpeed
        canDoubleJump = False

def on_b_pressed():
    global projectile
    projectile = sprites.create_projectile_from_sprite(img("""
            . . . . . . . . . c c 8 . . . . 
                    . . . . . . 8 c c c f 8 c c . . 
                    . . . c c 8 8 f c a f f f c c . 
                    . . c c c f f f c a a f f c c c 
                    8 c c c f f f f c c a a c 8 c c 
                    c c c b f f f 8 a c c a a a c c 
                    c a a b b 8 a b c c c c c c c c 
                    a f c a a b b a c c c c c f f c 
                    a 8 f c a a c c a c a c f f f c 
                    c a 8 a a c c c c a a f f f 8 a 
                    . a c a a c f f a a b 8 f f c a 
                    . . c c b a f f f a b b c c 6 c 
                    . . . c b b a f f 6 6 a b 6 c . 
                    . . . c c b b b 6 6 a c c c c . 
                    . . . . c c a b b c c c . . . . 
                    . . . . . c c c c c c . . . . .
        """),
        hero,
        60,
        0)
    hero.vy = -2 * pixelsToMeters
    music.rest(music.beat(BeatFraction.WHOLE))
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def setLevelTileMap(level: number):
    clearGame()
    if level == 0:
        tiles.set_tilemap(tilemap("""
            level
        """))
    elif level == 1:
        tiles.set_tilemap(tilemap("""
            level_0
        """))
    elif level == 2:
        tiles.set_tilemap(tilemap("""
            level_1
        """))
    elif level == 3:
        tiles.set_tilemap(tilemap("""
            level_2
        """))
    elif level == 4:
        tiles.set_tilemap(tilemap("""
            level_3
        """))
    elif level == 5:
        tiles.set_tilemap(tilemap("""
            level_4
        """))
    elif level == 6:
        tiles.set_tilemap(tilemap("""
            level_5
        """))
    elif level == 7:
        tiles.set_tilemap(tilemap("""
            level_6
        """))
    initializeLevel(level)
def initializeFlierAnimations():
    pass

def on_a_pressed():
    attemptJump()
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def animateCrouch():
    pass
def clearGame():
    for value in sprites.all_of_kind(SpriteKind.Bumper):
        value.destroy()
    for value2 in sprites.all_of_kind(SpriteKind.Coin):
        value2.destroy()
    for value3 in sprites.all_of_kind(SpriteKind.Goal):
        value3.destroy()
    for value4 in sprites.all_of_kind(SpriteKind.Flier):
        value4.destroy()
    for value5 in sprites.all_of_kind(SpriteKind.Energy):
        value5.destroy()

def on_overlap_tile2(sprite, location):
    global jumpHeight, doubleJump1, doubleJump2, canLaunch, currentLevel, elasped
    jumpHeight = -4
    doubleJump1 = -3
    doubleJump2 = -4.5
    canLaunch = 0
    info.change_life_by(1)
    currentLevel += 1
    if hasNextLevel():
        game.splash("Next level unlocked!")
        setLevelTileMap(currentLevel)
    else:
        elasped = game.runtime() - startTime
        game.splash("Your time was...")
        game.splash(str(elasped))
        game.over(True, effects.confetti)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        tile1
    """),
    on_overlap_tile2)

def on_on_overlap3(sprite, otherSprite):
    info.change_life_by(-1)
    sprite.say("Ow!", invincibilityPeriod * 1.5)
    music.power_down.play()
    pause(invincibilityPeriod * 1.5)
sprites.on_overlap(SpriteKind.player, SpriteKind.Flier, on_on_overlap3)

def createEnemies():
    global bumper, engery
    # enemy that moves back and forth
    for value6 in tiles.get_tiles_by_type(assets.tile("""
        tile4
    """)):
        bumper = sprites.create(assets.image("""
            myImage0
        """), SpriteKind.Bumper)
        tiles.place_on_tile(bumper, value6)
        tiles.set_tile_at(value6, assets.tile("""
            tile0
        """))
        bumper.ay = gravity
        if Math.percent_chance(50):
            bumper.vx = Math.random_range(30, 60)
        else:
            bumper.vx = Math.random_range(-60, -30)
    # enemy that flies at player
    for value7 in tiles.get_tiles_by_type(assets.tile("""
        tile7
    """)):
        engery = sprites.create(assets.image("""
            myImage1
        """), SpriteKind.Flier)
        tiles.place_on_tile(engery, value7)
        tiles.set_tile_at(value7, assets.tile("""
            tile0
        """))
    # enemy that flies at player
    for value8 in tiles.get_tiles_by_type(assets.tile("""
        myTile0
    """)):
        engery = sprites.create(assets.image("""
            myImage
        """), SpriteKind.Energy)
        tiles.place_on_tile(engery, value8)
        tiles.set_tile_at(value8, assets.tile("""
            tile0
        """))

def on_down_pressed():
    if not (hero.is_hitting_tile(CollisionDirection.BOTTOM)):
        hero.vy += 80
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def showInstruction(text: str):
    game.show_long_text(text, DialogLayout.BOTTOM)
    music.ba_ding.play()
    info.change_score_by(1)

def on_on_overlap4(sprite, otherSprite):
    global canLaunch, jumpHeight, doubleJump1, doubleJump2
    otherSprite.destroy(effects.halo, 500)
    canLaunch = 1
    jumpHeight = -5
    doubleJump1 = -4
    doubleJump2 = -5.5
sprites.on_overlap(SpriteKind.player, SpriteKind.Energy, on_on_overlap4)

def createPlayer(player2: Sprite):
    player2.ay = gravity
    scene.camera_follow_sprite(player2)
    controller.move_sprite(player2, 100, 0)
    player2.z = 5
    info.set_life(3)
    info.set_score(0)
def initializeLevel(level: number):
    global playerStartLocation
    effects.clouds.start_screen_effect()
    playerStartLocation = tiles.get_tiles_by_type(assets.tile("""
        tile6
    """))[0]
    tiles.place_on_tile(hero, playerStartLocation)
    tiles.set_tile_at(playerStartLocation, assets.tile("""
        tile0
    """))
    createEnemies()
    spawnGoals()

def on_on_overlap5(sprite, otherSprite):
    otherSprite.destroy(effects.spray, 500)
    sprite.destroy(effects.spray, 500)
    info.change_score_by(5)
sprites.on_overlap(SpriteKind.projectile, SpriteKind.Flier, on_on_overlap5)

def hasNextLevel():
    return currentLevel != levelCount
def spawnGoals():
    global coin
    for value82 in tiles.get_tiles_by_type(assets.tile("""
        tile5
    """)):
        coin = sprites.create(img("""
                . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . f f f f . . . . . . 
                            . . . . f f 5 5 5 5 f f . . . . 
                            . . . . f 5 5 5 5 5 5 f . . . . 
                            . . . f 5 5 5 4 4 5 5 5 f . . . 
                            . . . f 5 5 5 4 4 5 5 5 f . . . 
                            . . . f 5 5 5 4 4 5 5 5 f . . . 
                            . . . f 5 5 5 4 4 5 5 5 f . . . 
                            . . . . f 5 5 5 5 5 5 f . . . . 
                            . . . . f f 5 5 5 5 f f . . . . 
                            . . . . . . f f f f . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . .
            """),
            SpriteKind.Coin)
        tiles.place_on_tile(coin, value82)
        tiles.set_tile_at(value82, assets.tile("""
            tile0
        """))
heroFacingLeft = False
coin: Sprite = None
playerStartLocation: tiles.Location = None
engery: Sprite = None
bumper: Sprite = None
elasped = 0
projectile: Sprite = None
doubleJumpSpeed = 0
canDoubleJump = False
startTime = 0
doubleJump2 = 0
doubleJump1 = 0
jumpHeight = 0
canLaunch = 0
currentLevel = 0
levelCount = 0
gravity = 0
pixelsToMeters = 0
invincibilityPeriod = 0
hero: Sprite = None
hero = sprites.create(img("""
        . . . . f f f f f . . . . . . . 
            . . . f e e e e e f . . . . . . 
            . . f d d d d e e e f . . . . . 
            . c d f d d f d e e f f . . . . 
            . c d f d d f d e e d d f . . . 
            c d e e d d d d e e b d c . . . 
            c d d d d c d d e e b d c . . . 
            c c c c c d d e e e f c . . . . 
            . f d d d d e e e f f . . . . . 
            . . f f f f f e e e e f . . . . 
            . . . . f f e e e e e e f . f f 
            . . . f e e f e e f e e f . e f 
            . . f e e f e e f e e e f . e f 
            . f b d f d b f b b f e f f e f 
            . f d d f d d f d d b e f f f f 
            . . f f f f f f f f f f f f f .
    """),
    SpriteKind.player)
# how long to pause between each contact with a
# single enemy
invincibilityPeriod = 600
pixelsToMeters = 30
gravity = 9.81 * pixelsToMeters
scene.set_background_image(img("""
    9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989998999899989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989998999899989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998999899989998999899989998999899989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        9989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989898999898989998989899989998999899989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999989999999899999998999999999999999999999999999999
        8989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989898989
        9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
"""))
initializeAnimations()
createPlayer(hero)
levelCount = 8
currentLevel = 0
setLevelTileMap(currentLevel)
giveIntroduction()
canLaunch = 0
jumpHeight = -4
doubleJump1 = -3
doubleJump2 = -4.5

def on_on_update():
    global canLaunch
    if canLaunch == 1 and (controller.A.is_pressed() and controller.B.is_pressed()):
        canLaunch = 0
        hero.vy = -10 * pixelsToMeters
game.on_update(on_on_update)

# set up hero animations

def on_on_update2():
    global heroFacingLeft
    if hero.vx < 0:
        heroFacingLeft = True
    elif hero.vx > 0:
        heroFacingLeft = False
    if hero.is_hitting_tile(CollisionDirection.TOP):
        hero.vy = 0
game.on_update(on_on_update2)

# Flier movement

def on_on_update3():
    for value9 in sprites.all_of_kind(SpriteKind.Flier):
        if abs(value9.x - hero.x) < 60:
            if value9.x - hero.x < -5:
                value9.vx = 25
            elif value9.x - hero.x > 5:
                value9.vx = -25
            if value9.y - hero.y < -5:
                value9.vy = 25
            elif value9.y - hero.y > 5:
                value9.vy = -25
        else:
            value9.vy = -20
            value9.vx = 0
game.on_update(on_on_update3)

# Reset double jump when standing on wall

def on_on_update4():
    global canDoubleJump
    if hero.is_hitting_tile(CollisionDirection.BOTTOM):
        canDoubleJump = True
game.on_update(on_on_update4)

# bumper movement

def on_on_update5():
    for value10 in sprites.all_of_kind(SpriteKind.Bumper):
        if value10.is_hitting_tile(CollisionDirection.LEFT):
            value10.vx = Math.random_range(30, 60)
        elif value10.is_hitting_tile(CollisionDirection.RIGHT):
            value10.vx = Math.random_range(-60, -30)
game.on_update(on_on_update5)
