from vpython import *  # noqa: F401,F403
import random
import math

# ---------- Scene Setup ----------
scene.title = "Cute 3D Bottle Filling Animation \N{DROPLET}"
scene.width = 1000
scene.height = 700
scene.background = color.white
# Center the view around the bottle body
scene.center = vector(0, 7, 0)
scene.forward = vector(0.2, -0.25, -1)

# Lighting: gentle ambient + a couple of lights for soft highlights
scene.lights = []
distant_light(direction=vector(-1, -1, -1), color=vector(0.9, 0.9, 1))
local_light(pos=vector(6, 12, 8), color=vector(1, 0.95, 0.95))
local_light(pos=vector(-6, 6, -8), color=vector(0.9, 1, 0.95))

# ---------- Bottle Geometry ----------
# Dimensions (in arbitrary units)
y0 = 0.0
body_h = 12.0
neck_h = 3.0
r_bottom = 2.9
r_mid = 2.6
r_top = 2.2
r_neck = 0.8
wall = 0.12

# Inner radii for liquid regions
r_body_inner = r_mid - wall - 0.1  # safely inside body
r_neck_inner = r_neck - wall - 0.05  # safely inside neck

# Glass color (pastel tint) and opacity for a cute translucent look
glass_col = vector(0.7, 0.9, 1.0)

# Build body as three tapered transparent glass cylinders
body1_h = body_h * 0.42
body2_h = body_h * 0.38
body3_h = body_h - body1_h - body2_h

body1 = cylinder(pos=vector(0, y0, 0), axis=vector(0, body1_h, 0), radius=r_bottom,
                 color=glass_col, opacity=0.18, shininess=0.9)
body2 = cylinder(pos=vector(0, y0 + body1_h, 0), axis=vector(0, body2_h, 0), radius=r_mid,
                 color=glass_col, opacity=0.18, shininess=0.9)
body3 = cylinder(pos=vector(0, y0 + body1_h + body2_h, 0), axis=vector(0, body3_h, 0), radius=r_top,
                 color=glass_col, opacity=0.18, shininess=0.9)
# Neck
eck = cylinder(pos=vector(0, y0 + body_h, 0), axis=vector(0, neck_h, 0), radius=r_neck,
                color=glass_col, opacity=0.18, shininess=0.9)
# Rim
rim = ring(pos=vector(0, y0 + body_h + neck_h, 0), axis=vector(0, 1, 0),
           radius=r_neck + 0.05, thickness=0.09, color=glass_col, opacity=0.22)
# Cute cork
cork = cylinder(pos=vector(0, y0 + body_h + neck_h, 0), axis=vector(0, 0.7, 0), radius=r_neck * 0.9,
                color=vector(0.6, 0.35, 0.2), shininess=0.3)

# Base glass disc for nicer look
base = cylinder(pos=vector(0, y0 - 0.08, 0), axis=vector(0, 0.08, 0), radius=r_bottom + 0.05,
                color=glass_col, opacity=0.22)

# ---------- Liquid ----------
liquid_col = vector(0.65, 0.85, 1.0)
liquid_shine = 0.9

# Body liquid (fills first)
liquid_body = cylinder(pos=vector(0, y0, 0), axis=vector(0, 0.001, 0), radius=r_body_inner,
                       color=liquid_col, opacity=0.75, shininess=liquid_shine)
# Neck liquid (fills after body is full)
liquid_neck = cylinder(pos=vector(0, y0 + body_h, 0), axis=vector(0, 0.001, 0), radius=r_neck_inner,
                       color=liquid_col, opacity=0.75, shininess=liquid_shine)

# Gentle wave ring at the top surface of the liquid
wave_count = 22
wave_amp = 0.07
wave_rings = []
for i in range(wave_count):
    s = sphere(pos=vector(0, y0, 0), radius=0.06, color=vector(0.9, 0.95, 1), opacity=0.8)
    wave_rings.append(s)

# ---------- Cute Face (eyes + smile) ----------
# Use ellipsoids so we can "blink" by squashing vertically
eye_sep = 1.8
eye_y = y0 + 5.5
eye_z = r_mid + 0.05  # slightly in front of the bottle body

left_eye = ellipsoid(pos=vector(-eye_sep/2, eye_y, eye_z), size=vector(0.45, 0.45, 0.06), color=color.black)
right_eye = ellipsoid(pos=vector(eye_sep/2, eye_y, eye_z), size=vector(0.45, 0.45, 0.06), color=color.black)

# Smile: a front-facing arc using a curve
smile_y = y0 + 4.4
smile_r = 1.1
smile_pts = []
for a in [i*(math.pi/24) for i in range(25)]:  # 0 to pi
    x = smile_r*math.cos(a)
    y = smile_r*math.sin(a)
    smile_pts.append(vector(x, smile_y - 0.4 + y*0.4, eye_z))
