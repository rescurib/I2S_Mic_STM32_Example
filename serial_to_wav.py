#!/usr/bin/env python3
"""
UART to WAV Recorder for STM32 Audio Streaming

This script listens to a serial port for audio data streamed from an STM32 microcontroller and saves it as a 24-bit mono WAV file.

Usage:
    python serial_to_wav.py [--port COM_PORT] [--rate SAMPLE_RATE] [--output OUTPUT_FILE]

Arguments:
    --port      Serial COM port to listen to (default: COM12)
    --rate      Sample rate in Hz for the WAV file (default: 8000)
    --output    Output WAV file name (default: output.wav)

Example:
    python serial_to_wav.py --port COM3 --rate 16000 --output my_audio.wav

"""
import argparse
import serial
import wave

DEFAULT_COM_PORT = 'COM12'
DEFAULT_SAMPLE_RATE = 8000
DEFAULT_WAV_FILE = 'output.wav'

# Windows: use "mode" to see available COM ports
# Linux: use "ls /dev/tty*"

def parse_args():
    parser = argparse.ArgumentParser(description='UART to WAV recorder for STM32 audio streaming')
    parser.add_argument('--port', type=str, default=DEFAULT_COM_PORT, help='Serial COM port (default: COM3)')
    parser.add_argument('--rate', type=int, default=DEFAULT_SAMPLE_RATE, help='Sample rate in Hz (default: 8000)')
    parser.add_argument('--output', type=str, default=DEFAULT_WAV_FILE, help='Output WAV file name (default: output.wav)')
    return parser.parse_args()


def main():
    args = parse_args()
    ser = serial.Serial(args.port, baudrate=460800, timeout=1)
    print('Listening on {}...'.format(args.port))
    samples = []
    streaming = False
    buffer = b''
    while True:
        byte = ser.read(1)
        if not byte:
            continue
        buffer += byte
        # Only check for text commands if not streaming
        if not streaming and b'\n' in buffer:
            try:
                text = buffer.decode(errors='ignore').strip()
            except Exception:
                buffer = b''
                continue
            if text == 'Mic acquisition: START':
                print('Mic acquisition: START')
                streaming = True
                buffer = b''
                continue
            buffer = b''
            continue
        
        if streaming:
            if buffer == b"Mic acquisition: STOP\r\n":
                print('Mic acquisition: STOP')
                break
            #Process 3 bytes + newline
            if len(buffer) == 4 and buffer[3] == ord('\n'):
              raw = buffer[:3][::-1]  # little-endian PCM
              samples.append(raw)
              buffer = b''
    ser.close()
    if samples:
        print('Saving {} samples to {}'.format(len(samples), args.output))
        with wave.open(args.output, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(3)  # 24-bit
            wf.setframerate(args.rate)
            # Write samples as signed 24-bit little endian
            for s in samples:
                wf.writeframesraw(s)
        print('WAV file saved.')
    else:
        print('No samples received.')

if __name__ == '__main__':
    main()
