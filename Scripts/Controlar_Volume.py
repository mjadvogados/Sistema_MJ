import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_controller():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume(volume_controller):
    return volume_controller.GetMasterVolumeLevelScalar()

def set_volume(volume_controller, level):
    volume_controller.SetMasterVolumeLevelScalar(level, None)

def main():
    volume = get_volume_controller()

    # 🔊 Salva volume atual
    original_volume = get_current_volume(volume)
    print(f"Volume atual: {original_volume * 100:.0f}%")

    # 🔊 Define volume para 80%
    set_volume(volume, 0.2)
    print("Volume ajustado para 80%")

    # ⏳ Aguarda 10 segundos
    time.sleep(10)

    # 🔙 Retorna ao volume original
    set_volume(volume, original_volume)
    print(f"Volume restaurado para {original_volume * 100:.0f}%")

if __name__ == "__main__":
    main()
