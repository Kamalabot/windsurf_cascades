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

## Usage and Documentation

For detailed usage instructions, compression settings, and optimization strategies, please refer to the [README.md](README.md) file.

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
