from pathlib import Path

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import stft, istft


# =========================
# Пути проекта
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "input" / "violin_1.wav"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# Базовые функции
# =========================

def load_audio(path: Path):
    """
    Загружает WAV-файл.
    Если файл stereo, переводит его в mono.
    """
    data, sr = sf.read(path)

    if data.ndim == 2:
        print(f"Исходный файл stereo: {data.shape[1]} канала. Переводим в mono.")
        data = data.mean(axis=1)
    else:
        print("Исходный файл mono: 1 канал.")

    data = data.astype(np.float32)

    max_abs = np.max(np.abs(data))
    if max_abs > 0:
        data = data / max_abs

    duration = len(data) / sr

    print("Информация об аудиофайле:")
    print(f"Файл: {path}")
    print(f"Частота дискретизации: {sr} Hz")
    print(f"Количество отсчётов: {len(data)}")
    print(f"Длительность: {duration:.2f} секунд")
    print(f"Максимальная амплитуда: {np.max(np.abs(data)):.4f}")

    return data, sr


def save_audio(path: Path, y, sr):
    """
    Сохраняет звук в WAV без агрессивной нормализации.
    Если амплитуда вышла за [-1, 1], мягко ограничивает.
    """
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    y = np.clip(y, -1.0, 1.0)
    sf.write(path, y.astype(np.float32), sr)


def save_waveform(y, sr, path: Path, title: str):
    """
    Сохраняет график временной формы сигнала.
    """
    time = np.arange(len(y)) / sr

    plt.figure(figsize=(12, 4))
    plt.plot(time, y, linewidth=0.7)
    plt.xlabel("Time, s")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def save_spectrum(y, sr, path: Path, title: str):
    """
    Сохраняет амплитудный спектр всего сигнала.
    """
    spectrum = np.fft.rfft(y)
    freqs = np.fft.rfftfreq(len(y), d=1 / sr)
    magnitude = np.abs(spectrum)

    magnitude_db = 20 * np.log10(magnitude + 1e-12)

    plt.figure(figsize=(12, 4))
    plt.plot(freqs, magnitude_db, linewidth=0.7)
    plt.xlabel("Frequency, Hz")
    plt.ylabel("Magnitude, dB")
    plt.title(title)
    plt.xlim(0, sr / 2)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def compute_stft(y, sr):
    """
    STFT по требованиям лекции:
    окно Ханна примерно 50 мс,
    перекрытие 75%.

    При sr = 44100:
    50 мс ≈ 2205 отсчётов.
    Для удобства берём ближайшее стандартное значение 2048.
    """
    nperseg = 2048
    noverlap = int(nperseg * 0.75)

    freqs, times, zxx = stft(
        y,
        fs=sr,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        boundary="zeros",
        padded=True
    )

    return freqs, times, zxx, nperseg, noverlap


def save_spectrogram(y, sr, path: Path, title: str):
    """
    Сохраняет спектрограмму в логарифмической шкале частот.
    """
    freqs, times, zxx, _, _ = compute_stft(y, sr)

    power_db = 20 * np.log10(np.abs(zxx) + 1e-10)

    # Для логарифмической шкалы нельзя использовать 0 Hz.
    valid = freqs > 0

    plt.figure(figsize=(12, 6))
    plt.pcolormesh(
        times,
        freqs[valid],
        power_db[valid, :],
        shading="gouraud"
    )
    plt.yscale("log")
    plt.ylim(40, sr / 2)
    plt.xlabel("Time, s")
    plt.ylabel("Frequency, Hz, log scale")
    plt.title(title)
    plt.colorbar(label="Magnitude, dB")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


# =========================
# Оценка шума и SNR
# =========================

def estimate_noise_and_snr(y, sr, noise_seconds=2.0, label=""):
    """
    Оценивает мощность шума по первым noise_seconds секундам.
    Считает примерный SNR.
    """
    noise_samples = int(noise_seconds * sr)
    noise_part = y[:noise_samples]

    signal_power = np.mean(y ** 2)
    noise_power = np.mean(noise_part ** 2)

    if noise_power > 0:
        snr_db = 10 * np.log10(signal_power / noise_power)
    else:
        snr_db = np.inf

    print(f"\nОценка шума и SNR {label}:")
    print(f"Участок шума: первые {noise_seconds:.1f} секунд")
    print(f"Средняя мощность всего сигнала: {signal_power:.10f}")
    print(f"Средняя мощность шума: {noise_power:.10f}")
    print(f"SNR: {snr_db:.2f} dB")

    return noise_power, snr_db


