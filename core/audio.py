from pygame.mixer import Sound, init

init()

sounds = {
    'win': Sound('audio/sounds/win.ogg'),
    'loss': Sound('audio/sounds/loss.ogg'),
    'crash': Sound('audio/sounds/crash.ogg'),
    'get coin': Sound('audio/sounds/get_coin.ogg'),
    'get coins': Sound('audio/sounds/get_coins.ogg'),
}
