"""Command-line interface for the Abstract Art Generator with Mandelbrot."""
import math
import typer
from typing import List, Optional
from .generator_mandel import generate_art, generate_animation
from .colors import PALETTES, parse_hex_color

app = typer.Typer(help="Generate abstract art images and animations.")

@app.command()
def generate(
    width: int = typer.Option(800, "--width", "-W", help="Image width in pixels"),
    height: int = typer.Option(600, "--height", "-H", help="Image height in pixels"),
    num_shapes: int = typer.Option(100, "--num-shapes", "-n", help="Number of random shapes"),
    seed: Optional[int] = typer.Option(None, "--seed", help="Random seed for reproducibility"),
    palette: str = typer.Option("random", "--palette", "-p", help=f"Color palette: {', '.join(PALETTES.keys())}"),
    custom_palette: Optional[List[str]] = typer.Option(None, "--custom-palette", help="Custom hex colors"),
    distribution: str = typer.Option("uniform", "--distribution", "-d", help="Shape distribution: uniform, cluster, radial"),
    cluster_count: int = typer.Option(5, "--clusters", help="Number of clusters (for cluster distribution)"),
    cluster_radius: float = typer.Option(100.0, "--cluster-radius", help="Cluster radius"),
    min_size: float = typer.Option(20.0, "--min-size", help="Minimum shape size"),
    max_size: float = typer.Option(200.0, "--max-size", help="Maximum shape size"),
    size_exponent: float = typer.Option(2.0, "--size-exponent", help="Exponent for size distribution"),
    shape_types: List[str] = typer.Option(["ellipse", "rectangle", "polygon", "line"], "--shape-types", help="Shape types to include"),
    stroke: bool = typer.Option(False, "--stroke", help="Draw shape outlines"),
    stroke_width: int = typer.Option(1, "--stroke-width", help="Outline width"),
    stroke_color: str = typer.Option("#000000", "--stroke-color", help="Outline color (hex)"),
    blend_mode: str = typer.Option("normal", "--blend", help="Blend mode: normal, multiply, screen"),
    background_color: str = typer.Option("#FFFFFF", "--background", help="Background color (hex)"),
    gradient: bool = typer.Option(False, "--gradient", help="Use a gradient background"),
    gradient_colors: Optional[List[str]] = typer.Option(None, "--gradient-colors", help="Two hex colors for gradient"),
    noise: bool = typer.Option(False, "--noise", help="Add noise texture"),
    noise_scale: float = typer.Option(0.1, "--noise-scale", help="Scale of noise (0-1)"),
    fractal_trees: int = typer.Option(0, "--fractal-trees", help="Number of fractal trees to draw"),
    fractal_depth: int = typer.Option(5, "--fractal-depth", help="Depth of fractal trees"),
    fractal_branch_angle: float = typer.Option(math.pi/6, "--fractal-branch-angle", help="Branch angle in radians"),
    fractal_scale: float = typer.Option(0.7, "--fractal-scale", help="Branch length scale factor"),
    fractal_width: int = typer.Option(1, "--fractal-width", help="Line width for fractal"),
    fractal_color: str = typer.Option("#000000", "--fractal-color", help="Color for fractal (hex)"),
    frames: int = typer.Option(1, "--frames", help="Number of frames for animation"),
    duration: float = typer.Option(0.1, "--duration", help="Frame duration in seconds"),
    output: str = typer.Option("art.png", "--output", "-o", help="Output filename"),
    mandelbrot: bool = typer.Option(False, "--mandelbrot", help="Draw colorful Mandelbrot fractal"),
    mandelbrot_iter: int = typer.Option(200, "--mandelbrot-iter", help="Iterations for Mandelbrot fractal"),
    mandelbrot_zoom: float = typer.Option(1.0, "--mandelbrot-zoom", help="Mandelbrot zoom factor"),
    mandelbrot_cx: float = typer.Option(-0.7, "--mandelbrot-cx", help="Mandelbrot real center"),
    mandelbrot_cy: float = typer.Option(0.0, "--mandelbrot-cy", help="Mandelbrot imaginary center"),
    mandelbrot_color_offset: float = typer.Option(0.0, "--mandelbrot-color-offset", help="Mandelbrot color cycling offset"),
):
    """Generate a static image or animation."""
    bg_color = parse_hex_color(background_color)
    stroke_col = stroke_color
    fractal_col = fractal_color
    grad_cols = None
    if gradient and gradient_colors and len(gradient_colors) == 2:
        grad_cols = gradient_colors
    art_kwargs = {
        "width": width,
        "height": height,
        "num_shapes": num_shapes,
        "seed": seed,
        "palette_name": palette,
        "custom_palette": custom_palette,
        "distribution": distribution,
        "cluster_count": cluster_count,
        "cluster_radius": cluster_radius,
        "min_shape_size": min_size,
        "max_shape_size": max_size,
        "size_exponent": size_exponent,
        "shape_types": shape_types,
        "stroke": stroke,
        "stroke_width": stroke_width,
        "stroke_color": stroke_col,
        "blend_mode": blend_mode,
        "background_color": bg_color,
        "gradient": gradient,
        "gradient_colors": grad_cols,
        "noise": noise,
        "noise_scale": noise_scale,
        "fractal_trees": fractal_trees,
        "fractal_depth": fractal_depth,
        "fractal_branch_angle": fractal_branch_angle,
        "fractal_scale": fractal_scale,
        "fractal_width": fractal_width,
        "fractal_color": fractal_col,
        "mandelbrot": mandelbrot,
        "mandelbrot_iter": mandelbrot_iter,
        "mandelbrot_zoom": mandelbrot_zoom,
        "mandelbrot_center": (mandelbrot_cx, mandelbrot_cy),
        "mandelbrot_color_offset": mandelbrot_color_offset,
    }
    if frames > 1:
        generate_animation(output, frames=frames, duration=duration, **art_kwargs)
        typer.echo(f"Animation saved to {output}")
    else:
        img = generate_art(**art_kwargs)
        img.save(output)
        typer.echo(f"Art saved to {output}")

def main():
    app()

if __name__ == "__main__":
    main()

