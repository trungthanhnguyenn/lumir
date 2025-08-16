import gradio as gr
import os
import requests
import json
import uuid
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
WINDMILL_API_URL = os.getenv("WINDMILL_API_URL", "http://localhost:80")
WINDMILL_TOKEN = os.getenv("WINDMILL_TOKEN", "")
WINDMILL_ROUTE = "lumir_ai_v2"

# Database configurations
QDRANT_CONFIG = {
    "host": os.getenv("QDRANT_HOST", "192.168.2.78"),
    "port": int(os.getenv("QDRANT_PORT", "1237")),
    "vector_size": int(os.getenv("QDRANT_VECTOR_SIZE", "768"))
}

MINIO_CONFIG = {
    "endpoint": os.getenv("MINIO_ENDPOINT", "192.168.2.78:1235"),
    "access_key": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    "secret_key": os.getenv("MINIO_SECRET_KEY", "minioadmin123"),
    "secure": os.getenv("MINIO_SECURE", "false").lower() == "true"
}

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "192.168.2.78"),
    "database": os.getenv("POSTGRES_DATABASE", "docsdb"),
    "user": os.getenv("POSTGRES_USER", "user"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "port": int(os.getenv("POSTGRES_PORT", "1234"))
}

RAG_CONFIG = {
    "version": int(os.getenv("RAG_VERSION", "1")),
    "url": os.getenv("RAG_URL", "192.168.2.78:7001"),
    "grpc": os.getenv("RAG_GRPC", "true").lower() == "true"
}

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "Vietnamese")

# Global variables for session management
chat_sessions: Dict[str, Dict[str, Any]] = {}

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())

def suggest_birthday_from_session(session_id: str) -> str:
    """Generate a suggested birthday based on session ID hash"""
    # Use session ID hash to generate consistent birthday suggestion
    hash_obj = hashlib.md5(session_id.encode())
    hash_int = int(hash_obj.hexdigest()[:8], 16)
    
    # Generate day (1-28), month (1-12), year (1990-2005)
    day = (hash_int % 28) + 1
    month = ((hash_int >> 5) % 12) + 1
    year = 1990 + ((hash_int >> 9) % 16)
    
    return f"{day:02d}/{month:02d}/{year}"

# Validate birthday in DD/MM/YYYY format
def is_valid_birthday(date_str: str) -> bool:
    try:
        if not date_str:
            return False
        datetime.strptime(date_str.strip(), "%d/%m/%Y")
        return True
    except Exception:
        return False


