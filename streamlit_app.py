
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Absolute Value Explorer",
    layout="wide"
)

st.title("Interactive Absolute Value Explorer")
st.write("Change the equation and viewing window to explore the graph.")

st.latex(r"y = a|x-h|+k")

# ---------------------------------
# FUNCTION PARAMETERS
# ---------------------------------
st.subheader("1. Change the equation")

c1, c2, c3, c4 = st.columns(4)

with c1:
    a = st.number_input(
        "a (stretch/flip)",
        value=1.0,
        step=0.5
    )

with c2:
    h = st.number_input(
        "h (left/right)",
        value=0.0,
        step=1.0
    )

with c3:
    k = st.number_input(
        "k (up/down)",
        value=0.0,
        step=1.0
    )

with c4:
    x = st.number_input(
        "x (input point)",
        value=2.0,
        step=1.0
    )

y = a * abs(x - h) + k

# ---------------------------------
# DYNAMIC AXIS RANGES
# ---------------------------------
st.subheader("2. Adjust the graph window")

r1, r2 = st.columns(2)

with r1:
    st.markdown("**Horizontal axis (x)**")

    x_min = st.number_input(
        "Minimum x",
        value=-10.0,
        step=1.0,
        key="xmin"
    )

    x_max = st.number_input(
        "Maximum x",
        value=10.0,
        step=1.0,
        key="xmax"
    )

with r2:
    st.markdown("**Vertical axis (y)**")

    y_min = st.number_input(
        "Minimum y",
        value=-10.0,
        step=1.0,
        key="ymin"
    )

    y_max = st.number_input(
        "Maximum y",
        value=10.0,
        step=1.0,
        key="ymax"
    )

# Validate ranges
if x_min >= x_max:
    st.error("Minimum x must be less than maximum x.")
    st.stop()

if y_min >= y_max:
    st.error("Minimum y must be less than maximum y.")
    st.stop()

# ---------------------------------
# GENERATE GRAPH
# ---------------------------------
xs = np.linspace(x_min, x_max, 1200)
ys = a * np.abs(xs - h) + k

fig, ax = plt.subplots(figsize=(11, 7))

# Dark background
fig.patch.set_facecolor("#202124")
ax.set_facecolor("#202124")

# Function
ax.plot(
    xs,
    ys,
    color="deepskyblue",
    linewidth=2.5,
    label=r"$y=a|x-h|+k$"
)

# White coordinate axes
ax.axhline(
    0,
    color="white",
    linewidth=1.8,
    zorder=2
)

ax.axvline(
    0,
    color="white",
    linewidth=1.8,
    zorder=2
)

# GREEN DOTTED LINE OF SYMMETRY: x = h
ax.axvline(
    h,
    color="lime",
    linestyle=":",
    linewidth=2.5,
    label=f"Axis of symmetry: x = {h:g}",
    zorder=3
)

# Vertex
ax.scatter(
    h,
    k,
    color="red",
    s=110,
    zorder=5,
    label=f"Vertex ({h:g}, {k:g})"
)

# Current input point
ax.scatter(
    x,
    y,
    color="yellow",
    edgecolors="black",
    linewidths=0.7,
    s=110,
    zorder=6,
    label=f"Point ({x:g}, {y:g})"
)

# Dashed guide lines to locate the point
ax.plot(
    [x, x],
    [0, y],
    color="yellow",
    linestyle="--",
    alpha=0.8
)

ax.plot(
    [0, x],
    [y, y],
    color="yellow",
    linestyle="--",
    alpha=0.8
)

# Dynamic viewing limits
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Choose readable tick intervals dynamically
def choose_step(span):
    rough_step = span / 10
    magnitude = 10 ** np.floor(np.log10(rough_step))
    normalized = rough_step / magnitude

    if normalized <= 1:
        nice = 1
    elif normalized <= 2:
        nice = 2
    elif normalized <= 5:
        nice = 5
    else:
        nice = 10

    return nice * magnitude

x_step = choose_step(x_max - x_min)
y_step = choose_step(y_max - y_min)

ax.set_xticks(np.arange(
    np.ceil(x_min / x_step) * x_step,
    x_max + x_step * 0.01,
    x_step
))

ax.set_yticks(np.arange(
    np.ceil(y_min / y_step) * y_step,
    y_max + y_step * 0.01,
    y_step
))

# White tick labels, grid, borders and axis labels
ax.tick_params(colors="white", labelsize=9)
ax.grid(True, color="white", alpha=0.18)

for spine in ax.spines.values():
    spine.set_color("white")

ax.set_xlabel("x-axis", color="white", fontsize=12)
ax.set_ylabel("y-axis", color="white", fontsize=12)

ax.set_title(
    "Absolute Value Function",
    color="white",
    fontsize=15
)

# Legend
legend = ax.legend(loc="best")
legend.get_frame().set_facecolor("#303134")
legend.get_frame().set_edgecolor("white")

for text in legend.get_texts():
    text.set_color("white")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ---------------------------------
# CALCULATIONS
# ---------------------------------
st.subheader("3. Explore the mathematics")

st.markdown("**Equation**")
st.latex(rf"y={a:g}|x-({h:g})|+({k:g})")

st.markdown("**Substitute the selected x-value**")
st.latex(
    rf"y={a:g}|{x:g}-({h:g})|+({k:g})"
)

st.markdown("**Result**")
st.latex(rf"y={y:g}")

m1, m2, m3 = st.columns(3)

m1.metric("Vertex", f"({h:g}, {k:g})")
m2.metric("Selected point", f"({x:g}, {y:g})")
m3.metric("Axis of symmetry", f"x = {h:g}")

if a > 0:
    st.success(f"Opens upward. Range: y ≥ {k:g}")
elif a < 0:
    st.info(f"Opens downward. Range: y ≤ {k:g}")
else:
    st.info(f"Horizontal line. Range: y = {k:g}")

st.write("**Domain:** all real numbers.")
