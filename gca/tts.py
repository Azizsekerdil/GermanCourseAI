from __future__ import annotations

import subprocess
import threading

from . import config as C


class Speaker:
    def __init__(self, rate: int = 155):
        self.rate = rate

    def speak(self, text: str) -> None:
        if not text:
            return
        threading.Thread(target=self._run, args=(text,), daemon=True).start()

    def _run(self, text: str) -> None:
        escaped = text.replace("'", "''")
        script = ("Add-Type -AssemblyName System.Speech; "
                  "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                  f"$s.Rate={max(-10, min(10, round((self.rate-150)/20)))}; "
                  "$v=$s.GetInstalledVoices() | Where-Object {$_.VoiceInfo.Culture.Name -like 'de-*'} | Select-Object -First 1; "
                  "if($v){$s.SelectVoice($v.VoiceInfo.Name)}; "
                  f"$s.Speak('{escaped}')")
        try:
            subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                           check=False, capture_output=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except OSError:
            pass

    def info(self) -> str:
        return "Windows System.Speech (de-DE when installed)"
