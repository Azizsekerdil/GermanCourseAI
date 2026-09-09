from __future__ import annotations

import subprocess
import sys
import threading

from . import config as C

MACOS_VOICE = "Anna"                 # voice used by the macOS `say` command


class Speaker:
    def __init__(self, rate: int = 155):
        self.rate = rate

    def speak(self, text: str) -> None:
        if not text:
            return
        threading.Thread(target=self._run, args=(text,), daemon=True).start()

    def _run(self, text: str) -> None:
        if sys.platform == "darwin": return self._run_macos(text)
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

    def _run_macos(self, text: str) -> None:
        # A language voice is an optional download on macOS, but `say` substitutes the system
        # voice on its own, so only a missing or unusable `say` binary is guarded here.
        try:
            subprocess.run(["/usr/bin/say", "-v", MACOS_VOICE, "-r", str(self.rate)],
                           input=text, text=True, check=False, capture_output=True)
        except OSError:
            pass

    def info(self) -> str:
        if sys.platform == "darwin": return f"macOS say ({MACOS_VOICE})"
        return "Windows System.Speech (de-DE when installed)"
