import streamlit as st
from transformers import pipeline

MODEL = "google/gemma-3-1b-it"

st.set_page_config(
    page_title="WriteFlow",
    page_icon="✦",
    layout="centered",
)

st.markdown(
    """
    <style>
        #MainMenu, footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        .block-container {
            max-width: 850px;
            padding-top: 2rem;
            padding-bottom: 7rem;
        }

        .brand {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .tagline {
            color: #777;
            font-size: 0.9rem;
            margin-top: -0.25rem;
            margin-bottom: 2rem;
        }

        .example-card {
            padding: 1rem 1.1rem;
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 12px;
            margin-bottom: 0.75rem;
        }

        .example-title {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .example-text {
            color: #777;
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### WriteFlow")
    st.caption("Your local AI writing assistant")

    st.divider()

    st.markdown("**Capabilities**")
    st.caption("Rewrite")
    st.caption("Summarize")
    st.caption("Improve grammar")
    st.caption("Change tone")
    st.caption("Transform text")

    st.divider()

    st.markdown("**About**")
    st.caption("Powered by Gemma 3 1B")
    st.caption("Hugging Face Transformers")
    st.caption("Runs locally on your computer")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model=MODEL,
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="brand">WriteFlow</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">Rewrite, refine, and transform your text.</div>',
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown("#### What would you like to improve?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="example-card">
                <div class="example-title">Rewrite professionally</div>
                <div class="example-text">
                    Turn an informal message into a polished one.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="example-card">
                <div class="example-title">Improve grammar</div>
                <div class="example-text">
                    Fix grammar while keeping the original meaning.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="example-card">
                <div class="example-title">Summarize</div>
                <div class="example-text">
                    Turn long text into a concise summary.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="example-card">
                <div class="example-title">Change the tone</div>
                <div class="example-text">
                    Make your writing more formal, friendly, or concise.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask WriteFlow to transform your text..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Working..."):
            pipe = load_model()

            result = pipe(
                st.session_state.messages,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
            )

            generated = result[0]["generated_text"]

            if isinstance(generated, list):
                response = generated[-1]["content"]
            else:
                response = generated

        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