smile = curve(pos=smile_pts, color=color.black, radius=0.05)

# ---------- Heart Bubbles ----------
def make_heart(scale=0.25, col=vector(1, 0.6, 0.8)):
    # Build at origin, then return a compound so we can move/animate easily
    left = sphere(pos=vector(-0.18*scale, 0.1*scale, 0), radius=0.18*scale, color=col, opacity=0.9)
    right = sphere(pos=vector(0.18*scale, 0.1*scale, 0), radius=0.18*scale, color=col, opacity=0.9)
    tip = cone(pos=vector(0, 0.05*scale, 0), axis=vector(0, -0.45*scale, 0), radius=0.23*scale,
               color=col, opacity=0.9)
    return compound([left, right, tip])

heart_colors = [vector(1, 0.6, 0.8), vector(1, 0.7, 0.75), vector(1, 0.55, 0.7), vector(0.95, 0.7, 0.9)]
heart_count = 8
hearts = []
for i in range(heart_count):
    h = make_heart(scale=random.uniform(0.17, 0.28), col=random.choice(heart_colors))
    h.pos = vector(random.uniform(-r_body_inner*0.75, r_body_inner*0.75),
                   random.uniform(y0 + 0.4, y0 + 4.0),
                   random.uniform(-0.25, 0.25))
    h.rotate(angle=random.uniform(0, 2*math.pi), axis=vector(0, 1, 0))
    hearts.append(h)

# ---------- Bubbles ----------
bubble_count = 20
bubbles = []
for i in range(bubble_count):
    b = sphere(pos=vector(random.uniform(-r_body_inner*0.85, r_body_inner*0.85), y0 + 0.3,
                          random.uniform(-r_body_inner*0.85, r_body_inner*0.85)),
               radius=random.uniform(0.05, 0.09), color=vector(1, 1, 1), opacity=0.6, shininess=0.5)
    bubbles.append(b)

# ---------- Pouring Droplets ----------
droplet_count = 12
droplets = []
spout_xz_offset = vector(0.15, 0, 0.0)  # small horizontal offset so stream is visible
spout_y = y0 + body_h + neck_h + 0.8
for i in range(droplet_count):
    d = sphere(pos=vector(0, spout_y + i*0.15, 0) + spout_xz_offset,
               radius=0.09, color=liquid_col, opacity=0.9)
    d.vy = 0.0
    droplets.append(d)

# A little pouring spout visual
spout = cylinder(pos=vector(0, y0 + body_h + neck_h + 1.1, 0) + spout_xz_offset,
                 axis=vector(0, -0.35, 0), radius=0.2, color=vector(0.6, 0.6, 0.6), opacity=0.9)

# ---------- Animation Parameters ----------
level = 0.0  # total filled height across body+neck
level_max = body_h + neck_h
fill_speed = 0.9  # units per second
paused = False

blink_timer = 0.0
blink_interval = 2.6  # seconds between blinks
blink_duration = 0.12
is_blinking = False

# ---------- Helpers ----------

def surface_radius(current_level):
    # Returns the surface radius to place wave ring depending on which section is filling
    if current_level <= 0:
        return r_body_inner
    if current_level < body_h:
        # interpolate body radii across height (approximate using segments)
        if current_level < body1_h:
            return min(r_bottom - wall - 0.15, r_body_inner + 0.25)
        elif current_level < body1_h + body2_h:
            return r_body_inner
        else:
            return min(r_top - wall - 0.1, r_body_inner)
    else:
        return r_neck_inner


def update_waves(current_level, t):
    # Position the wave ring along a circle around the surface
    if current_level <= 0.01:
        for s in wave_rings:
            s.visible = False
        return
    r = surface_radius(current_level)
    y = y0 + min(current_level, body_h) if current_level <= body_h else y0 + body_h + min(current_level - body_h, neck_h)
    # tiny bob if in body; for neck keep small amplitude
    amp = wave_amp if current_level < body_h else wave_amp * 0.5
    for i, s in enumerate(wave_rings):
        angle = 2*math.pi * (i / wave_count)
        s.visible = True
        s.pos = vector(r*math.cos(angle), y + amp*math.sin(angle*2 + t*3.0), r*math.sin(angle))


