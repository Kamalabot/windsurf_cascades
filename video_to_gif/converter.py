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
from pygifsicle import optimize as gifsicle_optimize
import shutil

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
    return np.mean(np.abs(np.array(frame1) - np.array(frame2)))

def should_keep_frame(frame, prev_frame, threshold):
    """Determine if a frame should be kept based on difference threshold."""
    if prev_frame is None:
        return True
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
    """Optimize a single frame with given parameters."""
    frame, max_colors, dither = args
    try:
        if dither:
            frame = apply_dithering(frame)
        
        # Convert to palette mode with limited colors
        new_frame = frame.convert('P', palette=Image.ADAPTIVE, colors=max_colors)
        return new_frame
    except Exception as e:
        return None

def optimize_gif(input_gif, output_gif, max_colors=256, num_workers=None, frame_skip_threshold=0, dither=True):
    """Optimize GIF file size using advanced techniques and multiprocessing."""
    try:
        if num_workers is None:
            num_workers = max(1, mp.cpu_count() - 1)

        # Open the GIF file
        with Image.open(input_gif) as img:
            # Get total frames for progress bar
            n_frames = img.n_frames
            frames = []
            prev_frame = None
            
            # Extract and filter frames
            click.echo("Extracting and filtering frames...")
            for i in tqdm(range(n_frames), desc="Extracting"):
                img.seek(i)
                current_frame = img.copy()
                
                # Only keep frames that are sufficiently different
                if should_keep_frame(current_frame, prev_frame, frame_skip_threshold):
                    frames.append(current_frame)
                    prev_frame = current_frame

            click.echo(f"Retained {len(frames)}/{n_frames} frames after filtering")

            # Prepare arguments for multiprocessing
            args = [(frame, max_colors, dither) for frame in frames]
            
            # Process frames in parallel with progress bar
            click.echo("Optimizing frames...")
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
            
    except Exception as e:
        click.echo(f"Optimization error: {str(e)}", err=True)
    return False

def create_gif_with_progress(video, output_path, fps, opt, fuzz):
    """Create GIF from video with progress bar."""
    total_frames = int(video.duration * fps)
    
    with tqdm(total=total_frames, desc="Converting") as pbar:
        def progress_callback(t):
            pbar.update(1)
        
        video.write_gif(
            output_path,
            fps=fps,
            program='ffmpeg',
            opt=opt,
            fuzz=fuzz,
            callback=progress_callback
        )

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
            gifsicle_optimize(final_gif_path, 
                            output_file,
                            options=['--optimize=3', f'--lossy={lossy}'])
            
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
