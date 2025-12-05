"""
Reconocimiento de voz con SpeechRecognition (micro o archivo).
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import speech_recognition as sr

from python.mediapipe_voice.utils import load_config
from python.detection.scripts.inference import WebSocketPublisher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconoce comandos de voz y los emite al WS.")
    parser.add_argument("--config", type=Path, help="Archivo YAML con parámetros.")
    parser.add_argument("--audio-file", type=Path, help="Archivo WAV para pruebas.")
    parser.add_argument("--ws-url", type=str, help="WebSocket destino (usa 'none' para desactivar).")
    parser.add_argument("--phrase-time-limit", type=int, default=5, help="Límite de grabación en segundos.")
    parser.add_argument("--mic-device-index", type=int, help="Índice del micrófono (opcional).")
    return parser.parse_args()


def normalize_command(text: str, mapping: dict[str, str]) -> str | None:
    normalized = text.lower().strip()
    for phrase, action in mapping.items():
        if phrase in normalized:
            return action
    return None


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    ws_url = args.ws_url if args.ws_url is not None else cfg.get("ws_url")
    if ws_url and ws_url.lower() == "none":
        ws_url = None
    mapping = cfg["voice"].get("commands", {})

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = cfg["voice"].get("energy_threshold", 300)
    recognizer.pause_threshold = cfg["voice"].get("pause_threshold", 0.8)

    def emit(text: str):
        command = normalize_command(text, mapping)
        message = {
            "timestamp": time.time(),
            "module": "multimodal",
            "type": "command" if command else "voice_raw",
            "payload": {
                "transcript": text,
                "action": command,
                "confidence": 0.8 if command else 0.0,
                "source": "voice",
            },
        }
        return message

    with WebSocketPublisher(ws_url) as publisher:
        if args.audio_file:
            with sr.AudioFile(str(args.audio_file)) as source:
                audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"[voice] Archivo {args.audio_file.name}: \"{text}\"")
                publisher.publish(emit(text))
            except sr.UnknownValueError:
                print(f"[voice] No se pudo reconocer el audio {args.audio_file}")
            except sr.RequestError as exc:
                print(f"[voice] Error del servicio de reconocimiento: {exc}")
        else:
            mic_kwargs = {}
            if args.mic_device_index is not None:
                mic_kwargs["device_index"] = args.mic_device_index
            with sr.Microphone(**mic_kwargs) as source:
                print("[voice] Di un comando (Ctrl+C para salir)...")
                while True:
                    audio = recognizer.listen(source, phrase_time_limit=args.phrase_time_limit)
                    try:
                        text = recognizer.recognize_google(audio, language="en-US")
                        print(f"[voice] Reconocido: {text}")
                        publisher.publish(emit(text))
                    except sr.UnknownValueError:
                        print("[voice] No se entendió el audio.")
                    except sr.RequestError as exc:
                        print(f"[voice] Error en el servicio de reconocimiento: {exc}")


if __name__ == "__main__":
    main()