def reset_scene():
    global level, paused, blink_timer, is_blinking
    level = 0.0
    paused = False
    blink_timer = 0.0
    is_blinking = False
    liquid_body.axis = vector(0, 0.001, 0)
    liquid_neck.axis = vector(0, 0.001, 0)
    for b in bubbles:
        b.pos = vector(random.uniform(-r_body_inner*0.85, r_body_inner*0.85), y0 + 0.3,
                       random.uniform(-r_body_inner*0.85, r_body_inner*0.85))
    for h in hearts:
        h.pos = vector(random.uniform(-r_body_inner*0.75, r_body_inner*0.75),
                       random.uniform(y0 + 0.4, y0 + 4.0),
                       random.uniform(-0.25, 0.25))
    for i, d in enumerate(droplets):
        d.pos = vector(0, spout_y + i*0.15, 0) + spout_xz_offset
        d.vy = 0.0
    left_eye.size.y = 0.45
    right_eye.size.y = 0.45


# ---------- Controls ----------

def on_keydown(evt):
    global paused
    k = evt.key
    if k == ' ':  # space to pause/resume
        paused = not paused
    elif k in ('r', 'R'):
        reset_scene()

scene.bind('keydown', on_keydown)

# ---------- Main Animation Loop ----------
prev_t = 0.0
if hasattr(scene, 'time'):  # vpython provides scene.time
    prev_t = scene.time

while True:
    rate(60)
    # Delta time
    t_now = scene.time if hasattr(scene, 'time') else prev_t + 1/60
    dt = max(1/300, t_now - prev_t)
    prev_t = t_now

    if not paused:
        # Fill progression
        if level < level_max:
            level = min(level_max, level + fill_speed * dt)

        # Update liquid body height then neck height
        body_fill = min(level, body_h)
        neck_fill = max(0.0, level - body_h)
        liquid_body.axis = vector(0, max(0.001, body_fill), 0)
        liquid_neck.axis = vector(0, max(0.001, min(neck_h, neck_fill)), 0)

        # Bubbles rise within the body region; respawn near bottom when leaving the surface
        surf_y = y0 + body_fill if level <= body_h else y0 + body_h
        for b in bubbles:
            # horizontal gentle drift
            b.pos.x += math.sin(t_now*0.8 + id(b)*0.001) * 0.002
            b.pos.z += math.cos(t_now*0.6 + id(b)*0.001) * 0.002
            # rise speed proportional to size
            b.pos.y += 0.35 * dt / max(0.05, b.radius) * 0.03
            # keep inside body radius
            r2d = math.hypot(b.pos.x, b.pos.z)
            if r2d > r_body_inner - 0.05:
                angle = random.random() * 2*math.pi
                b.pos.x = (r_body_inner - 0.1) * math.cos(angle)
                b.pos.z = (r_body_inner - 0.1) * math.sin(angle)
            # respawn
            if b.pos.y > surf_y - 0.2:
                b.pos = vector(random.uniform(-r_body_inner*0.85, r_body_inner*0.85), y0 + 0.3,
                               random.uniform(-r_body_inner*0.85, r_body_inner*0.85))

        # Hearts rise slower and gently rotate
        for h in hearts:
            h.pos.y += 0.15 * dt
            h.rotate(angle=0.5 * dt, axis=vector(0, 1, 0))
            h.rotate(angle=0.2 * dt, axis=vector(1, 0, 0))
            if h.pos.y > surf_y - 0.4:
                h.pos = vector(random.uniform(-r_body_inner*0.75, r_body_inner*0.75), y0 + 0.6,
                               random.uniform(-0.25, 0.25))

        # Pouring droplets physics (simple)
        g = -4.0
        target_surface = y0 + (body_fill if level <= body_h else body_h)
        for d in droplets:
            d.vy += g * dt
            d.pos.y += d.vy * dt
            # Slight x,z wiggle
            d.pos.x += math.sin(t_now*3 + id(d)*0.001) * 0.002
            d.pos.z += math.cos(t_now*2 + id(d)*0.001) * 0.002
            # Hit the liquid surface -> respawn near the spout
            if d.pos.y <= target_surface + 0.05:
                d.pos = vector(0, spout_y, 0) + spout_xz_offset + vector(random.uniform(-0.02, 0.02), 0, random.uniform(-0.02, 0.02))
                d.vy = 0.0

        # Blinking logic
        blink_timer += dt
        if not is_blinking and blink_timer >= blink_interval:
            is_blinking = True
            blink_timer = 0.0
        if is_blinking:
            # Animate eyes squashing for a quick blink
            left_eye.size.y = max(0.06, left_eye.size.y - 0.009 / max(1/60, dt))
            right_eye.size.y = max(0.06, right_eye.size.y - 0.009 / max(1/60, dt))
            if left_eye.size.y <= 0.07:
                # reopen quickly
                left_eye.size.y = 0.45
                right_eye.size.y = 0.45
                is_blinking = False

    # Waves always reflect current surface
    update_waves(level, t_now)
