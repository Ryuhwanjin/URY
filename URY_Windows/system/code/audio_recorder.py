#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 URY Engine — 노트북 내장 실시간 오디오 녹음기 모듈 v2.0 (audio_recorder.py)
- macOS: 네이티브 AVFoundation mac_audio_rec 바이너리 활용 ➔ Apple AAC/M4A 100% 무설치 고음질 녹음
- Windows: sounddevice/PortAudio 직접 WAV 녹음 (외부 ffmpeg 불필요)
- 기타: ffmpeg / sox / wave fallback 녹음
- 녹음 완료 시 오늘 날짜 해당 과목 '음성녹음' 폴더에 자동 안착
"""

import os
import sys
import time
import re
import subprocess
import signal
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import config_manager


def find_mac_recorder_bin():
    """macOS native recorder(mac_audio_rec)를 앱/소스 경로에서 탐색."""

    candidates = []

    # PyInstaller .app
    if getattr(sys, "executable", None):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))

        candidates.extend([
            os.path.abspath(
                os.path.join(
                    exe_dir,
                    "..",
                    "Resources",
                    "bin",
                    "mac_audio_rec"
                )
            ),
            os.path.abspath(
                os.path.join(
                    exe_dir,
                    "..",
                    "..",
                    "Resources",
                    "bin",
                    "mac_audio_rec"
                )
            ),
        ])

    # PyInstaller 임시 경로
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(
            os.path.join(meipass, "bin", "mac_audio_rec")
        )

    # 소스 실행 환경
    candidates.extend([
        os.path.abspath(
            os.path.join(
                SCRIPT_DIR,
                "..",
                "bin",
                "mac_audio_rec"
            )
        ),
        os.path.join(
            SCRIPT_DIR,
            "mac_audio_rec"
        ),
    ])

    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


def build_recording_filename(rec_dir, date_str, course_name, ext):
    """날짜와 과목명이 드러나는 충돌 없는 녹음 파일명을 만든다."""
    try:
        date_str = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        date_str = datetime.now().strftime("%Y-%m-%d")
    safe_course = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", str(course_name)).strip(" ._") or "과목"
    prefix = f"{date_str}_{safe_course}_"
    session_num = 1 + sum(name.startswith(prefix) for name in os.listdir(rec_dir))
    return f"{prefix}{session_num}교시_실시간녹음.{ext}"


class AudioRecorder:
    def __init__(self):
        self.process = None
        self._stream = None
        self._wave_file = None
        self.output_file = None
        self.is_recording = False
        self.start_time = None

    def _start_windows_recording(self):
        import wave
        import sounddevice as sd

        device = sd.query_devices(kind="input")
        channels = min(2, int(device["max_input_channels"]))
        if channels < 1:
            raise RuntimeError("사용 가능한 Windows 마이크 입력 장치가 없습니다.")

        self._wave_file = wave.open(self.output_file, "wb")
        self._wave_file.setnchannels(channels)
        self._wave_file.setsampwidth(2)
        self._wave_file.setframerate(int(device["default_samplerate"]))

        def write_audio(indata, frames, timing, status):
            self._wave_file.writeframesraw(indata)

        self._stream = sd.RawInputStream(
            samplerate=int(device["default_samplerate"]),
            channels=channels,
            dtype="int16",
            callback=write_audio,
        )
        try:
            self._stream.start()
        except Exception:
            self._stream.close()
            self._stream = None
            self._wave_file.close()
            self._wave_file = None
            raise

    def _stop_windows_recording(self):
        stream, self._stream = self._stream, None
        wave_file, self._wave_file = self._wave_file, None
        try:
            if stream:
                stream.stop()
        finally:
            if stream:
                stream.close()
            if wave_file:
                wave_file.close()

    def start_recording(self, course_name_or_folder: str, lecture_date: str = None) -> dict:
        """녹음 시작: 과목 폴더에 YYYY-MM-DD_과목명_1교시_실시간녹음 형식으로 기록."""
        if self.is_recording:
            return {"status": "already_running", "message": "이미 녹음이 진행 중입니다."}

        # 과목명 -> 폴더명 확인
        folder_name = course_name_or_folder
        for c in config_manager.load_settings().get("courses", []):
            if c.get("course_name") == course_name_or_folder:
                folder_name = c.get("folder_name", course_name_or_folder)
                break

        course_dir = config_manager.get_course_dir(folder_name)
        rec_dir = os.path.join(course_dir, "음성녹음")
        os.makedirs(rec_dir, exist_ok=True)

        mac_bin = find_mac_recorder_bin()
        ext = "m4a" if (sys.platform == "darwin" and mac_bin) else "wav"
        filename = build_recording_filename(rec_dir, lecture_date, course_name_or_folder, ext)
        self.output_file = os.path.join(rec_dir, filename)

        try:
            if sys.platform == "darwin":
                if not mac_bin:
                    return {
                        "status": "error",
                        "message": (
                            "macOS native recorder(mac_audio_rec)를 찾을 수 없습니다. "
                            "앱 번들의 Contents/Resources/bin/mac_audio_rec를 확인해주세요."
                        )
                    }

                cmd = [mac_bin, self.output_file]
            elif sys.platform == "win32":
                self._start_windows_recording()
                self.is_recording = True
                self.start_time = time.time()
                print(f"🔴 [AudioRecorder] 실시간 마이크 녹음 시작: {self.output_file}")
                return {
                    "status": "success",
                    "output_file": self.output_file,
                    "file_name": filename
                }
            else:
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "dshow",
                    "-i",
                    "audio=Microphone",
                    self.output_file
                ]

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 프로세스 정상 구동 여부 즉각 확인 (0.2초 대기)
            time.sleep(0.2)
            exit_code = self.process.poll()
            if exit_code is not None:
                err_out = ""
                if self.process.stderr:
                    err_out = self.process.stderr.read()
                self.process = None
                self.is_recording = False
                return {
                    "status": "error",
                    "message": f"녹음기 프로세스 즉시 종료됨 (코드 {exit_code}):\n{err_out.strip()}"
                }

            self.is_recording = True
            self.start_time = time.time()

            print(f"🔴 [AudioRecorder] 실시간 마이크 녹음 시작: {self.output_file}")
            return {
                "status": "success",
                "output_file": self.output_file,
                "file_name": filename
            }

        except Exception as e:
            if self._stream or self._wave_file:
                try:
                    self._stop_windows_recording()
                except Exception:
                    pass
            self.is_recording = False
            self.process = None
            print(f"⚠️ 녹음 구동 오류: {e}")
            return {"status": "error", "message": str(e)}

    def stop_recording(self) -> dict:
        """녹음 중지 및 파일 정상 닫기"""
        if not self.is_recording or not (self.process or self._stream):
            return {"status": "not_running", "message": "녹음 중이 아닙니다."}

        try:
            if sys.platform == "win32" and self._stream:
                self._stop_windows_recording()
            elif sys.platform == "win32":
                self.process.terminate()
            else:
                self.process.send_signal(signal.SIGINT)

            if self.process:
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()

            duration_sec = int(time.time() - self.start_time) if self.start_time else 0
            self.is_recording = False
            out_file = self.output_file
            self.process = None

            file_size = os.path.getsize(out_file) if (out_file and os.path.exists(out_file)) else 0
            print(f"⏹️ [AudioRecorder] 녹음 완료 ({duration_sec}초 경과, {file_size} bytes): {out_file}")
            return {
                "status": "success",
                "output_file": out_file,
                "duration_sec": duration_sec,
                "file_size": file_size
            }
        except Exception as e:
            self.is_recording = False
            self.process = None
            return {"status": "error", "message": str(e)}


# 글로벌 싱글톤 인스턴스
recorder_instance = AudioRecorder()
