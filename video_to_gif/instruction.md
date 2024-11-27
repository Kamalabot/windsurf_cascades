# MP4 to GIF Converter

A command-line tool to convert MP4 videos to GIF format using Python, with advanced compression and optimization features.

## Features

- Convert MP4 videos to GIF format
- Three-stage compression pipeline
- Intelligent frame skipping
- Floyd-Steinberg dithering
- Parallel processing for faster optimization
- Real-time progress tracking
- Lossy and lossless compression
- Adaptive color palette optimization
- Command-line interface for easy usage
- Detailed compression statistics

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - moviepy (video processing)
  - click (CLI interface)
  - Pillow (image optimization)
  - tqdm (progress bars)
  - pygifsicle (final optimization)
  - numpy (frame analysis)
- System requirements:
  - gifsicle (install via package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd video-to-gif
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Install gifsicle:
- Linux: `sudo apt-get install gifsicle`
- macOS: `brew install gifsicle`
- Windows: Download from http://www.lcdf.org/gifsicle/

## Usage

Basic usage:
```bash
python converter.py input.mp4 output.gif
```

Advanced usage with maximum compression:
```bash
python converter.py input.mp4 output.gif --fps 10 --scale 0.8 --quality 85 --colors 64 --frame-skip 15 --lossy 100
```

## Arguments

Required arguments:
- `input_file`: Path to the input MP4 file
- `output_file`: Path for the output GIF file

Optional arguments:
- `--fps`: Frames per second in output GIF (default: 10)
- `--scale`: Scale factor for resizing (default: 1.0, e.g., 0.5 for half size)
- `--quality`: Initial quality (1-100, default: 95)
- `--colors`: Maximum number of colors (2-256, default: 64)
- `--workers`: Number of worker processes (default: CPU count - 1)
- `--frame-skip`: Frame skip threshold (0-100, default: 10.0)
- `--dither/--no-dither`: Enable/disable dithering (default: enabled)
- `--lossy`: Lossy compression level (20-200, default: 80)

## Advanced Compression Techniques

The converter uses a three-stage optimization process:

1. Initial Conversion (moviepy):
   - Frame extraction and processing
   - Initial compression using ffmpeg
   - Frame rate optimization
   - Quality reduction

2. Intermediate Optimization (Pillow):
   - Intelligent frame skipping
   - Color palette reduction
   - Floyd-Steinberg dithering
   - Parallel frame processing
   - Frame difference analysis

3. Final Optimization (gifsicle):
   - Lossy compression
   - Advanced frame optimization
   - Global color table optimization
   - Metadata optimization

## Tips for Maximum Compression

1. Frame Skipping (--frame-skip):
   - Higher values skip more similar frames
   - Start with 10-15 for good results
   - Maximum 30-40 for aggressive compression

2. Color Reduction (--colors):
   - Use 32-64 colors for high compression
   - Minimum 16 colors for maximum compression
   - Enable dithering to maintain quality

3. Scale Reduction (--scale):
   - 0.5-0.8 for significant size reduction
   - Consider target display size

4. Lossy Compression (--lossy):
   - 80-120 for good compression
   - Up to 200 for maximum compression
   - Higher values may affect quality

5. Frame Rate (--fps):
   - 8-10 fps for most content
   - 5-8 fps for maximum compression

## Example Commands

1. Balanced compression:
```bash
python converter.py input.mp4 output.gif --fps 10 --scale 0.8 --quality 90 --colors 64 --frame-skip 10 --lossy 80
```

2. High compression:
```bash
python converter.py input.mp4 output.gif --fps 8 --scale 0.6 --quality 85 --colors 32 --frame-skip 20 --lossy 120
```

3. Maximum compression:
```bash
python converter.py input.mp4 output.gif --fps 5 --scale 0.5 --quality 70 --colors 16 --frame-skip 30 --lossy 200 --no-dither
```

## Progress Tracking

The converter shows progress for each stage:
1. Loading video file
2. Converting to initial GIF
3. Extracting and filtering frames
4. Optimizing frames in parallel
5. Applying final optimization
6. Detailed compression statistics

## Notes

- Shows frame retention ratio after filtering
- Displays compression statistics for each stage
- Automatic cleanup of temporary files
- Parallel processing for faster optimization
- Supports common MP4 video formats

## License

MIT License
