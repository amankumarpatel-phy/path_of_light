import time
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Path of Light — Fermat's Principle", layout="wide")

st.title("Path of Light from a Fish to Your Eye")
st.subheader("Fermat's Principle in the spirit of Feynman's Lectures")

st.markdown(
    """
Fermat's principle says light takes the path that makes **travel time stationary** (usually minimal).
For a fish underwater and an observer in air, light bends at the surface so that time is minimized,
which gives Snell's law.
"""
)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Scene geometry")
    water_depth = st.slider("Fish depth below surface (m)", 0.5, 5.0, 2.0, 0.1)
    eye_height = st.slider("Observer eye height above surface (m)", 0.5, 5.0, 2.0, 0.1)
    fish_x = st.slider("Fish horizontal position (m)", -6.0, -0.5, -3.0, 0.1)
    eye_x = st.slider("Observer horizontal position (m)", 0.5, 6.0, 3.0, 0.1)

with col2:
    st.markdown("### Optical speeds")
    c_air = st.slider("Speed in air (relative units)", 1.0, 3.0, 2.25, 0.05)
    c_water = st.slider("Speed in water (relative units)", 0.5, 2.5, 1.69, 0.05)
    n_air = 1 / c_air
    n_water = 1 / c_water
    st.info(f"Refractive-index ratio (n_water / n_air): {n_water / n_air:.3f}")

fish = np.array([fish_x, -water_depth])
eye = np.array([eye_x, eye_height])

# Candidate refraction point at y = 0
x_cross = np.linspace(fish_x - 1.0, eye_x + 1.0, 300)

def travel_time(x0: float) -> float:
    p = np.array([x0, 0.0])
    d_water = np.linalg.norm(fish - p)
    d_air = np.linalg.norm(eye - p)
    return d_water / c_water + d_air / c_air

T = np.array([travel_time(x0) for x0 in x_cross])
i_opt = int(np.argmin(T))
x_opt = float(x_cross[i_opt])
T_opt = float(T[i_opt])

opt_point = np.array([x_opt, 0.0])

# Angles with respect to the normal (vertical)
vw = opt_point - fish
va = eye - opt_point
sin_theta_water = abs(vw[0]) / np.linalg.norm(vw)
sin_theta_air = abs(va[0]) / np.linalg.norm(va)

lhs = n_water * sin_theta_water
rhs = n_air * sin_theta_air

st.markdown("---")
st.markdown("### Numerical result")
st.write(f"Optimal crossing point at surface: x = **{x_opt:.3f} m**")
st.write(f"Minimum travel time (relative units): **{T_opt:.5f}**")
st.write(
    f"Snell check: n_water sin(theta_water) = **{lhs:.5f}**, "
    f"n_air sin(theta_air) = **{rhs:.5f}**, difference = **{abs(lhs-rhs):.2e}**"
)

left, right = st.columns([1, 1])

with left:
    st.markdown("### Animation: trying many possible paths")
    run_animation = st.button("Run scan animation")
    frame_holder = st.empty()

    def draw_scene(x0: float, highlight=False):
        p = np.array([x0, 0.0])
        fig, ax = plt.subplots(figsize=(6, 4))

        # Regions
        ax.axhspan(-10, 0, color="#87CEFA", alpha=0.35, label="Water")
        ax.axhspan(0, 10, color="#FFFACD", alpha=0.4, label="Air")
        ax.axhline(0, color="k", lw=1.5)

        # Points
        ax.plot(fish[0], fish[1], "bo", markersize=8)
        ax.text(fish[0] + 0.1, fish[1] - 0.2, "Fish", color="b")
        ax.plot(eye[0], eye[1], "ro", markersize=8)
        ax.text(eye[0] + 0.1, eye[1] + 0.1, "Eye", color="r")

        # Path segments
        color = "crimson" if highlight else "gray"
        lw = 3 if highlight else 1.8
        alpha = 1.0 if highlight else 0.65
        ax.plot([fish[0], p[0]], [fish[1], p[1]], color=color, lw=lw, alpha=alpha)
        ax.plot([p[0], eye[0]], [p[1], eye[1]], color=color, lw=lw, alpha=alpha)

        # optimal crossing marker
        ax.plot(opt_point[0], opt_point[1], marker="*", color="gold", markersize=12)

        time_value = travel_time(x0)
        ax.set_title(f"Surface crossing x = {x0:.2f}, travel time = {time_value:.4f}")
        ax.set_xlim(min(fish_x - 1.5, -7), max(eye_x + 1.5, 7))
        ax.set_ylim(-water_depth - 1.0, eye_height + 1.2)
        ax.set_xlabel("Horizontal position x")
        ax.set_ylabel("Vertical position y")
        ax.grid(alpha=0.3)
        frame_holder.pyplot(fig, clear_figure=True)

    if run_animation:
        for x0 in np.linspace(x_cross.min(), x_cross.max(), 60):
            draw_scene(float(x0), highlight=abs(x0 - x_opt) < 0.08)
            time.sleep(0.03)

    # Always show final best path
    draw_scene(x_opt, highlight=True)

with right:
    st.markdown("### Travel time versus crossing point")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(x_cross, T, color="navy", lw=2)
    ax2.plot(x_opt, T_opt, "o", color="crimson", markersize=8)
    ax2.set_xlabel("Surface crossing position x")
    ax2.set_ylabel("Total travel time")
    ax2.set_title("Fermat's principle: minimum-time path")
    ax2.grid(alpha=0.3)
    st.pyplot(fig2, clear_figure=True)

st.markdown("---")
st.caption(
    "Tip: move fish/eye positions and speeds, then rerun the animation. "
    "You will see the minimum shift while Snell's law remains satisfied."
)