def get_or_create_session(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get existing session or create new one"""
    if not session_id or session_id not in chat_sessions:
        new_session_id = generate_session_id()
        chat_sessions[new_session_id] = {
            "session_id": new_session_id,
            "history": [],
            "suggested_birthday": suggest_birthday_from_session(new_session_id),
            "created_at": datetime.now().isoformat()
        }
        return chat_sessions[new_session_id]
    return chat_sessions[session_id]

def call_windmill_api(
    question: str,
    upload: bool,
    language: str,
    session_id: str,
    history: List[Dict],
    birthday: str,
    rerank: bool = False
) -> str:
    """Call Windmill API with the provided parameters"""
    
    payload = {
        "Question": question,
        "Upload": upload,
        "Qdrant_Config": QDRANT_CONFIG,
        "MinIO_Config": MINIO_CONFIG,
        "Postgre_Config": POSTGRES_CONFIG,
        "RAG_Config": RAG_CONFIG,
        "session_id": session_id,
        "history": history,
        "rerank": rerank,
        "birthday": birthday,
        "language": language
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WINDMILL_TOKEN}"
    }
    
    try:
        logger.info(f"Calling Windmill API with session_id: {session_id}")
        logger.info(f"History format being sent: {history[:2] if len(history) > 2 else history}")  # Log first 2 items
        response = requests.post(
            f"{WINDMILL_API_URL}/api/r/{WINDMILL_ROUTE}",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            # Some Windmill routes return a JSON-encoded string (e.g. "...\n...")
            # Parse it to preserve real newlines; fallback to unescaping common sequences
            try:
                parsed = json.loads(response.text)
                if isinstance(parsed, str):
                    return parsed
                # If it's an object with a 'text' field
                if isinstance(parsed, dict) and isinstance(parsed.get('text'), str):
                    return parsed['text']
                # Fallback: just return text with basic unescape for newlines/tabs/quotes
                return response.text.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')
            except Exception:
                # If JSON parsing fails, try to unescape common sequences
                return response.text.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')
        else:
            error_msg = f"API Error {response.status_code}: {response.text}"
            logger.error(error_msg)
            return error_msg
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        logger.error(error_msg)
        return error_msg

def handle_file_upload(files, session_id_state):
    """Handle file upload and return status"""
    if not files:
        return "Không có file nào được upload.", session_id_state
    
    session = get_or_create_session(session_id_state)
    
    # For now, just return success message
    # In a real implementation, you would process and upload files
    uploaded_files = [f.name for f in files]
    status_msg = f"Đã upload thành công {len(uploaded_files)} file: {', '.join(uploaded_files)}"
    
    logger.info(f"Files uploaded for session {session['session_id']}: {uploaded_files}")
    return status_msg, session['session_id']

def chat_with_ai(
    message: str,
    history: List[Dict[str, str]],
    language: str,
    upload_enabled: bool,
    birthday: str,
    rerank_enabled: bool,
    session_id_state: str
):
    """Main chat function with improved UX and non-intrusive birthday suggestion"""
    if not message.strip():
        # No message -> nothing to do
        yield history, "", session_id_state
        return
    
    # Get or create session
    session = get_or_create_session(session_id_state)
    session_id = session['session_id']
    
    # Determine birthday to use (do NOT auto-fill the UI input)
    if not birthday or not str(birthday).strip():
        birthday_to_use = session['suggested_birthday']  # used for API only
    else:
        birthday_to_use = birthday
    
    # 1. Immediately show user message
    history.append({"role": "user", "content": message})
    yield history, "", session_id_state
    
    # 2. Show typing indicator
    history.append({"role": "assistant", "content": "💭 Đang suy nghĩ..."})
    yield history, "", session_id_state
    
    # Load existing history from session
    if session['history']:
        api_history = session['history'].copy()
    else:
        api_history = []
        for msg in history[:-2]:  # Exclude current message and typing indicator
            if msg.get('role') and msg.get('content') and msg['content'] != "💭 Tiến hành phân tích dữ liệu...":
                api_history.append({"role": msg['role'], "content": msg['content']})
    
    # Add current message to API history
    api_history.append({"role": "user", "content": message})
    
    # Call Windmill API
    response = call_windmill_api(
        question=message,
        upload=upload_enabled,
        language=language,
        session_id=session_id,
        history=api_history,
        birthday=birthday_to_use,
        rerank=rerank_enabled
    )
    
    # 3. Replace typing indicator with actual response (and append birthday hint if needed)
    final_response = response
    if (not birthday) or (not str(birthday).strip()) or (not is_valid_birthday(str(birthday).strip())):
        if language == "Vietnamese":
            final_response = f"{response}\n\n💡 Để nhận được câu trả lời cá nhân hoá hơn, vui lòng tạo tài khoản và đăng nhập vào hệ thống."
        else:
            final_response = f"{response}\n\n💡 To get more personalized answers, please sign up and login to the system."
    
    # Update the typing indicator with the final response (whether modified or original)
    history[-1] = {"role": "assistant", "content": final_response}
    
    # Add response to API history
    api_history.append({"role": "assistant", "content": final_response})
    
    # Update session history (persistent storage)
    session['history'] = api_history
    
    yield history, "", session_id_state

def reset_chat(session_id_state):
    """Reset chat and create new session"""
    new_session = get_or_create_session()
    # Add welcome message to new session
    welcome_msg = {
        "role": "assistant", 
        "content": "👋 Xin chào! Tôi là Lumir-AI, trợ lý tài chính chuyên về trading.\n\n🔹 Tôi có thể giúp bạn:\n• Phân tích thị trường và xu hướng\n• Tư vấn chiến lược đầu tư\n• Giải đáp các câu hỏi về tài chính\n\nHãy cho tôi biết bạn cần hỗ trợ gì nhé! 😊"
    }
    new_session['history'] = [welcome_msg]
    hint_text = f"Gợi ý ngày sinh cho phiên này: **{new_session['suggested_birthday']}**"
    return [welcome_msg], new_session['session_id'], "", hint_text

def load_session_history(session_id_state):
    """Load chat history from session"""
    if not session_id_state or session_id_state not in chat_sessions:
        return []
    
    session = chat_sessions[session_id_state]
    gradio_history = []
    
    # Convert API history format to Gradio format
    for msg in session.get('history', []):
        if msg.get('role') and msg.get('content'):
            gradio_history.append({
                "role": msg['role'], 
                "content": msg['content']
            })
    
    return gradio_history

# CSS styling
CSS = """
.container {
    max-width: 1200px;
    margin: 0 auto;
}
.header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 20px;
}
.chat-container {
    height: 500px;
}
.config-panel {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}
.typing-indicator {
    animation: pulse 1.5s ease-in-out infinite;
    color: #666;
    font-style: italic;
}
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}
.message-input {
    border-radius: 20px !important;
    border: 2px solid #e1e5e9 !important;
    padding: 12px 16px !important;
}
.message-input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}
.send-button {
    border-radius: 20px !important;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
}
footer {
    visibility: hidden;
}
"""

# Create Gradio interface
with gr.Blocks(theme="soft", css=CSS, title="LUMIR") as demo:
    
    # Header
    gr.HTML("""
    <div class="header">
        <h1>🤖 Smart Trading Assistant</h1>
        <p>Powered by BEQ-HOLDING</p>
    </div>
    """)
    
    # Session state
    session_id_state = gr.State("")
    
    with gr.Row():
        # Left column - Configuration
        with gr.Column(scale=1):
            gr.HTML('<div class="config-panel"><h3>⚙️ Configuration</h3></div>')
            
            # Language selection
            language_dropdown = gr.Dropdown(
                choices=["Vietnamese", "English", "Chinese", "Japanese", "Korean"],
                value=DEFAULT_LANGUAGE,
                label="🌐 Language",
                info="Select response language"
            )
            
            # Upload settings
            upload_checkbox = gr.Checkbox(
                label="📁 Enable Upload Mode",
                value=False,
                info="Enable file upload processing"
            )
            
            # File upload
            file_upload = gr.File(
                label="📎 Upload Files",
                file_count="multiple",
                file_types=[".pdf", ".docx", ".txt", ".md"],
                visible=False
            )
            
            upload_status = gr.Textbox(
                label="Trạng thái Upload",
                interactive=False,
                visible=False
            )
            
            # Birthday input + Suggest button
            with gr.Row():
                birthday_input = gr.Textbox(
                    label="🎂 Birthday (DD/MM/YYYY)",
                    placeholder="27/12/2002",
                    info="Used for personalized responses",
                    scale=4
                )
                suggest_birthday_btn = gr.Button("Gợi ý 🎂", variant="secondary", scale=1)
            
            birthday_hint = gr.Markdown(visible=True)
            
            # Suggest birthday button action (placed after components are defined)
            def suggest_birthday(session_id):
                session = get_or_create_session(session_id)
                return f"Gợi ý ngày sinh cho phiên này: **{session['suggested_birthday']}**"
            
            suggest_birthday_btn.click(
                fn=suggest_birthday,
                inputs=[session_id_state],
                outputs=[birthday_hint]
            )
            
            # Advanced settings
            with gr.Accordion("🔧 Advanced Settings", open=False):
                rerank_checkbox = gr.Checkbox(
                    label="🔄 Enable Reranking",
                    value=False,
                    info="Improve search result relevance"
                )
                
                session_info = gr.Textbox(
                    label="ID Phiên",
                    interactive=False,
                    info="Định danh phiên chat hiện tại"
                )
        
        # Right column - Chat interface
        with gr.Column(scale=2):
            # Chat interface
            chatbot = gr.Chatbot(
                label="💬 Chat",
                height=500,
                show_copy_button=True,
                type="messages"
            )
            
            # Message input
            with gr.Row():
                msg_input = gr.Textbox(
                    label="",
                    placeholder="Nhập tin nhắn của bạn...",
                    scale=4,
                    lines=2,
                    elem_classes=["message-input"]
                )
                send_btn = gr.Button("Gửi 📤", scale=1, variant="primary", elem_classes=["send-button"])
            
            # Control buttons
            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
                new_session_btn = gr.Button("🆕 New Session", variant="secondary")
    
    # Event handlers
    def toggle_upload_visibility(upload_enabled):
        return {
            file_upload: gr.update(visible=upload_enabled),
            upload_status: gr.update(visible=upload_enabled)
        }
    
    def initialize_session():
        session = get_or_create_session()
        # Add welcome message to new sessions
        if not session['history']:
            welcome_msg = {
                "role": "assistant", 
                "content": "👋 Xin chào! Tôi là Lumir-AI, trợ lý tài chính chuyên về trading.\n\n🔹 Tôi có thể giúp bạn:\n• Phân tích thị trường và xu hướng\n• Tư vấn chiến lược đầu tư\n• Giải đáp các câu hỏi về tài chính\n\nHãy cho tôi biết bạn cần hỗ trợ gì nhé! 😊"
            }
            session['history'] = [welcome_msg]
            initial_history = [welcome_msg]
        else:
            initial_history = load_session_history(session['session_id'])
        
        hint_text = f"Gợi ý ngày sinh cho phiên này: **{session['suggested_birthday']}**"
        
        return session['session_id'], "", initial_history, hint_text
    
    # Initialize session on load
    demo.load(
        fn=initialize_session,
        outputs=[session_id_state, birthday_input, chatbot, birthday_hint]
    )
    
    # Update session info display and load history when session changes
    def on_session_change(session_id):
        history = load_session_history(session_id)
        hint_text = ""
        if session_id in chat_sessions:
            hint_text = f"Gợi ý ngày sinh cho phiên này: **{chat_sessions[session_id]['suggested_birthday']}**"
        return session_id, history, hint_text
    
    session_id_state.change(
        fn=on_session_change,
        inputs=[session_id_state],
        outputs=[session_info, chatbot, birthday_hint]
    )
    
    # Toggle upload visibility
    upload_checkbox.change(
        fn=toggle_upload_visibility,
        inputs=[upload_checkbox],
        outputs=[file_upload, upload_status]
    )
    
    # File upload handler
    file_upload.upload(
        fn=handle_file_upload,
        inputs=[file_upload, session_id_state],
        outputs=[upload_status, session_id_state]
    )
    
    # Chat handlers with streaming support
    def submit_message(message, history, language, upload_enabled, birthday, rerank_enabled, session_id):
        # Generator function for streaming
        for result in chat_with_ai(message, history, language, upload_enabled, birthday, rerank_enabled, session_id):
            yield result
    
    # Send message on button click
    send_btn.click(
        fn=submit_message,
        inputs=[
            msg_input, chatbot, language_dropdown, upload_checkbox, 
            birthday_input, rerank_checkbox, session_id_state
        ],
        outputs=[chatbot, msg_input, session_id_state]
    )
    
    # Send message on Enter
    msg_input.submit(
        fn=submit_message,
        inputs=[
            msg_input, chatbot, language_dropdown, upload_checkbox,
            birthday_input, rerank_checkbox, session_id_state
        ],
        outputs=[chatbot, msg_input, session_id_state]
    )
    
    # Clear chat
    clear_btn.click(
        fn=lambda: ([], ""),
        outputs=[chatbot, msg_input]
    ).then(
        fn=lambda: "",
        outputs=[birthday_input]
    )
    
    # New session
    new_session_btn.click(
        fn=reset_chat,
        inputs=[session_id_state],
        outputs=[chatbot, session_id_state, birthday_input, birthday_hint]
    )

if __name__ == "__main__":
    print("🚀 Starting Windmill AI Chat Interface...")
    print(f"📡 API URL: {WINDMILL_API_URL}")
    print(f"🔑 Token configured: {'Yes' if WINDMILL_TOKEN else 'No'}")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,  # Changed port to avoid conflict
        share=True,
        show_error=True
    )
