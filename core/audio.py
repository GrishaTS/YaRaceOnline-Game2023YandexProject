from pygame.mixer import Sound, init

init()

sounds = {
    'win': Sound('audio/sounds/win.ogg'),
    'loss': Sound('audio/sounds/loss.ogg'),
    'crash': Sound('audio/sounds/crash.ogg'),
    'get coin': Sound('audio/sounds/get_coin.ogg'),
    '321': Sound('audio/sounds/321.ogg'),
    'default_car': Sound('audio/sounds/default_car.ogg'),
    'overclocking': Sound('audio/sounds/overclocking.ogg')
}
