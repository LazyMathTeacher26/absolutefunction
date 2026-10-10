
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Absolute Value Explorer",
    layout="wide"
)

st.title("Interactive Absolute Value Explorer")
st.write("Change the values and watch the graph respond.")

st.latex(r"y = a|x-h|+k")

# Interactive controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    a = st.number_input("a (stretch/flip)", value=1.0, step=0.5)

with col2:
    h = st.number_input("h (left/right)", value=0.0, step=1.0)

with col3:
    k = st.number_input("k (up/down)", value=0.0, step=1.0)

with col4:
    x = st.number_input("x (input)", value=2.0, step=1.0)

# Calculate y
y = a * abs(x - h) + k

# Generate function
xs = np.linspace(-10, 10, 1000)
ys = a * np.abs(xs - h) + k

# Create graph
fig, ax = plt.subplots(figsize=(10, 6))

fig.patch.set_facecolor("#202124")
ax.set_facecolor("#202124")

ax.plot(
    xs, ys,
    color="deepskyblue",
    linewidth=2.5,
    label="y = a|x-h|+k"
)

# White coordinate axes
ax.axhline(0, color="white", linewidth=2)
ax.axvline(0, color="white", linewidth=2)

# Grid and numbered ticks
ax.set_xticks(np.arange(-10, 11, 1))
ax.set_yticks(np.arange(-10, 11, 1))
ax.tick_params(colors="white", labelsize=9)
ax.grid(True, color="white", alpha=0.18)

for spine in ax.spines.values():
    spine.set_color("white")

# Vertex
ax.scatter(
    h, k, color="red", s=100, zorder=5,
    label=f"Vertex ({h:g}, {k:g})"
)

# Selected point
ax.scatter(
    x, y, color="lime", s=100, zorder=6,
    label=f"Point ({x:g}, {y:g})"
)

# Guide lines
ax.plot([x, x], [0, y], "g--", alpha=0.7)
ax.plot([0, x], [y, y], "g--", alpha=0.7)

ax.set_xlim(-10, 10)

ymin = min(-10, k - 3, float(np.min(ys)) - 1)
ymax = max(10, k + 3, float(np.max(ys)) + 1)
ax.set_ylim(ymin, ymax)

ax.set_xlabel("x-axis", color="white")
ax.set_ylabel("y-axis", color="white")
ax.set_title(
    "Absolute Value Function",
    color="white"
)

legend = ax.legend()
legend.get_frame().set_facecolor("#303134")
for item in legend.get_texts():
    item.set_color("white")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Show calculations
st.subheader("Step-by-step calculation")

st.latex(
    rf"y={a:g}|{x:g}-({h:g})|+({k:g})"
)
st.latex(
    rf"y={a:g}\times {abs(x-h):g}+({k:g})"
)
st.latex(rf"\boxed{{y={y:g}}}")

st.write(f"**Selected point:** ({x:g}, {y:g})")
st.write(f"**Vertex:** ({h:g}, {k:g})")
st.write(f"**Axis of symmetry:** x = {h:g}")

if a > 0:
    st.write(f"**Range:** y ≥ {k:g}")
elif a < 0:
    st.write(f"**Range:** y ≤ {k:g}")
else:
    st.write(f"**Range:** y = {k:g}")

st.write("**Domain:** all real numbers")
