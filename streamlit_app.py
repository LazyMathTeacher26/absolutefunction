import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import random
import time
import math

st.set_page_config(
    page_title="Absolute Value Explorer",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# COMPACT PAGE STYLE + TOP HEADING
# ---------------------------------------------------------
st.markdown("""
<style>
/* Remove excess top whitespace while leaving Streamlit controls usable */
.stAppViewBlockContainer,
.block-container {
    padding-top: 0.35rem !important;
    padding-bottom: 0.45rem !important;
}

/* Streamlit's header can reserve space even when visually empty */
header[data-testid="stHeader"] {
    height: 0rem !important;
    min-height: 0rem !important;
}

/* Compact vertical spacing */
div[data-testid="stVerticalBlock"] {
    gap: 0.45rem;
}

/* Reduce heading margins */
h1, h2, h3 {
    margin-top: 0.1rem !important;
    margin-bottom: 0.25rem !important;
}

/* Compact horizontal rules */
hr {
    margin-top: 0.25rem !important;
    margin-bottom: 0.25rem !important;
}

/* Keep plot images from adding extra bottom whitespace */
div[data-testid="stImage"] {
    margin-bottom: 0 !important;
}
.stMarkdown p {
    margin-bottom: 0.3rem !important;
}
</style>
""", unsafe_allow_html=True)

# Render the heading as the FIRST visible element, before all page content.
# A single HTML block avoids extra height from Streamlit columns/title widgets.
st.markdown("""
<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    width:100%;
    margin:0 0 5px 0;
    padding:0;
">
  <div style="flex:1 1 auto; min-width:0;">
    <div style="font-size:clamp(1.15rem, 2.2vw, 1.65rem); font-weight:750; line-height:1.15;">
      📐 Interactive Absolute Value Explorer
    </div>
    <div style="font-size:0.82rem; color:var(--text-color); opacity:0.72; margin-top:3px;">
      Explore, experiment, and master absolute value functions.
    </div>
  </div>
  <div style="flex:0 0 auto; text-align:right; line-height:1.2; font-size:0.78rem;">
    <strong>Shirhan A. Biottong</strong><br>
    <em>Algebra 1 Teacher</em><br>
    <span style="font-size:0.65rem; opacity:0.72;">Atlantic Coast High School</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR: INTERACTIVE FUNCTION CONTROLS
# ---------------------------------------------------------
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

y = a * abs(x - h) + k
X = sp.Symbol("x")
ac, hc, kc = sp.nsimplify(a), sp.nsimplify(h), sp.nsimplify(k)
expr = sp.simplify(ac * sp.Abs(X - hc) + kc)
if ac == 1:
    expr = sp.Abs(X - hc) + kc
elif ac == -1:
    expr = -sp.Abs(X - hc) + kc
expr = sp.simplify(expr)

# ---------------------------------------------------------
# MAIN EXPLORER
# ---------------------------------------------------------
graph_col, math_col = st.columns([1.9, 0.9], gap="small")
with graph_col:
    st.latex(r"y=a|x-h|+k")
    xs = np.linspace(x_min, x_max, 1000)
    ys = a * np.abs(xs - h) + k

    fig, ax = plt.subplots(figsize=(9, 5.6))
    fig.patch.set_facecolor("#202124")
    ax.set_facecolor("#202124")
    ax.plot(xs, ys, color="deepskyblue", linewidth=2.5, label=r"$y=a|x-h|+k$")
    ax.axhline(0, color="white", linewidth=1.5)
    ax.axvline(0, color="white", linewidth=1.5)
    ax.axvline(h, color="lime", linestyle=":", linewidth=2, label=f"Symmetry: x = {h:g}")
    ax.scatter(h, k, color="red", s=85, zorder=5, label=f"Vertex ({h:g}, {k:g})")
    ax.scatter(x, y, color="yellow", edgecolors="black", s=85, zorder=6, label=f"Point ({x:g}, {y:g})")
    ax.plot([x, x], [0, y], color="yellow", linestyle="--", alpha=0.8)
    ax.plot([0, x], [y, y], color="yellow", linestyle="--", alpha=0.8)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
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
	st.markdown("")
    st.markdown("**3. Explore the Mathematics**")
    st.markdown("**Simplified Equation**")
    st.latex(rf"y={sp.latex(expr)}")
    st.markdown("<hr style='margin:3px 0;'>", unsafe_allow_html=True)
    st.markdown("**Substitution**")
    st.latex(rf"y={a:g}\left|{x:g}-({h:g})\right|+({k:g})")
    st.markdown("**Calculated y-value**")
    st.latex(rf"y={y:g}")
    st.markdown("<hr style='margin:3px 0;'>", unsafe_allow_html=True)
    st.markdown("**Key Properties**")
    st.markdown(
        f"<div style='line-height:1.25;'>"
        f"Vertex: ({h:g}, {k:g})<br>"
        f"Selected point: ({x:g}, {y:g})<br>"
        f"Axis of symmetry: x = {h:g}</div>",
        unsafe_allow_html=True,
    )
    if a > 0:
        st.markdown(f"<div style='line-height:1.25;'><br>Opens upward<br>Range: y ≥ {k:g}<br></div>", unsafe_allow_html=True)
    elif a < 0:
        st.markdown(f"<div style='line-height:1.25;'><br>Opens downward<br>Range: y ≤ {k:g}<br></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='line-height:1.25;'><br>Horizontal line<br>Range: y = {k:g}<br></div>", unsafe_allow_html=True)
    st.markdown("Domain: all real numbers.")

# ---------------------------------------------------------
# GAME STATE
# ---------------------------------------------------------
st.subheader("🎮 Absolute Value Challenge")
st.caption("Earn XP, build streaks, unlock badges, and become an Absolute Value Master.")

GAME_DEFAULTS = {
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
for key, value in GAME_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

DIFFICULTY_SETTINGS = {
    "Beginner": {"range": 3, "coefficients": [-2, -1, 1, 2], "time": 90},
    "Explorer": {"range": 5, "coefficients": [-3, -2, -1, 1, 2, 3], "time": 60},
    "Master": {"range": 9, "coefficients": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], "time": 60},
}

def generate_av_questions(difficulty):
    settings = DIFFICULTY_SETTINGS[difficulty]
    r = settings["range"]
    questions = []
    for _ in range(10):
        qa = random.choice(settings["coefficients"])
        qh = random.randint(-r, r)
        qk = random.randint(-r, r)
        qx = random.randint(-r, r)
        qy = qa * abs(qx - qh) + qk
        qexpr = sp.simplify(qa * sp.Abs(X - qh) + qk)
        questions.append({
            "a": qa, "h": qh, "k": qk, "x": qx, "y": qy,
            "opening": "Upward" if qa > 0 else "Downward",
            "expression": qexpr,
            "equation_latex": sp.latex(qexpr),
        })
    return questions

def start_new_game(difficulty):
    settings = DIFFICULTY_SETTINGS[difficulty]
    st.session_state.av_game_questions = generate_av_questions(difficulty)
    st.session_state.av_game_index = 0
    st.session_state.av_game_score = 0
    st.session_state.av_game_results = []
    st.session_state.av_game_streak = 0
    st.session_state.av_game_best_streak = 0
    st.session_state.av_game_difficulty = difficulty
    st.session_state.av_game_duration = settings["time"]
    st.session_state.av_game_deadline = time.time() + settings["time"]
    st.session_state.av_game_status = "playing"
    st.session_state.av_game_started = True
    st.session_state.av_game_session_id += 1

def submit_current_answer(index, q, student_y, student_opening):
    if len(st.session_state.av_game_results) > index:
        return
    y_correct = int(student_y) == int(q["y"])
    opening_correct = student_opening == q["opening"]
    points = (10 if y_correct else 0) + (10 if opening_correct else 0)
    new_streak = st.session_state.av_game_streak + 1 if points == 20 else 0
    st.session_state.av_game_streak = new_streak
    st.session_state.av_game_best_streak = max(
        st.session_state.av_game_best_streak, new_streak
    )
    st.session_state.av_game_score += points
    st.session_state.av_game_results.append({
        "expression": q["expression"], "a": q["a"], "h": q["h"], "k": q["k"],
        "x": q["x"], "y": q["y"], "opening": q["opening"],
        "student_y": int(student_y), "student_opening": student_opening,
        "y_correct": y_correct, "opening_correct": opening_correct,
        "points": points, "timed_out": False,
    })
    st.session_state.av_game_status = "answered"

def record_timeout(index, q):
    if len(st.session_state.av_game_results) > index:
        return
    st.session_state.av_game_results.append({
        "expression": q["expression"], "a": q["a"], "h": q["h"], "k": q["k"],
        "x": q["x"], "y": q["y"], "opening": q["opening"],
        "student_y": None, "student_opening": "No answer",
        "y_correct": False, "opening_correct": False,
        "points": 0, "timed_out": True,
    })
    st.session_state.av_game_streak = 0
    st.session_state.av_game_status = "timeout"

# ---------------------------------------------------------
# START SCREEN
# ---------------------------------------------------------
if not st.session_state.av_game_started:
    st.markdown("### 🕵️ Ready, Math Detective?")
    st.write("Each question is worth **20 points**: 10 for the y-value and 10 for the opening direction.")
    st.write("After you answer, the graph and a worked explanation will appear.")
    st.write("Choose a difficulty to begin. Beginner gives you extra time.")

    difficulty = st.selectbox(
        "Choose your level",
        ["Beginner", "Explorer", "Master"],
        index=1,
        key="av_difficulty_choice",
    )
    descriptions = {
        "Beginner": "Gentle warm-up • smaller numbers • 90 seconds per question",
        "Explorer": "Standard challenge • integers from −5 to 5 • 60 seconds per question",
        "Master": "Advanced challenge • larger coefficients and shifts • 60 seconds per question",
    }
    st.info(descriptions[difficulty])
    if st.button("🚀 Start Game", key="av_start_game", use_container_width=True, type="primary"):
        start_new_game(difficulty)
        st.rerun()

# ---------------------------------------------------------
# GAME RENDERER
# ---------------------------------------------------------
@st.fragment(run_every="1s")
def render_av_game():
    if not st.session_state.av_game_started:
        return

    questions = st.session_state.av_game_questions
    index = st.session_state.av_game_index
    total_questions = len(questions)

    if index >= total_questions:
        results = st.session_state.av_game_results
        score = st.session_state.av_game_score
        max_score = total_questions * 20
        percentage = round(score / max_score * 100) if max_score else 0
        correct_y = sum(bool(r["y_correct"]) for r in results)
        correct_opening = sum(bool(r["opening_correct"]) for r in results)
        perfect = sum(r["points"] == 20 for r in results)
        timeouts = sum(bool(r["timed_out"]) for r in results)

        if percentage >= 90:
            level_title, badge_text = "Absolute Value Master", "🏆 GOLD MASTER"
        elif percentage >= 70:
            level_title, badge_text = "Graph Explorer", "🥈 SILVER EXPLORER"
        elif percentage >= 50:
            level_title, badge_text = "Vertex Detective", "🥉 BRONZE DETECTIVE"
        else:
            level_title, badge_text = "Absolute Value Rookie", "🌱 ROOKIE ACHIEVEMENT"

        st.markdown("## 🏁 Challenge Complete!")
        if percentage >= 90:
            st.balloons()
        st.markdown(f"""
        <div class="game-card">
          <div style="font-size:1.35rem;font-weight:700;">{badge_text}</div>
          <div style="font-size:1.1rem;margin-top:0.3rem;">{level_title}</div>
          <div class="small-muted">Difficulty: {st.session_state.av_game_difficulty}</div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Final Score", f"{score} / {max_score}")
        m2.metric("Percentage", f"{percentage}%")
        m3.metric("Perfect Questions", f"{perfect} / {total_questions}")
        m4.metric("Best Streak", st.session_state.av_game_best_streak)
        st.progress(percentage / 100)

        st.markdown("### 📊 Your Learning Report")
        l1, l2, l3 = st.columns(3)
        l1.metric("Y-values correct", f"{correct_y} / {total_questions}")
        l2.metric("Opening correct", f"{correct_opening} / {total_questions}")
        l3.metric("Timed out", timeouts)

        needs_y = correct_y < total_questions
        needs_opening = correct_opening < total_questions
        if not needs_y and not needs_opening:
            st.success("🌟 Fantastic! You answered every skill correctly.")
        else:
            st.markdown("**What to practice next:**")
            if needs_y:
                st.write("• **Evaluating the function:** substitute the given x-value, calculate the absolute value first, multiply by a, then add k.")
            if needs_opening:
                st.write("• **Opening direction:** positive a opens upward; negative a opens downward.")
        st.caption(f"Time limit per question: {st.session_state.av_game_duration} seconds. Best correct-answer streak: {st.session_state.av_game_best_streak}.")

        with st.expander("📘 Review all 10 questions and worked solutions", expanded=True):
            for i, result in enumerate(results, start=1):
                st.markdown(f"**Question {i} — {result['points']} / 20 points**")
                st.latex(rf"y={sp.latex(result['expression'])}")
                st.write(f"Given x = {result['x']}")
                st.write(f"Your y-value: {result['student_y'] if result['student_y'] is not None else 'Timed out'}")
                st.write(f"Your opening: {result['student_opening']}")
                st.write(f"Correct y-value: {result['y']}")
                st.write(f"Correct opening: {result['opening']}")
                st.write(
                    f"Feedback: y-value {'correct' if result['y_correct'] else 'review needed'}; "
                    f"opening {'correct' if result['opening_correct'] else 'review needed'}."
                )
                st.latex(
                    rf"y={result['a']}|{result['x']}-({result['h']})|+({result['k']})"
                    rf"={result['a']}\cdot {abs(result['x']-result['h'])}+({result['k']})"
                    rf"={result['y']}"
                )
                gx = np.linspace(result["h"] - 6, result["h"] + 6, 300)
                gy = result["a"] * np.abs(gx - result["h"]) + result["k"]
                fig2, ax2 = plt.subplots(figsize=(5, 2.5))
                ax2.plot(gx, gy, linewidth=2, label="Function")
                ax2.axvline(result["h"], linestyle=":", linewidth=1.5, label=f"Symmetry x={result['h']}")
                ax2.scatter([result["h"]], [result["k"]], s=45, label=f"Vertex ({result['h']}, {result['k']})")
                ax2.scatter([result["x"]], [result["y"]], s=45, label=f"Point ({result['x']}, {result['y']})")
                ax2.set_title(f"Question {i}: graph reveal")
                ax2.grid(True, alpha=0.25)
                ax2.legend(fontsize=7)
                fig2.tight_layout()
                st.pyplot(fig2, use_container_width=True)
                plt.close(fig2)
                st.divider()

        st.markdown("### 🎓 Achievement Certificate")
        st.markdown(f"""
        <div class="game-card" style="text-align:center;border:2px solid #D4AF37;">
          <div style="font-size:2rem;">🏅</div>
          <div style="font-size:1.5rem;font-weight:700;">Certificate of Achievement</div>
          <p>This certifies that a student completed the Absolute Value Challenge.</p>
          <div style="font-size:1.15rem;font-weight:700;">{level_title}</div>
          <p>Score: {score} / {max_score} ({percentage}%)</p>
          <p>Difficulty: {st.session_state.av_game_difficulty} • Best streak: {st.session_state.av_game_best_streak}</p>
          <p>Absolute Value Explorer • Algebra 1</p>
          <p><strong>Shirhan A. Biottong</strong> | Atlantic Coast High School</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("To save or print the certificate, use your browser or device's Print option.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Play Again", key="av_play_again", use_container_width=True, type="primary"):
                start_new_game(st.session_state.av_game_difficulty)
                st.rerun()
        with c2:
            if st.button("🏠 Return to Explorer", key="av_return_explorer", use_container_width=True):
                st.session_state.av_game_started = False
                st.session_state.av_game_status = "waiting"
                st.rerun()
        return

    q = questions[index]
    status = st.session_state.av_game_status
    remaining = max(0, math.ceil(st.session_state.av_game_deadline - time.time()))
    if status == "playing" and remaining <= 0:
        record_timeout(index, q)
        st.rerun()

    status = st.session_state.av_game_status
    remaining = max(0, math.ceil(st.session_state.av_game_deadline - time.time()))

    st.markdown(f"### ✏️ Question {index + 1} of {total_questions}")
    st.progress(index / total_questions)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Question", f"{index + 1}/{total_questions}")
    m2.metric("Time Left", f"{remaining}s")
    m3.metric("Score", st.session_state.av_game_score)
    m4.metric("🔥 Current Streak", st.session_state.av_game_streak)

    if status == "playing" and remaining <= 10:
        st.warning("⏰ Final seconds! Check your answer.")

    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown("**Calculate the y-value and identify the opening direction.**")
    st.latex(rf"y={q['equation_latex']}")
    st.markdown(f"**Given:** x = {q['x']}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Hint: calculate the absolute value first, then multiply by a and add k.")

    if status == "playing":
        with st.form(key=f"av_answer_form_{st.session_state.av_game_session_id}_{index}"):
            answer_col, opening_col = st.columns(2)
            with answer_col:
                student_y = st.number_input("Your calculated y-value", value=0, step=1, key=f"av_student_y_{st.session_state.av_game_session_id}_{index}")
            with opening_col:
                student_opening = st.radio("The graph opens:", ["Upward", "Downward"], key=f"av_student_opening_{st.session_state.av_game_session_id}_{index}")
            submitted = st.form_submit_button("✅ Submit Answer", use_container_width=True)
        if submitted:
            submit_current_answer(index, q, student_y, student_opening)
            st.rerun()

    elif status in ("answered", "timeout"):
        if status == "answered":
            result = st.session_state.av_game_results[index]
            if result["points"] == 20:
                st.success("🎉 Perfect! Both answers are correct!")
                if st.session_state.av_game_streak >= 3:
                    st.toast(f"🔥 {st.session_state.av_game_streak} in a row! Streak bonus unlocked!", icon="🏆")
            elif result["points"] == 10:
                st.info("👍 One part is correct. Review the explanation and keep going!")
            else:
                st.warning("💡 This one is a learning opportunity. Check the steps below.")
            st.metric("Points earned", f"{result['points']} / 20")
        else:
            result = st.session_state.av_game_results[index]
            st.warning("⏰ Time is up for this question. Use the solution to learn the steps.")

        st.markdown("**Answer and explanation**")
        st.write(f"Correct y-value: **{q['y']}**")
        st.write(f"Correct opening: **{q['opening']}**")
        st.latex(
            rf"y={q['a']}|{q['x']}-({q['h']})|+({q['k']})"
            rf"={q['a']}\cdot {abs(q['x']-q['h'])}+({q['k']})"
            rf"={q['y']}"
        )

        gx = np.linspace(q["h"] - 6, q["h"] + 6, 300)
        gy = q["a"] * np.abs(gx - q["h"]) + q["k"]
        fig3, ax3 = plt.subplots(figsize=(7, 3.4))
        ax3.plot(gx, gy, color="deepskyblue", linewidth=2.5, label="Function")
        ax3.axvline(q["h"], color="limegreen", linestyle=":", linewidth=2, label=f"Line of symmetry x={q['h']}")
        ax3.scatter([q["h"]], [q["k"]], color="red", s=75, zorder=4, label=f"Vertex ({q['h']}, {q['k']})")
        ax3.scatter([q["x"]], [q["y"]], color="orange", s=75, zorder=5, label=f"Point ({q['x']}, {q['y']})")
        ax3.set_xlabel("x")
        ax3.set_ylabel("y")
        ax3.set_title("Graph Reveal")
        ax3.grid(True, alpha=0.25)
        ax3.legend(fontsize=8)
        fig3.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

        if st.button("➡️ Next Question", key=f"av_next_{st.session_state.av_game_session_id}_{index}", use_container_width=True, type="primary"):
            st.session_state.av_game_index += 1
            st.session_state.av_game_status = "playing"
            st.session_state.av_game_deadline = time.time() + st.session_state.av_game_duration
            st.rerun()

render_av_game()