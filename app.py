
import re
import streamlit as st

st.set_page_config(
    page_title="AgentIF-Lite",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AgentIF-Lite")
st.subheader("AI Instruction Compliance Evaluator")

st.write(
    "Evaluate whether a response follows measurable task instructions."
)

instructions = st.text_area(
    "Task instructions",
    placeholder=(
        "Example: Write exactly 3 bullet points. "
        "Use no more than 60 words."
    )
)

response = st.text_area(
    "AI response",
    placeholder="Paste the response you want to evaluate."
)


def evaluate_response(instructions, response):
    checks = []

    # Check for an exact bullet-point count.
    bullet_match = re.search(
        r"exactly\s+(\d+)\s+bullet points?",
        instructions,
        re.IGNORECASE
    )

    if bullet_match:
        expected = int(bullet_match.group(1))
        actual = sum(
            1 for line in response.splitlines()
            if re.match(r"^\s*[-*•]\s+", line)
        )

        checks.append({
            "constraint": f"Exactly {expected} bullet points",
            "passed": actual == expected,
            "details": f"Found {actual} bullet points."
        })

    # Check for a maximum word count.
    word_match = re.search(
        r"(?:no more than|at most|under)\s+(\d+)\s+words?",
        instructions,
        re.IGNORECASE
    )

    if word_match:
        limit = int(word_match.group(1))
        actual_words = len(response.split())

        checks.append({
            "constraint": f"Maximum {limit} words",
            "passed": actual_words <= limit,
            "details": f"Found {actual_words} words."
        })

    # Check whether required keywords are present.
    keyword_match = re.search(
        r"include the keywords?\s+(.+?)(?:[.!?\n]|$)",
        instructions,
        re.IGNORECASE
    )

    if keyword_match:
        keywords = re.findall(
            r'"([^"]+)"|\'([^\']+)\'|([\w-]+)',
            keyword_match.group(1)
        )

        for groups in keywords:
            keyword = next(part for part in groups if part)

            passed = keyword.casefold() in response.casefold()

            checks.append({
                "constraint": f"Include '{keyword}'",
                "passed": passed,
                "details": (
                    "Keyword found." if passed
                    else "Keyword missing."
                )
            })

    if not checks:
        return [], 0.0, 0.0

    csr = (
        sum(check["passed"] for check in checks)
        / len(checks)
    ) * 100

    isr = 100.0 if all(
        check["passed"] for check in checks
    ) else 0.0

    return checks, csr, isr


if st.button("Evaluate Response"):
    if not instructions.strip() or not response.strip():
        st.warning("Please enter both instructions and a response.")
    else:
        checks, csr, isr = evaluate_response(
            instructions, response
        )

        if not checks:
            st.warning(
                "No supported measurable constraint was detected. "
                "Try an exact bullet count, a word limit, "
                "or a required keyword."
            )
        else:
            st.subheader("Evaluation Results")

            for check in checks:
                if check["passed"]:
                    st.success(
                        f"PASS — {check['constraint']}. "
                        f"{check['details']}"
                    )
                else:
                    st.error(
                        f"FAIL — {check['constraint']}. "
                        f"{check['details']}"
                    )

            col1, col2 = st.columns(2)

            col1.metric("CSR", f"{csr:.1f}%")
            col2.metric("ISR", f"{isr:.1f}%")

            st.caption(
                "CSR = satisfied constraints / detected constraints. "
                "ISR = 100% if all detected constraints pass; "
                "otherwise 0% for this single instruction."
            )

