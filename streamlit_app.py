
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

st.set_page_config(
    page_title="Absolute Value Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 0.4rem;
    padding-bottom: 0rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
}
h1 {font-size: 1.5rem !important; margin: 0 !important;}
h2, h3 {font-size: 1rem !important; margin: 0.2rem 0 !important;}
p {margin-bottom: 0.15rem !important;}
div[data-testid="stVerticalBlock"] {gap: 0.3rem;}
div[data-testid="stMetric"] {padding: 0.2rem;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# 1. VERTICAL SIDEBAR CONTROLS
# ---------------------------------
with st.sidebar:
    st.subheader("1. Function Parameters")

    a = st.number_input("a (stretch/flip)", value=1.0, step=0.5)
    h = st.number_input("h (left/right)", value=0.0, step=1.0)
    k = st.number_input("k (up/down)", value=0.0, step=1.0)
    x = st.number_input("x (input point)", value=0.0, step=1.0)

    st.divider()
    st.subheader("2. Graph Window")

    st.caption("Horizontal axis (x)")
    x_min = st.number_input("Minimum x", value=-10.0, step=1.0, key="xmin")
    x_max = st.number_input("Maximum x", value=10.0, step=1.0, key="xmax")

    st.caption("Vertical axis (y)")
    y_min = st.number_input("Minimum y", value=-10.0, step=1.0, key="ymin")
    y_max = st.number_input("Maximum y", value=10.0, step=1.0, key="ymax")

# ---------------------------------
# 2. VALIDATE RANGES
# ---------------------------------
if x_min >= x_max or y_min >= y_max:
    st.error("Each minimum must be less than its maximum.")
    st.stop()

# ---------------------------------
# 3. CALCULATE FUNCTION
# ---------------------------------
y = a * abs(x - h) + k

X = sp.Symbol("x")
ac = sp.nsimplify(a)
hc = sp.nsimplify(h)
kc = sp.nsimplify(k)

expr = sp.simplify(ac * sp.Abs(X - hc) + kc)

# Simplify coefficient 1 and avoid unnecessary + 0
if ac == 1:
    expr = sp.Abs(X - hc) + kc
elif ac == -1:
    expr = -sp.Abs(X - hc) + kc

expr = sp.simplify(expr)

# ---------------------------------
# 4. HEADER
# ---------------------------------
left, right = st.columns([3, 1])

with left:
    st.title("Interactive Absolute Value Explorer")
    st.caption("Explore Absolute Value Functions Intuitively")

with right:
    st.markdown("""
    <div style="text-align:right;line-height:1.1;font-size:0.8rem;">
    <strong>Shirhan A. Biottong</strong><br>
    <em>Algebra 1 Teacher</em><br>
    <span style="font-size:0.7rem;">Atlantic Coast High School</span>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# 5. GRAPH AND MATHEMATICS
# ---------------------------------
graph_col, math_col = st.columns([1.7, 1])

with graph_col:
    st.latex(r"y=a|x-h|+k")

    xs = np.linspace(x_min, x_max, 1000)
    ys = a * np.abs(xs - h) + k

    fig, ax = plt.subplots(figsize=(7, 4.8))
    fig.patch.set_facecolor("#202124")
    ax.set_facecolor("#202124")

    ax.plot(
        xs, ys,
        color="deepskyblue",
        linewidth=2.5,
        label=r"$y=a|x-h|+k$"
    )

    # White coordinate axes
    ax.axhline(0, color="white", linewidth=1.5)
    ax.axvline(0, color="white", linewidth=1.5)

    # Green dotted symmetry line
    ax.axvline(
        h, color="lime", linestyle=":",
        linewidth=2,
        label=f"Symmetry: x = {h:g}"
    )

    # Vertex
    ax.scatter(
        h, k, color="red", s=85, zorder=5,
        label=f"Vertex ({h:g}, {k:g})"
    )

    # Selected point
    ax.scatter(
        x, y, color="yellow", edgecolors="black",
        s=85, zorder=6,
        label=f"Point ({x:g}, {y:g})"
    )

    # Guide lines
    ax.plot([x, x], [0, y], color="yellow", linestyle="--", alpha=0.8)
    ax.plot([0, x], [y, y], color="yellow", linestyle="--", alpha=0.8)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # One-unit tick intervals
    ax.set_xticks(np.arange(np.ceil(x_min), np.floor(x_max) + 1, 1))
    ax.set_yticks(np.arange(np.ceil(y_min), np.floor(y_max) + 1, 1))

    ax.tick_params(colors="white", labelsize=8)
    ax.grid(True, color="white", alpha=0.18)

    for spine in ax.spines.values():
        spine.set_color("white")

    ax.set_xlabel("x-axis", color="white")
    ax.set_ylabel("y-axis", color="white")
    ax.set_title("Absolute Value Function", color="white", fontsize=12)

    legend = ax.legend(loc="best", fontsize=7)
    legend.get_frame().set_facecolor("#303134")
    legend.get_frame().set_edgecolor("white")

    for label in legend.get_texts():
        label.set_color("white")

    fig.tight_layout(pad=0.7)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with math_col:
    st.subheader("3. Explore the Mathematics")

    st.markdown("**Simplified Equation**")
    st.latex(rf"y={sp.latex(expr)}")

    st.divider()

    st.markdown("**Substitution**")
    st.latex(rf"y={a:g}\left|{x:g}-({h:g})\right|+({k:g})")

    st.markdown("**Calculated y-value**")
    st.latex(rf"y={y:g}")

    st.divider()

    st.markdown("**Key Properties**")
    st.write(f"Vertex: ({h:g}, {k:g})")
    st.write(f"Selected point: ({x:g}, {y:g})")
    st.write(f"Axis of symmetry: x = {h:g}")

    if a > 0:
        st.write("Opens upward")
        st.write(f"Range: y ≥ {k:g}")
    elif a < 0:
        st.write("Opens downward")
        st.write(f"Range: y ≤ {k:g}")
    else:
        st.write("Horizontal line")
        st.write(f"Range: y = {k:g}")

    st.caption("Domain: all real numbers.")




# ---------------------------------
# 6. GAMIFIED ABSOLUTE VALUE MISSION
# ---------------------------------

st.markdown("---")
st.subheader("🎮 Absolute Value Mission")
st.caption(
    "Explore the function, predict its opening, "
    "and substitute x-values to earn points!"
)

# Initialize game state
if "function_score" not in st.session_state:
    st.session_state.function_score = 0

if "function_round" not in st.session_state:
    st.session_state.function_round = 0

if "function_feedback" not in st.session_state:
    st.session_state.function_feedback = {}

if "function_attempts" not in st.session_state:
    st.session_state.function_attempts = set()

# ---------------------------------
# DISPLAY SIMPLIFIED FUNCTION
# ---------------------------------
st.markdown("**Your simplified function**")
st.latex(rf"y={sp.latex(expr)}")

# ---------------------------------
# THREE COMPACT GAME COLUMNS
# ---------------------------------
game1, game2, game3 = st.columns([1, 1.2, 1])

# ---------------------------------
# CHALLENGE 1: OPENING DIRECTION
# ---------------------------------
with game1:
    st.markdown("**🚀 Challenge 1: Opening**")
    st.write("Which way does your graph open?")

    opening_options = ["Upward", "Downward", "Horizontal"]

    opening_key = f"opening_answer_{st.session_state.function_round}"

    opening_answer = st.radio(
        "Choose the direction",
        opening_options,
        key=opening_key,
        label_visibility="collapsed"
    )

    opening_id = (
        st.session_state.function_round,
        "opening"
    )

    if st.button(
        "Check opening",
        key=f"check_opening_{st.session_state.function_round}",
        use_container_width=True
    ):
        if opening_id not in st.session_state.function_attempts:
            correct_opening = (
                "Upward" if a > 0
                else "Downward" if a < 0
                else "Horizontal"
            )

            if opening_answer == correct_opening:
                st.session_state.function_score += 10
                st.session_state.function_feedback["opening"] = (
                    f"✅ Correct! Since a = {a:g}, "
                    f"the graph opens {correct_opening.lower()}."
                )
            else:
                st.session_state.function_feedback["opening"] = (
                    f"💡 The graph opens {correct_opening.lower()}. "
                    f"Look at the sign of a = {a:g}."
                )

            st.session_state.function_attempts.add(opening_id)

    if "opening" in st.session_state.function_feedback:
        st.info(st.session_state.function_feedback["opening"])

# ---------------------------------
# CHALLENGE 2: SUBSTITUTE AN X-VALUE
# ---------------------------------
with game2:
    st.markdown("**🧮 Challenge 2: Substitute**")

    challenge_x = st.number_input(
        "Choose an x-value",
        value=2.0,
        step=1.0,
        key="game_challenge_x"
    )

    correct_y = a * abs(challenge_x - h) + k

    # Simplified substitution display
    st.markdown("**Substitute into the function**")
    st.latex(
        rf"y={a:g}\left|{challenge_x:g}-({h:g})\right|+({k:g})"
    )

    student_y = st.number_input(
        "What is y?",
        value=0.0,
        step=1.0,
        key=f"game_answer_{st.session_state.function_round}"
    )

    substitution_id = (
        st.session_state.function_round,
        "substitution"
    )

    if st.button(
        "Check y",
        key=f"check_y_{st.session_state.function_round}",
        use_container_width=True
    ):
        if substitution_id not in st.session_state.function_attempts:
            if np.isclose(student_y, correct_y):
                st.session_state.function_score += 10
                st.session_state.function_feedback["substitution"] = (
                    f"✅ Correct! y = {correct_y:g}. "
                    "You earned 10 points!"
                )
            else:
                st.session_state.function_feedback["substitution"] = (
                    "💡 Try again. Remember to evaluate the "
                    "absolute value first."
                )

            st.session_state.function_attempts.add(substitution_id)

    if "substitution" in st.session_state.function_feedback:
        st.info(st.session_state.function_feedback["substitution"])

# ---------------------------------
# CHALLENGE 3: FUNCTION FACTS AND SCORE
# ---------------------------------
with game3:
    st.markdown("**🏆 Challenge 3: Function Facts**")

    st.caption(f"Vertex: ({h:g}, {k:g})")
    st.caption(f"Symmetry: x = {h:g}")

    if a > 0:
        st.caption("↗ Opens upward")
        st.caption(f"Range: y ≥ {k:g}")
    elif a < 0:
        st.caption("↘ Opens downward")
        st.caption(f"Range: y ≤ {k:g}")
    else:
        st.caption("— Horizontal line")
        st.caption(f"Range: y = {k:g}")

    st.metric(
        "Total points",
        st.session_state.function_score
    )

    st.caption("10 points per correct challenge.")

    if st.button(
        "🔄 New Round",
        key="new_function_round",
        use_container_width=True
    ):
        st.session_state.function_round += 1
        st.session_state.function_feedback = {}
        st.rerun()

    if st.button(
        "Reset Score",
        key="reset_function_score",
        use_container_width=True
    ):
        st.session_state.function_score = 0
        st.session_state.function_round += 1
        st.session_state.function_feedback = {}
        st.session_state.function_attempts = set()
        st.rerun()

# ---------------------------------
# STEP-BY-STEP SOLUTION
# ---------------------------------
with st.expander("💡 Reveal the substitution steps"):
    st.markdown("**Step 1: Start with the function**")
    st.latex(r"y=a|x-h|+k")

    st.markdown("**Step 2: Substitute the selected x-value**")
    st.latex(
        rf"y={a:g}\left|{challenge_x:g}-({h:g})\right|+({k:g})"
    )

    st.markdown("**Step 3: Evaluate the absolute value**")
    st.latex(
        rf"y={a:g}\times{abs(challenge_x-h):g}+({k:g})"
    )

    st.markdown("**Step 4: Multiply and add**")
    st.latex(rf"y={correct_y:g}")

    st.markdown("**Remember:**")
    st.write(
        "The sign of a determines the opening direction. "
        "The vertex is (h, k), and the axis of symmetry is x = h."
    )

