
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random
import time
import math
from pathlib import Path

# =========================================================
# STINGRAY ORANGE THEME
# =========================================================
st.markdown("""
<style>
.stApp {
 background: radial-gradient(circle at 50% 0%, rgba(255,185,92,.20), transparent 42%),
             linear-gradient(145deg,#321608 0%,#211710 45%,#151515 100%);
 color:#fff;
}
.stAppViewBlockContainer,.block-container {max-width:1600px;padding-top:.65rem!important;padding-bottom:1.2rem!important}
header[data-testid="stHeader"] {background:transparent;height:2.5rem}
h1,h2,h3 {color:#fff!important;letter-spacing:-.025em;font-weight:750!important;margin-top:.15rem!important;margin-bottom:.4rem!important}
p {color:#F3E7DD;margin-bottom:.4rem!important}
div[data-testid="stVerticalBlock"] {gap:.65rem}
hr {border-color:rgba(255,153,51,.35)!important;margin:.4rem 0!important}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#49200D,#24150E);border-right:1px solid rgba(255,153,51,.35)}
section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3 {color:#FFAD55!important}
section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] .stCaption {color:#F3E7DD!important}
.stNumberInput input,.stTextInput input,.stSelectbox div[data-baseweb="select"] {border-radius:10px}
.stButton>button,.stFormSubmitButton>button {min-height:2.65rem;border-radius:12px;font-weight:700;border:1px solid rgba(255,153,51,.65);transition:all .2s}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"] {background:linear-gradient(135deg,#FF9D24,#E85D04);color:#fff;border:none;box-shadow:0 5px 18px rgba(232,93,4,.28)}
.stButton>button:hover,.stFormSubmitButton>button:hover {border-color:#FFD08A;transform:translateY(-1px)}
div[data-testid="stMetric"] {background:rgba(73,39,22,.88);border:1px solid rgba(255,153,51,.35);border-radius:14px;padding:14px}
div[data-testid="stMetricLabel"] {color:#E7C9B0!important}
div[data-testid="stMetricValue"] {color:#FFAD55!important;font-weight:750}
div[data-testid="stAlert"] {border-radius:12px}
div[data-testid="stExpander"] {background:rgba(40,29,23,.88);border:1px solid rgba(255,153,51,.32);border-radius:14px;overflow:hidden}
.game-card {background:linear-gradient(135deg,rgba(111,52,20,.96),rgba(35,29,26,.98));border:1px solid rgba(255,173,85,.55);border-radius:18px;padding:20px;margin:8px 0 14px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.small-muted {color:#D6B7A0;font-size:.85rem}
div[data-testid="stProgress"]>div>div {background:linear-gradient(90deg,#FFB347,#E85D04)}
div[data-testid="stMarkdownContainer"] {line-height:1.5}
@media(max-width:700px){.stAppViewBlockContainer,.block-container{padding-left:.75rem!important;padding-right:.75rem!important}.game-card{padding:15px;border-radius:14px}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;width:100%;margin:0 0 8px;padding:8px 0">
 <div style="flex:1;min-width:0">
  <div style="font-size:clamp(1.15rem,2.2vw,1.65rem);font-weight:750;color:#fff">📐 Interactive Absolute Value Explorer</div>
  <div style="font-size:.85rem;color:#FFB347;margin-top:5px">Explore, experiment, and master absolute value functions.</div>
 </div>
 <div style="text-align:right;line-height:1.4;font-size:.78rem;color:#FFF0E2;flex:0 0 auto">
  <strong>Shirhan A. Biottong</strong><br><em>Algebra 1 Teacher</em><br>
  <span style="font-size:.65rem;color:#D6B7A0">Atlantic Coast High School</span>
 </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# NARRATED ABSOLUTE VALUE VIDEO LESSON
# =========================================================
st.markdown("## 🎬 Watch the Lesson")
st.markdown(
    "Watch the lesson, then use the interactive graph below "
    "to explore how **a**, **h**, and **k** change the function."
)

video_path = Path(__file__).parent / "AbsoluteValueParameter.mp4"

if video_path.is_file():
    st.video(str(video_path))
else:
    st.warning(
        "Video not found. Please place "
        "`AbsoluteValueParameter.mp4` in the same folder "
        "as `streamlit_app.py`."
    )

st.divider()

# =========================================================
# EXPLORER CONTROLS
# =========================================================
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

if x_min >= x_max or y_min >= y_max:
    st.error("Each minimum must be less than its maximum.")
    st.stop()


# =========================================================
# EQUATION HELPERS
# =========================================================
def fmt(v):
    v = float(v)
    return str(int(v)) if v.is_integer() else f"{v:g}"


def abs_equation(a_val, h_val, k_val, variable="x"):
    a_val, h_val, k_val = (
        float(a_val),
        float(h_val),
        float(k_val)
    )

    inside = variable if h_val == 0 else (
        f"{variable}-{fmt(h_val)}"
        if h_val > 0
        else f"{variable}+{fmt(abs(h_val))}"
    )

    if a_val == 0:
        return rf"y={fmt(k_val)}"

    coefficient = (
        ""
        if a_val == 1
        else "-"
        if a_val == -1
        else fmt(a_val)
    )

    shift = (
        f"+{fmt(k_val)}"
        if k_val > 0
        else fmt(k_val)
        if k_val < 0
        else ""
    )

    return rf"y={coefficient}\left|{inside}\right|{shift}"


y = a * abs(x - h) + k
X = sp.Symbol("x")
expr = sp.simplify(
    sp.nsimplify(a) * sp.Abs(X - sp.nsimplify(h))
    + sp.nsimplify(k)
)


# =========================================================
# MAIN EXPLORER GRAPH + MATH
# =========================================================
graph_col, math_col = st.columns([1.8, 1], gap="small")

with graph_col:
    xs = np.linspace(x_min, x_max, 1000)
    ys = a * np.abs(xs - h) + k

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#211710")
    ax.set_facecolor("#30241D")

    ax.plot(
        xs,
        ys,
        color="#FF9D24",
        linewidth=3,
        label=r"$y=a|x-h|+k$"
    )

    ax.axhline(0, color="white", linewidth=1.5)
    ax.axvline(0, color="white", linewidth=1.5)

    ax.axvline(
        h,
        color="#A3E635",
        linestyle=":",
        linewidth=2,
        label=f"Symmetry: x={h:g}"
    )

    ax.scatter(
        h, k,
        color="white",
        edgecolors="#E85D04",
        linewidths=2,
        s=90,
        zorder=5,
        label=f"Vertex ({h:g}, {k:g})"
    )

    ax.scatter(
        x, y,
        color="#FFD43B",
        edgecolors="#211710",
        s=90,
        zorder=6,
        label=f"Point ({x:g}, {y:g})"
    )

    ax.plot(
        [x, x], [0, y],
        color="#FFD43B",
        linestyle="--",
        alpha=.8
    )

    ax.plot(
        [0, x], [y, y],
        color="#FFD43B",
        linestyle="--",
        alpha=.8
    )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.set_xticks(
        np.arange(np.ceil(x_min), np.floor(x_max) + 1, 1)
    )
    ax.set_yticks(
        np.arange(np.ceil(y_min), np.floor(y_max) + 1, 1)
    )

    ax.tick_params(colors="white", labelsize=8)
    ax.grid(True, color="white", alpha=.18)

    for spine in ax.spines.values():
        spine.set_color("white")

    ax.set_xlabel("x-axis", color="white")
    ax.set_ylabel("y-axis", color="white")
    ax.set_title("Absolute Value Function", color="white")

    legend = ax.legend(loc="best", fontsize=7)
    legend.get_frame().set_facecolor("#49271A")
    legend.get_frame().set_edgecolor("#FFAD55")

    for label in legend.get_texts():
        label.set_color("white")

    fig.tight_layout(pad=.7)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.latex(r"y=a|x-h|+k")


with math_col:
    st.markdown("### 3. Explore the Mathematics")

    st.markdown("**Simplified Equation**")
    st.latex(abs_equation(a, h, k))

    st.markdown("**Substitution**")
    st.latex(abs_equation(a, h, k).replace("x", fmt(x), 1))

    st.markdown("**Calculated y-value**")
    st.latex(rf"y={fmt(y)}")

    st.markdown("**Key Properties**")

    opening = (
        "Opens upward"
        if a > 0
        else "Opens downward"
        if a < 0
        else "Horizontal line"
    )

    range_text = (
        f"Range: y ≥ {k:g}"
        if a > 0
        else f"Range: y ≤ {k:g}"
        if a < 0
        else f"Range: y = {k:g}"
    )

    st.markdown(
        f"Vertex: ({h:g}, {k:g})  \n"
        f"Selected point: ({x:g}, {y:g})  \n"
        f"Axis of symmetry: x = {h:g}  \n"
        f"{opening}  \n"
        f"{range_text}  \n"
        f"Domain: all real numbers."
    )


st.divider()
st.subheader("🎮 Stingray Absolute Value Challenge")
st.caption(
    "Earn XP, build streaks, unlock badges, "
    "and become an Absolute Value Master."
)


# =========================================================
# GAME STATE
# =========================================================
DEFAULTS = {
    "av_game_started": False,
    "av_game_questions": [],
    "av_game_index": 0,
    "av_game_score": 0,
    "av_game_deadline": 0.0,
    "av_game_status": "waiting",
    "av_game_results": [],
    "av_game_streak": 0,
    "av_game_best_streak": 0,
    "av_game_difficulty": "Explorer",
    "av_game_duration": 60,
    "av_game_session_id": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


DIFFICULTY = {
    "Beginner": {
        "range": 3,
        "coefficients": [-2, -1, 1, 2],
        "time": 90
    },
    "Explorer": {
        "range": 5,
        "coefficients": [-3, -2, -1, 1, 2, 3],
        "time": 60
    },
    "Master": {
        "range": 9,
        "coefficients": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5],
        "time": 60
    },
}


def game_equation(a_val, h_val, k_val):
    return abs_equation(a_val, h_val, k_val)


def calculation_latex(a_val, x_val, h_val, k_val, y_val):
    inside = (
        f"{fmt(x_val)}+{fmt(abs(h_val))}"
        if h_val < 0
        else f"{fmt(x_val)}-{fmt(h_val)}"
        if h_val > 0
        else fmt(x_val)
    )

    distance = abs(x_val - h_val)

    shift = (
        f"+{fmt(k_val)}"
        if k_val > 0
        else fmt(k_val)
        if k_val < 0
        else ""
    )

    if a_val == 1:
        first = f"|{inside}|{shift}"
        second = f"{fmt(distance)}{shift}"

    elif a_val == -1:
        first = f"-|{inside}|{shift}"
        second = f"-{fmt(distance)}{shift}"

    else:
        first = f"{fmt(a_val)}\\left|{inside}\\right|{shift}"
        second = f"{fmt(a_val)}\\cdot {fmt(distance)}{shift}"

    return rf"y={first}={second}={fmt(y_val)}"


def generate_questions(level):
    settings = DIFFICULTY[level]
    r = settings["range"]
    questions = []

    for _ in range(10):
        qa = random.choice(settings["coefficients"])
        qh = random.randint(-r, r)
        qk = random.randint(-r, r)
        qx = random.randint(-r, r)
        qy = qa * abs(qx - qh) + qk

        questions.append({
            "a": qa,
            "h": qh,
            "k": qk,
            "x": qx,
            "y": qy,
            "opening": "Upward" if qa > 0 else "Downward",
            "equation_latex": game_equation(qa, qh, qk),
        })

    return questions


def start_game(level):
    st.session_state.av_game_questions = generate_questions(level)
    st.session_state.av_game_index = 0
    st.session_state.av_game_score = 0
    st.session_state.av_game_results = []
    st.session_state.av_game_streak = 0
    st.session_state.av_game_best_streak = 0
    st.session_state.av_game_difficulty = level
    st.session_state.av_game_duration = DIFFICULTY[level]["time"]
    st.session_state.av_game_deadline = (
        time.time() + DIFFICULTY[level]["time"]
    )
    st.session_state.av_game_status = "playing"
    st.session_state.av_game_started = True
    st.session_state.av_game_session_id += 1


def submit_answer(index, q, student_y, student_opening):
    if len(st.session_state.av_game_results) > index:
        return

    y_ok = int(student_y) == int(q["y"])
    opening_ok = student_opening == q["opening"]

    points = (10 if y_ok else 0) + (10 if opening_ok else 0)

    streak = (
        st.session_state.av_game_streak + 1
        if points == 20
        else 0
    )

    st.session_state.av_game_streak = streak

    st.session_state.av_game_best_streak = max(
        st.session_state.av_game_best_streak,
        streak
    )

    st.session_state.av_game_score += points

    st.session_state.av_game_results.append({
        **q,
        "student_y": int(student_y),
        "student_opening": student_opening,
        "y_correct": y_ok,
        "opening_correct": opening_ok,
        "points": points,
        "timed_out": False,
    })

    st.session_state.av_game_status = "answered"


def timeout_answer(index, q):
    if len(st.session_state.av_game_results) > index:
        return

    st.session_state.av_game_results.append({
        **q,
        "student_y": None,
        "student_opening": "No answer",
        "y_correct": False,
        "opening_correct": False,
        "points": 0,
        "timed_out": True,
    })

    st.session_state.av_game_streak = 0
    st.session_state.av_game_status = "timeout"


# =========================================================
# GAME START SCREEN
# =========================================================
if not st.session_state.av_game_started:
    st.markdown("### 🕵️ Ready, Math Detective?")

    st.write(
        "Each question is worth **20 points**: "
        "10 for the y-value and 10 for the opening direction."
    )

    st.write(
        "After you answer, one graph and a worked explanation will appear."
    )

    level = st.selectbox(
        "Choose your level",
        ["Beginner", "Explorer", "Master"],
        index=1,
        key="av_difficulty_choice"
    )

    descriptions = {
        "Beginner": (
            "Gentle warm-up • smaller numbers • "
            "90 seconds per question"
        ),
        "Explorer": (
            "Standard challenge • integers from −5 to 5 • "
            "60 seconds per question"
        ),
        "Master": (
            "Advanced challenge • larger coefficients and shifts • "
            "60 seconds per question"
        ),
    }

    st.info(descriptions[level])

    if st.button(
        "🚀 Start Stingray Challenge",
        key="av_start_game",
        use_container_width=True,
        type="primary"
    ):
        start_game(level)
        st.rerun()


# =========================================================
# GAME RENDERER
# =========================================================
@st.fragment(run_every="1s")
def render_game():
    if not st.session_state.av_game_started:
        return

    questions = st.session_state.av_game_questions
    index = st.session_state.av_game_index
    total = len(questions)

    # -----------------------------------------------------
    # COMPLETION SCREEN
    # -----------------------------------------------------
    if index >= total:
        results = st.session_state.av_game_results
        score = st.session_state.av_game_score
        max_score = total * 20

        pct = round(score / max_score * 100) if max_score else 0

        correct_y = sum(bool(r["y_correct"]) for r in results)
        correct_open = sum(
            bool(r["opening_correct"]) for r in results
        )
        perfect = sum(r["points"] == 20 for r in results)
        timed_out = sum(bool(r["timed_out"]) for r in results)

        if pct >= 90:
            title, badge = "Absolute Value Master", "🏆 GOLD MASTER"
        elif pct >= 70:
            title, badge = "Graph Explorer", "🥈 SILVER EXPLORER"
        elif pct >= 50:
            title, badge = "Vertex Detective", "🥉 BRONZE DETECTIVE"
        else:
            title, badge = "Absolute Value Rookie", "🌱 ROOKIE ACHIEVEMENT"

        st.markdown("## 🏁 Challenge Complete!")

        if pct >= 90:
            st.balloons()

        st.markdown(
            f'<div class="game-card">'
            f'<div style="font-size:1.35rem;font-weight:700">{badge}</div>'
            f'<div style="font-size:1.1rem">{title}</div>'
            f'<div class="small-muted">Difficulty: '
            f'{st.session_state.av_game_difficulty}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Final Score", f"{score} / {max_score}")
        m2.metric("Percentage", f"{pct}%")
        m3.metric("Perfect Questions", f"{perfect} / {total}")
        m4.metric("Best Streak", st.session_state.av_game_best_streak)

        st.progress(pct / 100)

        st.markdown("### 📊 Your Learning Report")

        l1, l2, l3 = st.columns(3)
        l1.metric("Y-values correct", f"{correct_y} / {total}")
        l2.metric("Opening correct", f"{correct_open} / {total}")
        l3.metric("Timed out", timed_out)

        if correct_y == total and correct_open == total:
            st.success("🌟 Fantastic! You answered every skill correctly.")
        else:
            st.markdown("**What to practice next:**")

            if correct_y < total:
                st.write(
                    "• **Evaluating:** calculate the absolute value first, "
                    "multiply by a, then add k."
                )

            if correct_open < total:
                st.write(
                    "• **Opening direction:** positive a opens upward; "
                    "negative a opens downward."
                )

        with st.expander(
            "📘 Review all 10 questions and worked solutions",
            expanded=True
        ):
            for i, r in enumerate(results, 1):
                st.markdown(
                    f"**Question {i} — {r['points']} / 20 points**"
                )
                st.latex(r["equation_latex"])
                st.write(f"Given x = {r['x']}")

                st.write(
                    "Your y-value: "
                    f"{r['student_y'] if r['student_y'] is not None else 'Timed out'}"
                )

                st.write(f"Your opening: {r['student_opening']}")
                st.write(f"Correct y-value: {r['y']}")
                st.write(f"Correct opening: {r['opening']}")

                st.latex(
                    calculation_latex(
                        r["a"], r["x"], r["h"], r["k"], r["y"]
                    )
                )

                st.divider()

        # -------------------------------------------------
        # ACHIEVEMENT CERTIFICATE
        # -------------------------------------------------
        st.markdown("### 🎓 Achievement Certificate")

        st.markdown(f"""
        <div class="game-card" style="text-align:center;border:2px solid #FFAD55">
          <div style="font-size:2rem">🏅</div>
          <div style="font-size:1.5rem;font-weight:700">Stingray Certificate of Achievement</div>
          <p>This certifies that a student completed the Absolute Value Challenge.</p>
          <div style="font-size:1.15rem;font-weight:700">{title}</div>
          <p>Score: {score} / {max_score} ({pct}%)</p>
          <p>Difficulty: {st.session_state.av_game_difficulty} • Best streak: {st.session_state.av_game_best_streak}</p>
          <p>Absolute Value Explorer • Algebra 1</p>
          <p><strong>Shirhan A. Biottong</strong> | Atlantic Coast High School</p>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            "To save or print the certificate, use your browser "
            "or device's Print option."
        )

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "🔄 Play Again",
                key="av_play_again",
                use_container_width=True,
                type="primary"
            ):
                start_game(st.session_state.av_game_difficulty)
                st.rerun()

        with c2:
            if st.button(
                "🏠 Return to Explorer",
                key="av_return_explorer",
                use_container_width=True
            ):
                st.session_state.av_game_started = False
                st.session_state.av_game_status = "waiting"
                st.rerun()

        return

    # -----------------------------------------------------
    # CURRENT QUESTION
    # -----------------------------------------------------
    q = questions[index]
    status = st.session_state.av_game_status

    remaining = max(
        0,
        math.ceil(st.session_state.av_game_deadline - time.time())
    )

    if status == "playing" and remaining <= 0:
        timeout_answer(index, q)
        st.rerun()
        return

    status = st.session_state.av_game_status

    remaining = max(
        0,
        math.ceil(st.session_state.av_game_deadline - time.time())
    )

    st.markdown(f"### ✏️ Question {index + 1} of {total}")
    st.progress(index / total)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Question", f"{index + 1}/{total}")
    m2.metric("Time Left", f"{remaining}s")
    m3.metric("Score", st.session_state.av_game_score)
    m4.metric("🔥 Current Streak", st.session_state.av_game_streak)

    if status == "playing" and remaining <= 10:
        st.warning("⏰ Final seconds! Check your answer.")

    st.markdown("""
    <div class="game-card" style="text-align:center;padding:24px 16px">
      <div style="font-size:.85rem;color:#FFB347;margin-bottom:12px;letter-spacing:.08em;font-weight:700">STINGRAY MATH CHALLENGE</div>
      <div style="font-size:1.05rem;font-weight:700;color:#fff">Calculate the y-value and identify the opening direction.</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(q["equation_latex"])
    st.markdown(f"**Given:** \\(x={q['x']}\\)")
    st.caption(
        "Hint: calculate the absolute value first, "
        "then multiply by a and add k."
    )

    # -----------------------------------------------------
    # ANSWER FORM
    # -----------------------------------------------------
    if status == "playing":
        with st.form(
            key=f"av_answer_form_{st.session_state.av_game_session_id}_{index}"
        ):
            ca, cb = st.columns(2)

            with ca:
                student_y = st.number_input(
                    "Your calculated y-value",
                    value=0,
                    step=1,
                    key=f"av_student_y_{st.session_state.av_game_session_id}_{index}"
                )

            with cb:
                student_opening = st.radio(
                    "The graph opens:",
                    ["Upward", "Downward"],
                    key=f"av_student_opening_{st.session_state.av_game_session_id}_{index}"
                )

            submitted = st.form_submit_button(
                "✅ Submit Answer",
                use_container_width=True
            )

        if submitted:
            submit_answer(index, q, student_y, student_opening)
            st.rerun()

    # -----------------------------------------------------
    # ANSWER FEEDBACK AND GRAPH REVEAL
    # -----------------------------------------------------
    elif status in ("answered", "timeout"):
        result = st.session_state.av_game_results[index]

        if status == "answered":
            if result["points"] == 20:
                st.success("🎉 Perfect! Both answers are correct!")

                if st.session_state.av_game_streak >= 3:
                    st.toast(
                        f"🔥 {st.session_state.av_game_streak} in a row! "
                        "Streak bonus unlocked!",
                        icon="🏆"
                    )

            elif result["points"] == 10:
                st.info(
                    "👍 One part is correct. Review the explanation "
                    "and keep going!"
                )

            else:
                st.warning(
                    "💡 This one is a learning opportunity. "
                    "Check the steps below."
                )

            st.metric("Points earned", f"{result['points']} / 20")

        else:
            st.warning(
                "⏰ Time is up for this question. "
                "Use the solution to learn the steps."
            )

        st.markdown("**Answer and explanation**")
        st.write(f"Correct y-value: **{q['y']}**")
        st.write(f"Correct opening: **{q['opening']}**")

        st.latex(
            calculation_latex(
                q["a"], q["x"], q["h"], q["k"], q["y"]
            )
        )

        # Exactly ONE graph is shown for this answered question.
        gx = np.linspace(q["h"] - 6, q["h"] + 6, 300)
        gy = q["a"] * np.abs(gx - q["h"]) + q["k"]

        fig, ax = plt.subplots(figsize=(7, 3.4))
        fig.patch.set_facecolor("#211710")
        ax.set_facecolor("#30241D")

        ax.plot(
            gx, gy,
            color="#FF9D24",
            linewidth=2.5,
            label="Function"
        )

        ax.axvline(
            q["h"],
            color="#A3E635",
            linestyle=":",
            linewidth=2,
            label=f"Line of symmetry x={fmt(q['h'])}"
        )

        ax.scatter(
            [q["h"]], [q["k"]],
            color="white",
            edgecolors="#E85D04",
            linewidths=2,
            s=75,
            zorder=4,
            label=f"Vertex ({fmt(q['h'])}, {fmt(q['k'])})"
        )

        ax.scatter(
            [q["x"]], [q["y"]],
            color="#FFD43B",
            edgecolors="#211710",
            s=75,
            zorder=5,
            label=f"Point ({fmt(q['x'])}, {fmt(q['y'])})"
        )

        ax.set_xlabel("x", color="white")
        ax.set_ylabel("y", color="white")
        ax.set_title("Stingray Graph Reveal", color="white")
        ax.tick_params(colors="white")
        ax.grid(True, color="white", alpha=.2)

        for spine in ax.spines.values():
            spine.set_color("white")

        leg = ax.legend(fontsize=8)
        leg.get_frame().set_facecolor("#49271A")
        leg.get_frame().set_edgecolor("#FFAD55")

        for label in leg.get_texts():
            label.set_color("white")

        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        if st.button(
            "➡️ Next Question",
            key=f"av_next_{st.session_state.av_game_session_id}_{index}",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.av_game_index += 1
            st.session_state.av_game_status = "playing"
            st.session_state.av_game_deadline = (
                time.time() + st.session_state.av_game_duration
            )
            st.rerun()


# =========================================================
# RUN THE GAME
# =========================================================
render_game()
