#!/usr/bin/env python3

import click
from moviepy.editor import VideoFileClip
import os
import sys
from PIL import Image
import tempfile
import glob
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool
import math
import numpy as np
import shutil
import subprocess

def validate_input_file(input_path):
    """Validate the input video file."""
    if not os.path.exists(input_path):
        raise click.BadParameter(f"Input file '{input_path}' does not exist.")
    if not input_path.lower().endswith('.mp4'):
        raise click.BadParameter("Input file must be an MP4 file.")
    return input_path

def validate_output_file(output_path):
    """Validate the output GIF path."""
    if not output_path.lower().endswith('.gif'):
        raise click.BadParameter("Output file must have .gif extension.")
    output_dir = os.path.dirname(output_path) or '.'
    if not os.path.exists(output_dir):
        raise click.BadParameter(f"Output directory '{output_dir}' does not exist.")
    return output_path

def calculate_frame_difference(frame1, frame2):
    """Calculate the difference between two frames."""
    # Convert frames to numpy arrays
    arr1 = np.array(frame1)
    arr2 = np.array(frame2)
    
    # Convert to grayscale if RGB
    if len(arr1.shape) == 3:
        arr1 = np.mean(arr1, axis=2)
    if len(arr2.shape) == 3:
        arr2 = np.mean(arr2, axis=2)
    
    # Ensure both arrays are 2D
    if len(arr1.shape) != 2:
        arr1 = arr1.reshape(arr1.shape[:2])
    if len(arr2.shape) != 2:
        arr2 = arr2.reshape(arr2.shape[:2])
    
    # Calculate mean absolute difference
    diff = np.mean(np.abs(arr1 - arr2))
    return diff

def should_keep_frame(frame, prev_frame, threshold):
    """Determine if a frame should be kept based on difference threshold."""
    if prev_frame is None:
        return True
    
    # Convert frames to PIL Images if they're numpy arrays
    if isinstance(frame, np.ndarray):
        frame = Image.fromarray((frame * 255).astype(np.uint8))
    if isinstance(prev_frame, np.ndarray):
        prev_frame = Image.fromarray((prev_frame * 255).astype(np.uint8))
    
    # Ensure both frames are in the same mode
    if frame.mode != prev_frame.mode:
        frame = frame.convert('RGB')
        prev_frame = prev_frame.convert('RGB')
    
    return calculate_frame_difference(frame, prev_frame) > threshold

def apply_dithering(frame):
    """Apply Floyd-Steinberg dithering to the frame."""
    frame = frame.convert('RGB')
    width, height = frame.size
    pixels = frame.load()
    
    for y in range(height-1):
        for x in range(width-1):
            old_pixel = pixels[x, y]
            new_pixel = tuple(map(lambda x: 0 if x < 128 else 255, old_pixel))
            pixels[x, y] = new_pixel
            
            error = tuple(map(lambda a, b: a - b, old_pixel, new_pixel))
            
            # Distribute error to neighboring pixels
            for nx, ny, w in [(x+1, y, 7/16), (x-1, y+1, 3/16), (x, y+1, 5/16), (x+1, y+1, 1/16)]:
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor = pixels[nx, ny]
                    pixels[nx, ny] = tuple(
                        int(max(0, min(255, neighbor[i] + error[i] * w)))
                        for i in range(3)
                    )
    
    return frame

def optimize_frame(args):
    """Optimize a single frame."""
    frame, max_colors, dither = args
    try:
        # Convert frame to PIL Image if it's a numpy array
        if isinstance(frame, np.ndarray):
            frame = Image.fromarray((frame * 255).astype(np.uint8))
        
        # Ensure frame is in RGB mode
        if frame.mode != 'RGB':
            frame = frame.convert('RGB')
        
        # Apply dithering if enabled
        if dither:
            frame = apply_dithering(frame)
        
        # Quantize colors
        frame = frame.quantize(colors=max_colors, method=2)  # method=2 is median cut
        return frame
    except Exception as e:
        click.echo(f"Frame optimization error: {str(e)}", err=True)
        return None

def gifsicle_optimize(input_path, output_path, options):
    """Optimize GIF using gifsicle command line tool."""
    cmd = ['gifsicle'] + options + ['-i', input_path, '-o', output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"Gifsicle optimization failed: {e.stderr.decode()}", err=True)
        return False

