from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.signal import find_peaks


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

SPECTROGRAM_DIR = OUTPUT_DIR / "spectrograms"
SPECTRUM_DIR = OUTPUT_DIR / "spectra"
TABLE_DIR = OUTPUT_DIR / "tables"

for folder in [SPECTROGRAM_DIR, SPECTRUM_DIR, TABLE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


AUDIO_FILES = {
    "A": INPUT_DIR / "a_voice.wav",
    "I": INPUT_DIR / "i_voice.wav",
    "Imitation": INPUT_DIR / "imitation.wav",
}


def load_audio(path: Path):
    """Загрузка аудио в mono."""
    y, sr = librosa.load(path, sr=None, mono=True)

    # нормализация амплитуды
    max_abs = np.max(np.abs(y))
    if max_abs > 0:
        y = y / max_abs

    return y, sr


def save_waveform(y, sr, name):
    """Сохранение осциллограммы."""
    times = np.arange(len(y)) / sr

    plt.figure(figsize=(12, 4))
    plt.plot(times, y)
    plt.title(f"Waveform: {name}")
    plt.xlabel("Time, s")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(SPECTRUM_DIR / f"{name}_waveform.png", dpi=200)
    plt.close()


def save_spectrogram(y, sr, name):
    """Построение спектрограммы через STFT с окном Ханна."""
    n_fft = 2048
    hop_length = 512

    stft = librosa.stft(
        y,
        n_fft=n_fft,
        hop_length=hop_length,
        window="hann"
    )

    db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    plt.figure(figsize=(12, 6))
    librosa.display.specshow(
        db,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="log"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title(f"Spectrogram with Hann window: {name}")
    plt.xlabel("Time, s")
    plt.ylabel("Frequency, Hz, log scale")
    plt.tight_layout()
    plt.savefig(SPECTROGRAM_DIR / f"{name}_spectrogram.png", dpi=200)
    plt.close()

    return stft


def save_average_spectrum(y, sr, name):
    """Средний амплитудный спектр."""
    spectrum = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), d=1 / sr)

    # ограничим анализ речевым диапазоном
    mask = (freqs >= 50) & (freqs <= 5000)
    freqs = freqs[mask]
    spectrum = spectrum[mask]

    if np.max(spectrum) > 0:
        spectrum = spectrum / np.max(spectrum)

    plt.figure(figsize=(12, 5))
    plt.plot(freqs, spectrum)
    plt.title(f"Average spectrum: {name}")
    plt.xlabel("Frequency, Hz")
    plt.ylabel("Normalized amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(SPECTRUM_DIR / f"{name}_spectrum.png", dpi=200)
    plt.close()

    return freqs, spectrum


def estimate_voice_range(freqs, spectrum, threshold=0.08):
    """Приближённая минимальная и максимальная частота по энергии спектра."""
    active = spectrum > threshold

    if not np.any(active):
        return None, None

    active_freqs = freqs[active]
    return float(active_freqs[0]), float(active_freqs[-1])


def estimate_main_tone(freqs, spectrum):
    """
    Основной тон оценивается как самый сильный пик
    в диапазоне частоты человеческого голоса.
    """
    mask = (freqs >= 70) & (freqs <= 400)
    f = freqs[mask]
    s = spectrum[mask]

    if len(f) == 0:
        return None

    peaks, _ = find_peaks(s, distance=5)

    if len(peaks) == 0:
        return float(f[np.argmax(s)])

    strongest_peak = peaks[np.argmax(s[peaks])]
    return float(f[strongest_peak])


def estimate_formants(freqs, spectrum):
    """
    Приближённая оценка формант:
    ищем сильные пики спектральной энергии в речевом диапазоне.
    """
    mask = (freqs >= 200) & (freqs <= 3500)
    f = freqs[mask]
    s = spectrum[mask]

    if len(f) == 0:
        return [None, None, None]

    peaks, properties = find_peaks(
        s,
        distance=20,
        prominence=0.03
    )

    if len(peaks) == 0:
        return [None, None, None]

    # сортировка пиков по силе
    strongest = peaks[np.argsort(s[peaks])[-3:]]

    # сортировка формант по частоте
    formants = sorted(f[strongest])

    while len(formants) < 3:
        formants.append(None)

    return [float(x) if x is not None else None for x in formants[:3]]


def count_harmonics(freqs, spectrum, main_tone):
    """
    Оценка количества обертонов:
    считаем пики около кратных частот основного тона.
    """
    if main_tone is None or main_tone <= 0:
        return 0

    count = 0
    max_freq = 5000
    tolerance = 25

    for k in range(2, int(max_freq // main_tone) + 1):
        target = k * main_tone
        mask = (freqs >= target - tolerance) & (freqs <= target + tolerance)

        if np.any(mask) and np.max(spectrum[mask]) > 0.08:
            count += 1

    return count


def process_file(label, path):
    print(f"Processing: {path.name}")

    y, sr = load_audio(path)
    duration = len(y) / sr

    save_waveform(y, sr, label)
    save_spectrogram(y, sr, label)
    freqs, spectrum = save_average_spectrum(y, sr, label)

    min_freq, max_freq = estimate_voice_range(freqs, spectrum)
    main_tone = estimate_main_tone(freqs, spectrum)
    formants = estimate_formants(freqs, spectrum)
    harmonics_count = count_harmonics(freqs, spectrum, main_tone)

    return {
        "sound": label,
        "file": path.name,
        "duration_sec": round(duration, 3),
        "sample_rate_hz": sr,
        "min_voice_freq_hz": round(min_freq, 2) if min_freq else None,
        "max_voice_freq_hz": round(max_freq, 2) if max_freq else None,
        "main_tone_hz": round(main_tone, 2) if main_tone else None,
        "harmonics_count": harmonics_count,
        "formant_1_hz": round(formants[0], 2) if formants[0] else None,
        "formant_2_hz": round(formants[1], 2) if formants[1] else None,
        "formant_3_hz": round(formants[2], 2) if formants[2] else None,
    }


def main():
    results = []

    for label, path in AUDIO_FILES.items():
        if not path.exists():
            print(f"File not found: {path}")
            continue

        results.append(process_file(label, path))

    df = pd.DataFrame(results)

    csv_path = TABLE_DIR / "voice_analysis_results.csv"
    df.to_csv(csv_path, index=False, sep=";")

    print("\nDone.")
    print(f"Results saved to: {OUTPUT_DIR}")
    print(f"Table saved to: {csv_path}")


if __name__ == "__main__":
    main()