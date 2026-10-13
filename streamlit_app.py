
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Absolute Value Explorer",
    layout="wide"
)

st.title("Interactive Absolute Value Explorer")

st.write("Explore Absolute Value Function Intuitively")

st.markdown(
    '<div style="text-align:right; line-height:1.0;">'
    '<div><strong>Shirhan A. Biottong</strong></div>'
    '<div><em>Algebra 1</em> Teacher</div>'
    '<div style="font-size:0.75em;">Atlantic Coast High School</div>'
    '</div>',
    unsafe_allow_html=True
)



st.latex(r"y = a|x-h|+k")

# ---------------------------------
# 1. FUNCTION PARAMETERS
# ---------------------------------
st.subheader("1. Change the value to see dynamic changes in the graph")

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

# Calculate y for the selected x
y = a * abs(x - h) + k

# ---------------------------------
# 2. DYNAMIC VIEWING RANGES
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

# Validate viewing ranges
if x_min >= x_max:
    st.error("Minimum x must be less than maximum x.")
    st.stop()

if y_min >= y_max:
    st.error("Minimum y must be less than maximum y.")
    st.stop()

# ---------------------------------
# 3. GENERATE GRAPH
# ---------------------------------
xs = np.linspace(x_min, x_max, 1200)
ys = a * np.abs(xs - h) + k

fig, ax = plt.subplots(figsize=(11, 7))

# Dark background
fig.patch.set_facecolor("#202124")
ax.set_facecolor("#202124")

# Plot absolute value function
ax.plot(
    xs,
    ys,
    color="deepskyblue",
    linewidth=2.5,
    label=r"$y=a|x-h|+k$"
)

# White coordinate axes
ax.axhline(
    y=0,
    color="white",
    linewidth=1.8,
    zorder=2
)

ax.axvline(
    x=0,
    color="white",
    linewidth=1.8,
    zorder=2
)

# Green dotted line of symmetry: x = h
ax.axvline(
    x=h,
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

# Selected input point
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

# Dashed guide lines for selected point
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

# ---------------------------------
# 4. AXIS LIMITS AND TICK INTERVALS
# ---------------------------------
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Tick interval is ALWAYS exactly 1 unit
ax.set_xticks(
    np.arange(
        np.ceil(x_min),
        np.floor(x_max) + 1,
        1
    )
)

ax.set_yticks(
    np.arange(
        np.ceil(y_min),
        np.floor(y_max) + 1,
        1
    )
)

# White tick labels and grid
ax.tick_params(
    axis="both",
    colors="white",
    labelsize=9
)

ax.grid(
    True,
    color="white",
    alpha=0.18
)

# White graph borders
for spine in ax.spines.values():
    spine.set_color("white")

# Axis labels
ax.set_xlabel(
    "x-axis",
    color="white",
    fontsize=12
)

ax.set_ylabel(
    "y-axis",
    color="white",
    fontsize=12
)

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
# 5. STEP-BY-STEP CALCULATIONS
# ---------------------------------
st.subheader("3. Explore the mathematics")

st.markdown("**Equation**")
st.latex(rf"y={a:g}|x-({h:g})|+({k:g})")

st.markdown("**Substitute the selected x-value**")
st.latex(
    rf"y={a:g}|{x:g}-({h:g})|+({k:g})"
)

st.markdown("**Calculate the answer**")
st.latex(rf"y={y:g}")

# Display important properties
m1, m2, m3 = st.columns(3)

m1.metric(
    "Vertex",
    f"({h:g}, {k:g})"
)

m2.metric(
    "Selected point",
    f"({x:g}, {y:g})"
)

m3.metric(
    "Axis of symmetry",
    f"x = {h:g}"
)

# Opening direction and range
if a > 0:
    st.success(
        f"The graph opens upward. Range: y ≥ {k:g}"
    )
elif a < 0:
    st.info(
        f"The graph opens downward. Range: y ≤ {k:g}"
    )
else:
    st.info(
        f"The graph is a horizontal line. Range: y = {k:g}"
    )

st.write("**Domain:** all real numbers.")
