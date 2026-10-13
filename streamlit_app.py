/* Atlantic Coast-inspired navy and Stingray blue */
:root {
    --stingray-navy: #0B1220;
    --stingray-blue: #2563EB;
    --stingray-cyan: #38BDF8;
    --stingray-light: #EAF4FF;
}

.stApp {
    color: var(--stingray-light);
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--stingray-cyan) !important;
}

.game-card {
    border-color: rgba(56, 189, 248, 0.4);
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        var(--stingray-blue),
        #0891B2
    );
}