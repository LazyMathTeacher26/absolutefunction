
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




# --------------------------------------------
# 6. RANDOM ABSOLUTE VALUE SPEED CHALLENGE
# 10 questions | 60 seconds per question
# --------------------------------------------

import random
import time
import streamlit as st
import sympy as sp

st.markdown("---")
st.subheader("🎮 Absolute Value Speed Challenge")

st.caption(
    "10 random functions • 60 seconds per question • "
    "Solve using pen and paper!"
)

# --------------------------------------------
# INITIALIZE GAME STATE
# --------------------------------------------

defaults = {
    "av_game_started": False,
    "av_game_questions": [],
    "av_game_index": 0,
    "av_game_score": 0,
    "av_game_deadline": 0.0,
    "av_game_status": "waiting",
    "av_game_results": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------
# GENERATE 10 RANDOM FUNCTIONS
# --------------------------------------------

def generate_av_questions():
    questions = []

    for _ in range(10):
        a = random.choice([-3, -2, -1, 1, 2, 3])
        h = random.randint(-5, 5)
        k = random.randint(-5, 5)
        x = random.randint(-5, 5)

        y = a * abs(x - h) + k

        X = sp.Symbol("x")
        expression = sp.simplify(
            a * sp.Abs(X - h) + k
        )

        questions.append({
            "a": a,
            "h": h,
            "k": k,
            "x": x,
            "y": y,
            "opening": "Upward" if a > 0 else "Downward",
            "equation": sp.latex(expression),
        })

    return questions


# --------------------------------------------
# START GAME
# --------------------------------------------

if not st.session_state.av_game_started:
    st.markdown("### 🕵️ Ready, Math Detective?")

    st.write("Each question is worth 20 points:")
    st.write("• 10 points for the correct y-value")
    st.write("• 10 points for the correct opening direction")
    st.write("⏱️ You have 1 minute (60 seconds) per question.")
    st.write("")

    if st.button(
        "🚀 Start Game",
        key="av_start_game",
        use_container_width=True
    ):
        st.session_state.av_game_questions = generate_av_questions()
        st.session_state.av_game_index = 0
        st.session_state.av_game_score = 0
        st.session_state.av_game_results = []
        st.session_state.av_game_status = "playing"
        st.session_state.av_game_deadline = time.time() + 60
        st.session_state.av_game_started = True
        st.rerun()


# --------------------------------------------
# GAME INTERFACE AND LIVE COUNTDOWN
# --------------------------------------------

@st.fragment(run_every="1s")
def render_av_game():

    if not st.session_state.av_game_started:
        return

    questions = st.session_state.av_game_questions
    index = st.session_state.av_game_index

    # ----------------------------------------
    # GAME COMPLETION
    # ----------------------------------------

    if index >= 10:
        st.success("🏁 Game complete!")

        score = st.session_state.av_game_score
        st.metric("Final Score", f"{score} / 200")

        percentage = score / 200 * 100
        st.write(f"Final percentage: {percentage:.0f}%")

        if percentage >= 90:
            st.balloons()
            st.write("🏆 Outstanding! Absolute Value Master!")
        elif percentage >= 70:
            st.write("👏 Great work!")
        else:
            st.write("💪 Keep practicing!")

        with st.expander("📘 Review all 10 questions"):
            for i, result in enumerate(
                st.session_state.av_game_results, start=1
            ):
                st.markdown(f"**Question {i}**")
                st.latex(
                    rf"y={sp.latex(result['expression'])}"
                )
                st.write(f"Given x: {result['x']}")
                st.write(f"Correct y-value: {result['y']}")
                st.write(f"Correct opening: {result['opening']}")
                st.write(f"Your y-answer: {result['student_y']}")
                st.write(
                    f"Your opening answer: "
                    f"{result['student_opening']}"
                )
                st.write(f"Points earned: {result['points']} / 20")
                st.divider()

        if st.button(
            "🔄 Play Again",
            key="av_play_again",
            use_container_width=True
        ):
            st.session_state.av_game_questions = generate_av_questions()
            st.session_state.av_game_index = 0
            st.session_state.av_game_score = 0
            st.session_state.av_game_results = []
            st.session_state.av_game_status = "playing"
            st.session_state.av_game_deadline = time.time() + 60
            st.rerun()

        return

    q = questions[index]

    # ----------------------------------------
    # TIMER
    # ----------------------------------------

    remaining = max(
        0,
        int(
            st.session_state.av_game_deadline
            - time.time()
            + 0.999
        )
    )

    if (
        st.session_state.av_game_status == "playing"
        and remaining <= 0
    ):
        st.session_state.av_game_status = "timeout"
        st.rerun()

    # ----------------------------------------
    # PROGRESS, TIME, SCORE
    # ----------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric("Question", f"{index + 1} / 10")
    c2.metric("Time Left", f"{remaining} sec")
    c3.metric("Score", st.session_state.av_game_score)

    st.progress((index + 1) / 10)

    # ----------------------------------------
    # RANDOM QUESTION
    # ----------------------------------------

    st.markdown(f"### ✏️ Question {index + 1}")
    st.write("Calculate y and identify the graph's opening.")

    st.latex(rf"y={q['equation']}")
    st.markdown(f"**Given:** x = {q['x']}")

    st.caption(
        "Work on paper. The substitution steps are hidden "
        "until the game ends."
    )

    # ----------------------------------------
    # STUDENT ANSWERS
    # ----------------------------------------

    if st.session_state.av_game_status == "playing":

        answer_col, opening_col = st.columns(2)

        with answer_col:
            student_y = st.number_input(
                "Your calculated y-value",
                value=0,
                step=1,
                key=f"av_student_y_{index}"
            )

        with opening_col:
            student_opening = st.radio(
                "The graph opens:",
                ["Upward", "Downward"],
                key=f"av_student_opening_{index}"
            )

        if st.button(
            "✅ Submit Answer",
            key=f"av_submit_{index}",
            use_container_width=True
        ):
            y_correct = int(student_y) == q["y"]
            opening_correct = student_opening == q["opening"]

            points = (
                (10 if y_correct else 0)
                + (10 if opening_correct else 0)
            )

            X = sp.Symbol("x")
            expression = sp.simplify(
                q["a"] * sp.Abs(X - q["h"]) + q["k"]
            )

            st.session_state.av_game_score += points

            st.session_state.av_game_results.append({
                "expression": expression,
                "a": q["a"],
                "h": q["h"],
                "k": q["k"],
                "x": q["x"],
                "y": q["y"],
                "opening": q["opening"],
                "student_y": student_y,
                "student_opening": student_opening,
                "points": points,
            })

            st.session_state.av_game_status = "answered"
            st.rerun()

    # ----------------------------------------
    # TIMEOUT FEEDBACK
    # ----------------------------------------

    elif st.session_state.av_game_status == "timeout":
        st.warning("⏰ Time is up! No points for this question.")

        X = sp.Symbol("x")
        expression = sp.simplify(
            q["a"] * sp.Abs(X - q["h"]) + q["k"]
        )

        if (
            not st.session_state.av_game_results
            or len(st.session_state.av_game_results) <= index
        ):
            st.session_state.av_game_results.append({
                "expression": expression,
                "a": q["a"],
                "h": q["h"],
                "k": q["k"],
                "x": q["x"],
                "y": q["y"],
                "opening": q["opening"],
                "student_y": "Timed out",
                "student_opening": "Timed out",
                "points": 0,
            })

        st.write(f"Correct y-value: {q['y']}")
        st.write(f"Correct opening: {q['opening']}")

    # ----------------------------------------
    # SUBMITTED ANSWER FEEDBACK
    # ----------------------------------------

    elif st.session_state.av_game_status == "answered":
        result = st.session_state.av_game_results[-1]

        if result["points"] == 20:
            st.success("🎉 Both answers are correct!")
        elif result["points"] == 10:
            st.info("👍 One answer is correct. Keep going!")
        else:
            st.warning("Review the correct answers below.")

        st.write(f"Correct y-value: {q['y']}")
        st.write(f"Correct opening: {q['opening']}")
        st.write(f"Points earned: {result['points']} / 20")

    # ----------------------------------------
    # NEXT QUESTION
    # ----------------------------------------

    if st.session_state.av_game_status in ("answered", "timeout"):

        if st.button(
            "➡️ Next Question",
            key=f"av_next_{index}",
            use_container_width=True
        ):
            st.session_state.av_game_index += 1
            st.session_state.av_game_status = "playing"
            st.session_state.av_game_deadline = time.time() + 60
            st.rerun()


render_av_game()
