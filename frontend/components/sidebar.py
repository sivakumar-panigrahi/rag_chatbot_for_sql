import streamlit as st
import json
from services.api_client import APIClient


def render_sidebar():
    client = APIClient("http://localhost:8089")

    with st.sidebar:
        st.title("🤖 Chat History")

        # ➕ New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.session_state.last_query = None
            st.rerun()

        st.divider()
        st.subheader("Previous Chats")

        try:
            conversations = client.list_conversations()
        except Exception:
            st.error("Could not load conversations from server.")
            conversations = []

        if not conversations:
            st.caption("No chats yet. Start a conversation!")
        
        for conv in conversations:
            # Columns for title button and delete button
            cols = st.columns([5, 1.2])
            is_active = st.session_state.get("conversation_id") == conv["id"]
            
            # Select appropriate label styling
            label = f"💬 {conv['title']}"
            if is_active:
                label = f"👉 {conv['title']}"

            with cols[0]:
                if st.button(
                    label,
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                ):
                    try:
                        messages_data = client.get_messages(conv["id"])
                        st.session_state.conversation_id = conv["id"]
                        st.session_state.messages = [
                            {"role": m["role"], "content": m["content"]}
                            for m in messages_data
                        ]
                        
                        # Search back for the latest query logs in the conversation to restore right-hand visual panels
                        last_query_found = None
                        for m in reversed(messages_data):
                            if m["role"] == "assistant" and m.get("query_logs"):
                                # Use the first log in the list
                                log = m["query_logs"][0]
                                try:
                                    res_list = json.loads(log["execution_result"]) if log.get("execution_result") else []
                                except Exception:
                                    res_list = []
                                last_query_found = {
                                    "question": log["question"],
                                    "sql": log["generated_sql"],
                                    "results": res_list,
                                    "execution_time": (log["execution_time_ms"] / 1000.0) if log.get("execution_time_ms") else 0.0,
                                }
                                break
                        
                        st.session_state.last_query = last_query_found
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error loading chat: {str(e)}")

            with cols[1]:
                if st.button(
                    "🗑️",
                    key=f"del_{conv['id']}",
                    help="Delete this chat",
                    use_container_width=True,
                ):
                    try:
                        client.delete_conversation(conv["id"])
                        if st.session_state.get("conversation_id") == conv["id"]:
                            st.session_state.conversation_id = None
                            st.session_state.messages = []
                            st.session_state.last_query = None
                        st.success("Deleted!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to delete: {str(e)}")