def optimize_gif(input_gif, output_gif, max_colors=256, num_workers=None, frame_skip_threshold=0, dither=True):
    """Optimize GIF file size using advanced techniques and multiprocessing."""
    try:
        frames = []
        prev_frame = None
        
        # Open input GIF
        with Image.open(input_gif) as img:
            n_frames = getattr(img, 'n_frames', 1)
            
            # Extract and filter frames
            click.echo(f"Extracting {n_frames} frames...")
            for i in tqdm(range(n_frames), desc="Extracting"):
                img.seek(i)
                current_frame = img.copy().convert('RGB')
                
                # Only keep frames that are sufficiently different
                if should_keep_frame(current_frame, prev_frame, frame_skip_threshold):
                    frames.append(current_frame)
                    prev_frame = current_frame
            
            click.echo(f"Retained {len(frames)} frames out of {n_frames}")
            
            if not frames:
                click.echo("No frames retained after filtering!", err=True)
                return False
            
            # Set up multiprocessing
            if num_workers is None:
                num_workers = max(1, os.cpu_count() - 1)
            
            # Prepare arguments for multiprocessing
            args = [(frame, max_colors, dither) for frame in frames]
            
            # Process frames in parallel with progress bar
            click.echo(f"Optimizing {len(args)} frames...")
            optimized_frames = []
            with Pool(num_workers) as pool:
                for result in tqdm(
                    pool.imap(optimize_frame, args),
                    total=len(args),
                    desc="Optimizing"
                ):
                    if result is not None:
                        optimized_frames.append(result)
                    else:
                        click.echo("Warning: Failed to optimize a frame", err=True)
            
            if optimized_frames:
                click.echo("Saving optimized GIF...")
                # Calculate optimal duration based on original and retained frame count
                duration = int(img.info.get('duration', 100) * (n_frames / len(frames)))
                
                # Save optimized GIF
                optimized_frames[0].save(
                    output_gif,
                    save_all=True,
                    append_images=optimized_frames[1:],
                    optimize=True,
                    duration=duration,
                    loop=0
                )
                return True
            
            click.echo("No frames were successfully optimized!", err=True)
            return False
            
    except Exception as e:
        click.echo(f"Optimization error: {str(e)}", err=True)
        return False

def create_gif_with_progress(video, output_path, fps, opt, fuzz):
    """Create GIF from video with progress bar."""
    total_frames = int(video.duration * fps)
    
    click.echo(f"Converting video to GIF ({total_frames} frames)...")
    with tqdm(total=1, desc="Converting") as pbar:
        video.write_gif(
            output_path,
            fps=fps,
            program='ffmpeg',
            opt=opt
        )
        pbar.update(1)

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--fps', default=10, help='Frames per second in the output GIF')
@click.option('--scale', default=1.0, help='Scale factor for the output GIF (e.g., 0.5 for half size)')
@click.option('--quality', default=95, help='Quality of the output GIF (1-100)')
@click.option('--colors', default=64, help='Maximum number of colors (2-256)')
@click.option('--workers', default=None, type=int, help='Number of worker processes (default: CPU count - 1)')
@click.option('--frame-skip', default=10.0, help='Frame skip threshold (0-100, higher = more frames skipped)')
@click.option('--dither/--no-dither', default=True, help='Enable/disable dithering')
@click.option('--lossy', default=80, help='Lossy compression level for gifsicle (20-200)')
def convert_to_gif(input_file, output_file, fps, scale, quality, colors, workers, frame_skip, dither, lossy):
    """Convert an MP4 video file to GIF format with advanced optimization.
    
    INPUT_FILE: Path to the input MP4 file
    OUTPUT_FILE: Path for the output GIF file
    """
    try:
        # Validate input and output files
        input_file = validate_input_file(input_file)
        output_file = validate_output_file(output_file)

        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as temp_gif, \
             tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as final_gif:
            temp_gif_path = temp_gif.name
            final_gif_path = final_gif.name

        # Load the video file
        click.echo("Loading video file...")
        with VideoFileClip(input_file) as video:
            # Resize if scale is not 1.0
            if scale != 1.0:
                video = video.resize(scale)
            
            # Convert to GIF with progress bar
            click.echo("Converting to GIF...")
            create_gif_with_progress(
                video,
                temp_gif_path,
                fps=fps,
                opt='optimizeplus',
                fuzz=quality
            )

        # Calculate frame skip threshold based on percentage
        frame_skip_threshold = (frame_skip / 100.0) * 255.0

        # Optimize the GIF using Pillow with multiprocessing
        if optimize_gif(temp_gif_path, final_gif_path, 
                       max_colors=colors, 
                       num_workers=workers,
                       frame_skip_threshold=frame_skip_threshold,
                       dither=dither):
            
            # Apply final optimization with gifsicle
            click.echo("Applying final optimization...")
            if gifsicle_optimize(final_gif_path, 
                             output_file,
                             ['--optimize=3', f'--lossy={lossy}']):
                # Calculate and display compression statistics
                original_size = os.path.getsize(temp_gif_path) / (1024*1024)
                intermediate_size = os.path.getsize(final_gif_path) / (1024*1024)
                final_size = os.path.getsize(output_file) / (1024*1024)
                
                click.echo("\n✨ Conversion completed successfully!")
                click.echo(f"Output file: {output_file}")
                click.echo(f"Original size: {original_size:.2f} MB")
                click.echo(f"After Pillow optimization: {intermediate_size:.2f} MB")
                click.echo(f"Final size: {final_size:.2f} MB")
                click.echo(f"Total compression ratio: {(1 - final_size/original_size)*100:.1f}%")
            else:
                click.echo("❌ Failed to optimize GIF", err=True)
                sys.exit(1)

        # Clean up temporary files
        for temp_file in [temp_gif_path, final_gif_path]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    # Enable support for ANSI escape sequences in Windows
    if os.name == 'nt':
        import colorama
        colorama.init()
    
    # Check if gifsicle is installed
    if not shutil.which('gifsicle'):
        click.echo("⚠️  Warning: gifsicle is not installed. Please install it for maximum compression.")
        click.echo("Installation instructions:")
        click.echo("- Linux: sudo apt-get install gifsicle")
        click.echo("- macOS: brew install gifsicle")
        click.echo("- Windows: Download from http://www.lcdf.org/gifsicle/")
        sys.exit(1)
    
    convert_to_gif()
