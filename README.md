# I2S Microphone Recorder Example

This project demonstrates how to use the STM32 I2S peripheral in DMA mode to acquire audio data from an INMP441 digital MEMS microphone and stream it over UART.

The I2S protocol is a kind of straight forward. At this point you might already found docs like [this](https://www.nxp.com/docs/en/user-manual/UM11732.pdf) or [that](https://www.st.com/resource/en/application_note/an4309-interfacing-an-stm32l1xx-microcontroller-with-an-external-i2s-audio-codec-to-play-audio-files-stmicroelectronics.pdf). But perhaps you haven't come across simple examples, just complete applications where you have to dig deep to find out how the heck they made the I2S work on an STM32. That's why I created this repo. Hope it helps.

## Features
- I2S audio acquisition from INMP441 MEMS microphone
- DMA-based data transfer for efficient sampling
- UART streaming of audio samples to a host PC (460800 baudrate)
- Start/stop recording with a user button (B1)
- Status LED (LD2) indicates recording state
- STM32CubeIDE and STM32CubeMX projects (so you can see all the configs you need)

## Hardware Requirements
- STM32F3 series microcontroller (tested on STM32F303RE)
- INMP441 MEMS microphone (I2S interface)
- UART connection to host PC
- User button (B1)
- Status LED (LD2)

<p align="center">
<img src="https://drive.google.com/uc?export=view&id=1k-mYVQVk2T5NjttuTqAW95a4pcD9Cpar" width="500">
<p>

## How It Works
1. **Initialization:**
   - I2S and UART peripherals are configured.
   - The system waits in an idle loop.
2. **Start/Stop Recording:**
   - Press the user button (B1) to start or stop audio acquisition.
   - The status LED (LD2) lights up when recording is active.
3. **Data Acquisition:**
   - Audio samples are acquired from the INMP441 via I2S using DMA.
   - Each received stereo sample is sent over UART in a simple binary format.

## UART Output Format
Each audio frame sent over UART consists of:
- Left Chan Low byte
- Left Chan Mid byte
- Left Chan High byte
- Newline character (`\n`)

## Usage
1. Connect the INMP441 microphone to the STM32 I2S pins.
2. Connect UART2 to your host PC and open a serial terminal.
3. Flash the firmware to your STM32 board.
4. Press the user button (B1) to start/stop recording.
5. Observe the status LED and monitor the UART output for audio data.

## File Overview

- `Src/serial_mic_recorder.c`: Main logic for I2S acquisition and UART streaming.
- `Inc/serial_mic_recorder.h`: Function prototypes.
- `I2S_Mic.ioc`: STM32CubeMX project configuration.

## Recording and Saving Audio to WAV

You can use `serial_to_wav.py` to record the audio data sent over UART and save it as a 24-bit mono WAV file on your PC.

```sh
python serial_to_wav.py --port COM12 --rate 8000 --output output.wav
```

The script will wait you for pressing the B1 button and then you will see "Mic acquisition: START" and record all incoming audio samples, and stop when you press the button again. The samples are then saved to the specified WAV file.
