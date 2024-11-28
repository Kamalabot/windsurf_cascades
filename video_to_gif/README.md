# Video to GIF Converter

A powerful tool to convert MP4 videos to highly optimized GIF files with advanced compression techniques.

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install gifsicle (required for optimal compression):

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install gifsicle
```

### macOS:
```bash
brew install gifsicle
```

### Windows:
Download the gifsicle executable from http://www.lcdf.org/gifsicle/ and add it to your system PATH.

## Usage

Basic usage with optimized defaults:
```bash
python converter.py input.mp4 output.gif
```

For help with options:
```bash
python converter.py --help
```

## Optimization Presets

### Default Settings (Balanced)
```bash
python converter.py input.mp4 output.gif \
    --fps 10 \
    --scale 1.0 \
    --quality 95 \
    --colors 64 \
    --frame-skip 10 \
    --lossy 80
```
Best for most videos, balancing quality and file size.

### Maximum Quality
```bash
python converter.py input.mp4 output.gif \
    --fps 15 \
    --scale 1.0 \
    --quality 100 \
    --colors 256 \
    --frame-skip 5 \
    --lossy 30
```
Highest quality output, larger file size.

### Maximum Compression
```bash
python converter.py input.mp4 output.gif \
    --fps 8 \
    --scale 0.5 \
    --quality 70 \
    --colors 32 \
    --frame-skip 15 \
    --lossy 150 \
    --no-dither
```
Smallest possible file size, reduced quality.

## Parameters Explained

| Parameter | Default | Range | Description |
|-----------|---------|--------|-------------|
| `--fps` | 10 | 5-30 | Frames per second. Higher = smoother but larger |
| `--scale` | 1.0 | 0.1-1.0 | Size scaling factor. 1.0 = original size |
| `--quality` | 95 | 1-100 | Initial conversion quality |
| `--colors` | 64 | 2-256 | Maximum colors in palette |
| `--frame-skip` | 10.0 | 0-100 | Skip similar frames threshold |
| `--dither` | True | True/False | Enable color dithering |
| `--lossy` | 80 | 20-200 | Gifsicle lossy compression level |

## Optimization Guide

### File Size vs Quality Trade-offs

1. For Smaller Files:
   - Reduce `--fps` to 8-10
   - Lower `--scale` to 0.5-0.7
   - Decrease `--colors` to 32-64
   - Increase `--frame-skip` to 12-15
   - Increase `--lossy` to 100-150

2. For Better Quality:
   - Increase `--fps` to 12-15
   - Keep `--scale` at 1.0
   - Use more `--colors` (128-256)
   - Lower `--frame-skip` to 5-8
   - Keep `--lossy` below 80

### Parameter Impact (Most to Least Effective)

1. `--scale`: Most significant impact on file size
   - Each 0.1 reduction roughly halves file size
   - Keep above 0.5 for readability

2. `--colors`: Major impact on file size
   - 32-64 colors: Good balance
   - Below 32: Visible quality loss
   - Above 128: Diminishing returns

3. `--frame-skip`: Affects smoothness and size
   - 5-10: Smooth animation
   - 10-15: Good compression
   - Above 15: May look choppy

4. `--fps`: Controls animation smoothness
   - 8-10: Good compression
   - 10-12: Smooth animation
   - Above 15: Large files

5. `--lossy`: Fine-tunes compression
   - 30-80: High quality
   - 80-120: Good compression
   - Above 120: Visible artifacts

6. `--quality`: Initial conversion quality
   - Above 90: Best quality
   - 70-90: Good compression
   - Below 70: Visible loss

### Tips for Best Results

1. Start with Scale:
   - First adjust `--scale` for target size
   - Consider display context

2. Adjust Colors:
   - Use `--colors 64` for most cases
   - Enable dithering with low colors

3. Fine-tune Motion:
   - Balance `--fps` and `--frame-skip`
   - Higher fps needs higher frame-skip

4. Final Compression:
   - Use `--lossy` last
   - Test different values

## Advanced Features

- Multi-core processing
- Intelligent frame skipping
- Three-stage compression
- Progress tracking
- Detailed statistics

## Troubleshooting

If output is too large:
1. Reduce input video length
2. Lower `--scale`
3. Reduce `--colors`
4. Increase `--frame-skip`
5. Adjust `--lossy`

If quality is poor:
1. Increase `--scale`
2. Add more `--colors`
3. Lower `--frame-skip`
4. Reduce `--lossy`
5. Enable `--dither`