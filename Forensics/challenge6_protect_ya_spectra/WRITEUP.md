# Challenge 6: Protect Ya Spectra — Writeup

## Overview
The victim’s iPod held a single track. In its spectrum, a message meant for investigators: a warning to always protect your neck when the Zodiac is near.

- File: `track.mp3`
- Category: Audio Steganography (Medium)
- Method: Visible spectrogram text (Side-only tones)
- Flag: `SecurinetsENIT{Y0U_MUST_4LW4YS_PR0T3CT_Y4_N3CK}`

---

## Steps (Audacity)
1. File → Import → Audio… → select `track.mp3`.
2. Track name ▼ → Spectrogram.
3. Spectrogram Settings…
   - Scale: Log
   - FFT size: 8192–16384
   - Window: Hann
   - Overlap: 80–90%
   - Max freq: ~16 kHz
4. Zoom into the last ~30 seconds.
5. Focus on 9–14 kHz. If faint, increase Range/dynamic range.
6. Optional: derive stereo difference (L−R) for extra contrast.

## Steps (Sonic Visualiser)
1. File → Open → `track.mp3`.
2. Layer → Add Spectrogram.
   - Log scale, window 8192–16384, high overlap.
3. Zoom to the last ~30 seconds, 9–14 kHz band.

## What you see
A large, high-contrast text appears across the band:

```
SecurinetsENIT{Y0U_MUST_4LW4YS_PR0T3CT_Y4_N3CK}
```

---

## Notes
- The imprint is generated with tones mapped to a text mask in the Side channel, making it robust yet easy to read with proper spectrogram settings.
- Metadata is clean and decoy; it doesn’t contain the flag.
