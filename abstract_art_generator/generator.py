import random
import math
from PIL import Image, ImageDraw, ImageChops
from .colors import PALETTES, parse_hex_color

def apply_gradient(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color=0)
    c1 = parse_hex_color(color1) if isinstance(color1, str) else color1
    c2 = parse_hex_color(color2) if isinstance(color2, str) else color2
    draw = ImageDraw.Draw(base)
    for y in range(height):
        t = y / (height - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return base

def apply_noise(img, scale, alpha=50):
    width, height = img.size
    res = (max(1, int(width * scale)), max(1, int(height * scale)))
    noise = Image.new('L', res)
    pix = noise.load()
    for x in range(res[0]):
        for y in range(res[1]):
            pix[x, y] = random.randint(0, 255)
    noise = noise.resize((width, height), resample=Image.BILINEAR)
    noise = noise.convert('RGBA')
    noise.putalpha(alpha)
    base = img.convert('RGBA')
    return Image.alpha_composite(base, noise)

def draw_fractal_tree(draw, x1, y1, length, angle, depth, branch_angle, scale, width, color):
    if depth == 0 or length < 2:
        return
    x2 = x1 + math.cos(angle) * length
    y2 = y1 + math.sin(angle) * length
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    new_length = length * scale
    draw_fractal_tree(draw, x2, y2, new_length, angle - branch_angle, depth - 1, branch_angle, scale, width, color)
    draw_fractal_tree(draw, x2, y2, new_length, angle + branch_angle, depth - 1, branch_angle, scale, width, color)

def generate_art(
    width=800,
    height=600,
    num_shapes=100,
    seed=None,
    palette_name='random',
    custom_palette=None,
    distribution='uniform',
    cluster_count=5,
    cluster_radius=100.0,
    min_shape_size=20.0,
    max_shape_size=200.0,
    size_exponent=2.0,
    shape_types=('ellipse', 'rectangle', 'polygon', 'line'),
    stroke=False,
    stroke_width=1,
    stroke_color=(0, 0, 0),
    blend_mode='normal',
    background_color=(255, 255, 255),
    gradient=False,
    gradient_colors=None,
    noise=False,
    noise_scale=0.1,
    fractal_trees=0,
    fractal_depth=5,
    fractal_branch_angle=math.pi/6,
    fractal_scale=0.7,
    fractal_width=1,
    fractal_color=(0, 0, 0, 255),
):
    random.seed(seed)
    if gradient and gradient_colors and len(gradient_colors) == 2:
        bg = apply_gradient(width, height, gradient_colors[0], gradient_colors[1])
    else:
        bg = Image.new('RGB', (width, height), color=background_color)
    img = bg
    if noise:
        img = apply_noise(img, noise_scale)

    base = img.convert('RGBA')
    if custom_palette:
        palette = [parse_hex_color(c) for c in custom_palette]
    else:
        palette = PALETTES.get(palette_name)

    positions = []
    if distribution == 'uniform':
        positions = [(random.uniform(0, width), random.uniform(0, height)) for _ in range(num_shapes)]
    elif distribution == 'cluster':
        centers = [(random.uniform(0, width), random.uniform(0, height)) for _ in range(cluster_count)]
        for _ in range(num_shapes):
            cx, cy = random.choice(centers)
            angle = random.random() * 2 * math.pi
            r = abs(random.gauss(0, cluster_radius))
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            positions.append((x, y))
    elif distribution == 'radial':
        cx, cy = width / 2, height / 2
        max_r = min(width, height) / 2
        for _ in range(num_shapes):
            angle = random.random() * 2 * math.pi
            r = random.random() * max_r
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            positions.append((x, y))
    else:
        raise ValueError(f'Unknown distribution: {distribution}')

    for x, y in positions:
        factor = random.random() ** size_exponent
        w = min_shape_size + (max_shape_size - min_shape_size) * factor
        h = min_shape_size + (max_shape_size - min_shape_size) * factor
        bbox = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]
        alpha = random.randint(25, 100)
        if palette:
            c = random.choice(palette)
            fill = (c[0], c[1], c[2], alpha)
        else:
            fill = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)
        outline = None
        if stroke:
            outline = parse_hex_color(stroke_color) if isinstance(stroke_color, str) else stroke_color
        layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, 'RGBA')
        shape = random.choice(shape_types)
        if shape == 'ellipse':
            draw.ellipse(bbox, fill=fill, outline=outline, width=stroke_width if stroke else 0)
        elif shape == 'rectangle':
            draw.rectangle(bbox, fill=fill, outline=outline, width=stroke_width if stroke else 0)
        elif shape == 'polygon':
            verts = []
            num_v = random.randint(3, 6)
            for i in range(num_v):
                ang = 2 * math.pi * i / num_v + random.uniform(-math.pi / num_v, math.pi / num_v)
                rad = max(w, h) / 2 * random.uniform(0.5, 1)
                vx = x + math.cos(ang) * rad
                vy = y + math.sin(ang) * rad
                verts.append((vx, vy))
            draw.polygon(verts, fill=fill, outline=outline)
            if stroke and outline and stroke_width > 0:
                # draw polygon outline manually
                pts = verts + [verts[0]]
                draw.line(pts, fill=outline, width=stroke_width)
        elif shape == 'line':
            x1 = random.uniform(bbox[0], bbox[2])
            y1 = random.uniform(bbox[1], bbox[3])
            x2 = random.uniform(bbox[0], bbox[2])
            y2 = random.uniform(bbox[1], bbox[3])
            lw = stroke_width if stroke else max(1, int((w + h) / 20))
            draw.line([(x1, y1), (x2, y2)], fill=fill, width=lw)
        if blend_mode == 'normal':
            base = Image.alpha_composite(base, layer)
        elif blend_mode == 'multiply':
            base = ImageChops.multiply(base, layer)
        elif blend_mode == 'screen':
            base = ImageChops.screen(base, layer)
        else:
            base = Image.alpha_composite(base, layer)

    for _ in range(fractal_trees):
        draw = ImageDraw.Draw(base, 'RGBA')
        x0 = random.uniform(0, width)
        y0 = random.uniform(0, height)
        color = fractal_color
        if isinstance(color, str):
            color = (*parse_hex_color(color), 255)
        draw_fractal_tree(
            draw,
            x0, y0,
            min(height, width) / 3,
            -math.pi / 2,
            fractal_depth,
            fractal_branch_angle,
            fractal_scale,
            fractal_width,
            color
        )
    return base.convert('RGB')

def generate_animation(
    output,
    frames=10,
    duration=0.1,
    **art_kwargs
):
    imgs = []
    seed = art_kwargs.get('seed', None)
    for i in range(frames):
        art_kwargs['seed'] = seed + i if seed is not None else None
        img = generate_art(**art_kwargs)
        imgs.append(img)
    imgs[0].save(
        output,
        save_all=True,
        append_images=imgs[1:],
        duration=int(duration * 1000),
        loop=0
    )