def save_metrics_csv(path: Path, original_snr, cleaned_snr):
    """
    Сохраняет сравнение SNR до и после обработки.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("metric;value\n")
        f.write(f"snr_original_db;{original_snr:.4f}\n")
        f.write(f"snr_cleaned_db;{cleaned_snr:.4f}\n")
        f.write(f"snr_difference_db;{cleaned_snr - original_snr:.4f}\n")


# =========================
# Спектральное вычитание
# =========================

def spectral_subtraction(
    y,
    sr,
    noise_start=0.0,
    noise_end=2.0,
    reduction_strength=0.85,
    spectral_floor=0.12
):
    """
    Шумопонижение методом спектрального вычитания.

    Алгоритм:
    1. Разложить сигнал через STFT с окном Ханна.
    2. Взять участок шума, например первые 2 секунды.
    3. Найти средний амплитудный спектр шума.
    4. Вычесть этот спектр из амплитудного спектра всего сигнала.
    5. Фазу оставить от исходного сигнала.
    6. Восстановить сигнал через inverse STFT.

    reduction_strength:
        насколько сильно вычитать шум.
        0.7–0.9 обычно мягче и безопаснее для музыки.
        1.0 и выше может сильнее чистить, но портить тембр.

    spectral_floor:
        нижний предел амплитуды.
        Он нужен, чтобы не возникал "музыкальный шум"
        и чтобы не вырезать полезные гармоники слишком резко.
    """
    freqs, times, zxx, nperseg, noverlap = compute_stft(y, sr)

    magnitude = np.abs(zxx)
    phase = np.angle(zxx)

    # Кадры STFT, которые относятся к шумовому участку.
    noise_mask = (times >= noise_start) & (times <= noise_end)

    if not np.any(noise_mask):
        raise ValueError("Не найден шумовой участок. Проверь noise_start/noise_end.")

    noise_magnitude = magnitude[:, noise_mask]

    # Средний спектр шума по времени.
    noise_profile = np.mean(noise_magnitude, axis=1, keepdims=True)

    # Лёгкое сглаживание шумового профиля по частоте.
    # Это уменьшает резкие провалы и артефакты.
    kernel_size = 7
    kernel = np.ones(kernel_size) / kernel_size
    noise_profile_smoothed = np.apply_along_axis(
        lambda x: np.convolve(x, kernel, mode="same"),
        axis=0,
        arr=noise_profile
    )

    # Спектральное вычитание:
    # Y[f,t] = max(X[f,t] - k * W[f], floor * X[f,t])
    subtracted = magnitude - reduction_strength * noise_profile_smoothed

    floor_value = spectral_floor * magnitude
    cleaned_magnitude = np.maximum(subtracted, floor_value)

    # Сохраняем фазу исходного сигнала.
    cleaned_zxx = cleaned_magnitude * np.exp(1j * phase)

    _, y_cleaned = istft(
        cleaned_zxx,
        fs=sr,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        input_onesided=True,
        boundary=True
    )

    # scipy может вернуть чуть большую длину из-за padding.
    y_cleaned = y_cleaned[:len(y)]

    # Убираем возможные NaN/inf.
    y_cleaned = np.nan_to_num(y_cleaned, nan=0.0, posinf=0.0, neginf=0.0)

    # Важно: не нормализуем до 1.0, иначе шум снова может стать заметнее.
    # Только защищаем от клиппинга.
    peak = np.max(np.abs(y_cleaned))
    if peak > 1.0:
        y_cleaned = y_cleaned / peak

    return y_cleaned.astype(np.float32)


# =========================
# Поиск моментов максимальной энергии
# =========================

def find_max_energy_moments(y, sr, path: Path, delta_t=0.1, delta_f=50.0, top_n=20):
    """
    Находит моменты времени и частотные полосы,
    где энергия максимальна.

    По заданию:
    Δt = 0.1 с
    Δf = 40–50 Гц

    Здесь используем Δf = 50 Гц.
    """
    freqs, times, zxx, _, _ = compute_stft(y, sr)

    power = np.abs(zxx) ** 2

    max_time = times[-1]
    time_bins = np.arange(0, max_time + delta_t, delta_t)
    freq_bins = np.arange(0, sr / 2 + delta_f, delta_f)

    rows = []

    for ti in range(len(time_bins) - 1):
        t1 = time_bins[ti]
        t2 = time_bins[ti + 1]

        time_mask = (times >= t1) & (times < t2)

        if not np.any(time_mask):
            continue

        for fi in range(len(freq_bins) - 1):
            f1 = freq_bins[fi]
            f2 = freq_bins[fi + 1]

            freq_mask = (freqs >= f1) & (freqs < f2)

            if not np.any(freq_mask):
                continue

            local_energy = np.sum(power[np.ix_(freq_mask, time_mask)])

            rows.append((t1, t2, f1, f2, local_energy))

    rows = sorted(rows, key=lambda x: x[4], reverse=True)
    top_rows = rows[:top_n]

    with open(path, "w", encoding="utf-8") as f:
        f.write("rank;time_from_s;time_to_s;freq_from_hz;freq_to_hz;energy\n")

        for rank, (t1, t2, f1, f2, energy) in enumerate(top_rows, start=1):
            f.write(
                f"{rank};"
                f"{t1:.3f};"
                f"{t2:.3f};"
                f"{f1:.1f};"
                f"{f2:.1f};"
                f"{energy:.10f}\n"
            )

    print(f"\nТоп-{top_n} моментов максимальной энергии сохранён в:")
    print(path)


# =========================
# Главная программа
# =========================

def main():
    y, sr = load_audio(INPUT_PATH)

    # 1. Сохраняем графики исходного сигнала.
    save_waveform(
        y,
        sr,
        OUTPUT_DIR / "waveform_original.png",
        "Original audio waveform"
    )

    save_spectrum(
        y,
        sr,
        OUTPUT_DIR / "spectrum_original.png",
        "Original audio spectrum"
    )

    save_spectrogram(
        y,
        sr,
        OUTPUT_DIR / "spectrogram_original.png",
        "Original audio spectrogram, Hann window"
    )

    # 2. Оцениваем шум до обработки.
    _, snr_original = estimate_noise_and_snr(
        y,
        sr,
        noise_seconds=2.0,
        label="до обработки"
    )

    # 3. Применяем спектральное вычитание.
    y_cleaned = spectral_subtraction(
        y,
        sr,
        noise_start=0.0,
        noise_end=2.0,
        reduction_strength=0.85,
        spectral_floor=0.12
    )

    # 4. Сохраняем очищенный звук.
    save_audio(
        OUTPUT_DIR / "violin_1_spectral_subtraction.wav",
        y_cleaned,
        sr
    )

    # 5. Сохраняем графики после обработки.
    save_waveform(
        y_cleaned,
        sr,
        OUTPUT_DIR / "waveform_spectral_subtraction.png",
        "Audio waveform after spectral subtraction"
    )

    save_spectrum(
        y_cleaned,
        sr,
        OUTPUT_DIR / "spectrum_spectral_subtraction.png",
        "Audio spectrum after spectral subtraction"
    )

    save_spectrogram(
        y_cleaned,
        sr,
        OUTPUT_DIR / "spectrogram_spectral_subtraction.png",
        "Audio spectrogram after spectral subtraction, Hann window"
    )

    # 6. Оцениваем шум после обработки.
    _, snr_cleaned = estimate_noise_and_snr(
        y_cleaned,
        sr,
        noise_seconds=2.0,
        label="после спектрального вычитания"
    )

    save_metrics_csv(
        OUTPUT_DIR / "snr_metrics.csv",
        snr_original,
        snr_cleaned
    )

    # 7. Ищем моменты максимальной энергии.
    find_max_energy_moments(
        y,
        sr,
        OUTPUT_DIR / "energy_moments_original.csv",
        delta_t=0.1,
        delta_f=50.0,
        top_n=20
    )

    find_max_energy_moments(
        y_cleaned,
        sr,
        OUTPUT_DIR / "energy_moments_spectral_subtraction.csv",
        delta_t=0.1,
        delta_f=50.0,
        top_n=20
    )

    print("\nГотово.")
    print("Результаты сохранены в папке lab9/output.")
    print("Главный очищенный файл:")
    print(OUTPUT_DIR / "violin_1_spectral_subtraction.wav")


if __name__ == "__main__":
    main()