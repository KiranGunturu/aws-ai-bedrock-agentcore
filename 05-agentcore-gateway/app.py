"""
ShopSmart — Maya Customer Support Chat UI
Module 05: Gateway — Runtime invocation

Maya now reaches real tools through AgentCore Gateway. Since the agent does
not yet know who the customer is (that arrives with Memory in Module 06 and
Identity in Module 07), it simply asks for the customer ID in the conversation
when it needs one. The UI stays a plain chat interface.

Usage:
    export AWS_REGION="us-east-1"
    streamlit run app.py
"""

import json
import os
import uuid

import boto3
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ShopSmart Support — Maya",
    page_icon="🛍️",
    layout="centered",
)

# ── Configuration ─────────────────────────────────────────────────────────────

REGION = os.environ.get("AWS_REGION", "us-east-1")

@st.cache_resource
def load_runtime_arn() -> str:
    """Load the Runtime ARN from SSM (/maya/runtime_arn), fallback to env var."""
    try:
        ssm = boto3.client("ssm", region_name=REGION)
        return ssm.get_parameter(Name="/maya/runtime_arn")["Parameter"]["Value"]
    except Exception:
        return os.environ.get("MAYA_RUNTIME_ARN", "")

RUNTIME_ARN = load_runtime_arn()

if not RUNTIME_ARN:
    st.error(
        "**No agent ARN configured.**\n\n"
        "Either add it to SSM Parameter Store:\n"
        "```\n"
        "aws ssm put-parameter --name /maya/runtime_arn --type String --value 'arn:aws:bedrock-agentcore:...' --overwrite\n"
        "```\n"
        "Or set the environment variable directly:\n"
        "```\n"
        "export MAYA_RUNTIME_ARN='arn:aws:bedrock-agentcore:...'\n"
        "```"
    )
    st.stop()

# ── AWS client ────────────────────────────────────────────────────────────────

@st.cache_resource
def get_client():
    return boto3.client("bedrock-agentcore", region_name=REGION)

client = get_client()

# ── Session state ─────────────────────────────────────────────────────────────

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────

st.title("🛍️ ShopSmart Support")
st.caption("Powered by Maya — Ask me about orders, returns, shipping, and more.")
st.divider()

# ── Display conversation history ──────────────────────────────────────────────

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ── Welcome message on first load ─────────────────────────────────────────────

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("Hi! I'm Maya, ShopSmart's virtual support agent. How can I help you today?")

# ── Invoke function ───────────────────────────────────────────────────────────

def invoke_maya(prompt: str) -> str:
    """Invoke Maya via AgentCore Runtime using SigV4 (Boto3)."""
    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=RUNTIME_ARN,
            runtimeSessionId=st.session_state.session_id,
            payload=json.dumps({"prompt": prompt}),
        )
        result = json.loads(response["response"].read())
        return result.get("result", "Sorry, I could not process your request.")
    except Exception as e:
        return f"Unable to reach Maya right now. Please try again. ({str(e)})"

# ── Chat input ────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask Maya something..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Maya is thinking..."):
            response = invoke_maya(prompt)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Session Info")
    st.caption(f"Session ID: `{st.session_state.session_id[:8]}...`")
    st.caption(f"Messages: {len(st.session_state.messages)}")
    st.divider()

    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()