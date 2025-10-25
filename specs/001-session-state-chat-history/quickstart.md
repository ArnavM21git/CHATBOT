# Quickstart: Session State Chat History

**Feature**: Session state chat history implementation  
**Date**: 2025-10-25  
**Phase**: Phase 1 - Design & Contracts  

## Overview

This quickstart guide shows how to implement and use the session state chat history feature in the NoteBot ChatBot application.

## Prerequisites

- Python 3.10+ installed
- Existing ChatBot.py Streamlit application working
- Required dependencies in requirements.txt:
  - streamlit==1.39.0
  - PyPDF2==3.0.1
  - langchain==0.2.16
  - langchain-google-genai==1.0.10
  - faiss-cpu==1.9.0.post1

## Implementation Steps

### Step 1: Create Core Modules

Create three new Python files in the project root:

#### `chat_history.py`
```python
import json
from datetime import datetime
from typing import List, Dict, Optional
import streamlit as st

class ChatHistoryManager:
    """Manages chat history with automatic persistence and cleanup."""
    
    MAX_MESSAGES = 50
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        self._initialize_history()
    
    def _initialize_history(self):
        """Initialize chat history from storage or create empty."""
        if 'chat_history' not in st.session_state:
            stored_data = self.storage_handler.load_from_storage()
            st.session_state.chat_history = stored_data.get('chat_history', [])
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add new message to chat history."""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'metadata': metadata or {}
        }
        
        st.session_state.chat_history.append(message)
        self._cleanup_if_needed()
        self.storage_handler.save_to_storage({
            'chat_history': st.session_state.chat_history
        })
    
    def _cleanup_if_needed(self):
        """Remove oldest Q&A pairs if over limit."""
        messages = st.session_state.chat_history
        if len(messages) > self.MAX_MESSAGES:
            # Remove complete Q&A pairs from beginning
            pairs_to_remove = (len(messages) - self.MAX_MESSAGES) // 2
            st.session_state.chat_history = messages[pairs_to_remove * 2:]
    
    def get_chat_history(self) -> List[Dict]:
        """Get current chat history."""
        return st.session_state.chat_history.copy()
    
    def clear_history(self):
        """Clear all chat history (for new document uploads)."""
        st.session_state.chat_history = []
        self.storage_handler.clear_storage()
```

#### `storage_handler.py`
```python
import json
import streamlit as st
import streamlit.components.v1 as components

class StorageHandler:
    """Handles browser sessionStorage operations via JavaScript."""
    
    STORAGE_KEY = 'chatbot_session'
    
    def load_from_storage(self) -> dict:
        """Load session data from browser sessionStorage."""
        try:
            # JavaScript to retrieve sessionStorage data
            js_code = f"""
            <script>
                const data = sessionStorage.getItem('{self.STORAGE_KEY}');
                if (data) {{
                    const result = JSON.parse(data);
                    window.parent.postMessage({{
                        type: 'storage_data',
                        payload: result
                    }}, '*');
                }} else {{
                    window.parent.postMessage({{
                        type: 'storage_data',
                        payload: {{}}
                    }}, '*');
                }}
            </script>
            """
            
            # Execute JavaScript (this is a simplified version)
            # In real implementation, you'd need bidirectional communication
            components.html(js_code, height=0)
            
            # For now, return empty dict (will be enhanced with real JS communication)
            return {}
            
        except Exception as e:
            st.warning(f"Storage unavailable: {e}")
            return {}
    
    def save_to_storage(self, data: dict) -> bool:
        """Save session data to browser sessionStorage."""
        try:
            json_data = json.dumps(data)
            js_code = f"""
            <script>
                sessionStorage.setItem('{self.STORAGE_KEY}', '{json_data}');
            </script>
            """
            components.html(js_code, height=0)
            return True
            
        except Exception as e:
            st.warning(f"Could not save to storage: {e}")
            return False
    
    def clear_storage(self):
        """Clear all stored session data."""
        js_code = f"""
        <script>
            sessionStorage.removeItem('{self.STORAGE_KEY}');
        </script>
        """
        components.html(js_code, height=0)
```

#### `session_manager.py`
```python
import uuid
import streamlit as st
from storage_handler import StorageHandler
from chat_history import ChatHistoryManager

class SessionManager:
    """Manages overall session state and coordination."""
    
    def __init__(self):
        self.storage_handler = StorageHandler()
        self.chat_manager = ChatHistoryManager(self.storage_handler)
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize session state variables."""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        if 'storage_status' not in st.session_state:
            st.session_state.storage_status = 'active'
        
        if 'document_metadata' not in st.session_state:
            st.session_state.document_metadata = {}
    
    def get_session_status(self) -> dict:
        """Get current session status information."""
        return {
            'session_id': st.session_state.session_id,
            'storage_status': st.session_state.storage_status,
            'message_count': len(st.session_state.get('chat_history', [])),
            'document_loaded': bool(st.session_state.document_metadata),
            'vector_store_ready': st.session_state.get('vector_store_ready', False)
        }
    
    def handle_new_document_upload(self, document_name: str):
        """Handle new document upload by clearing history."""
        self.chat_manager.clear_history()
        st.session_state.document_metadata = {
            'name': document_name,
            'processed_at': datetime.utcnow().isoformat() + 'Z'
        }
        st.session_state.vector_store_ready = False
```

### Step 2: Update Main ChatBot.py

Modify your existing `ChatBot.py` to integrate chat history:

```python
import streamlit as st
from session_manager import SessionManager

# Initialize session manager
@st.cache_resource
def get_session_manager():
    return SessionManager()

def main():
    st.title("🤖 NoteBot ChatBot with Memory")
    
    # Initialize session
    session_mgr = get_session_manager()
    
    # Sidebar for chat history
    with st.sidebar:
        st.header("📝 Chat History")
        
        # Display session status
        status = session_mgr.get_session_status()
        st.info(f"Messages: {status['message_count']}")
        
        if status['storage_status'] != 'active':
            st.warning("⚠️ Chat history not being saved")
        
        # Display chat history
        chat_history = session_mgr.chat_manager.get_chat_history()
        for msg in chat_history:
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            with st.expander(f"{role_icon} {msg['timestamp'][:16]}"):
                st.write(msg['content'])
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            session_mgr.chat_manager.clear_history()
            st.rerun()
    
    # Main area
    st.header("📄 Document Upload")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Handle new document
        if uploaded_file.name != st.session_state.get('current_document'):
            session_mgr.handle_new_document_upload(uploaded_file.name)
            st.session_state.current_document = uploaded_file.name
            st.success(f"Document '{uploaded_file.name}' uploaded! Chat history cleared.")
        
        # Your existing PDF processing code here...
        # process_pdf(uploaded_file)
        # setup_vector_store()
        
        st.header("💬 Chat Interface")
        
        # Chat input
        user_input = st.text_input("Ask a question about the document:")
        
        if user_input and st.button("Send"):
            # Add user message to history
            session_mgr.chat_manager.add_message("user", user_input)
            
            # Your existing AI response generation code here...
            # response = generate_response(user_input, chat_history)
            response = f"AI Response to: {user_input}"  # Placeholder
            
            # Add AI response to history
            session_mgr.chat_manager.add_message("assistant", response)
            
            # Refresh the page to show new messages
            st.rerun()

if __name__ == "__main__":
    main()
```

## Usage Examples

### Basic Chat Session

1. **Start Application**: `streamlit run ChatBot.py`
2. **Upload PDF**: Use file uploader to select document
3. **Ask Questions**: Type questions and click Send
4. **View History**: Check sidebar for previous messages
5. **Refresh Test**: Refresh browser page - history persists
6. **New Document**: Upload new file - history clears automatically

### Testing Chat Memory

```python
# Test conversation flow
user_questions = [
    "What is the main topic of this document?",
    "Can you elaborate on that?",  # Tests context reference
    "What did we discuss earlier?"  # Tests memory
]

# Each question should reference previous context
```

### Error Scenarios to Test

1. **Storage Disabled**: Open in private/incognito mode
2. **Large Conversations**: Send 30+ messages to test cleanup
3. **Page Refresh**: Refresh during active conversation
4. **Multiple Tabs**: Open same app in different browser tabs

## Configuration Options

### Adjust Message Limits

```python
# In chat_history.py
class ChatHistoryManager:
    MAX_MESSAGES = 100  # Change from 50 to 100
```

### Customize Storage Key

```python
# In storage_handler.py
class StorageHandler:
    STORAGE_KEY = 'my_custom_chatbot_key'
```

### Add Message Metadata

```python
# When adding messages
session_mgr.chat_manager.add_message(
    "user", 
    "What is renewable energy?",
    metadata={
        "document_page": 3,
        "confidence": 0.95,
        "processing_time": 1.2
    }
)
```

## Troubleshooting

### Common Issues

1. **History Not Persisting**
   - Check browser console for JavaScript errors
   - Verify sessionStorage is enabled
   - Test in different browsers

2. **Memory Usage High**
   - Reduce MAX_MESSAGES limit
   - Clear browser cache
   - Monitor Streamlit memory usage

3. **Slow Performance**
   - Check message cleanup logic
   - Optimize chat history rendering
   - Profile with Streamlit profiler

### Debug Mode

Add debug information to your application:

```python
# Add to main()
if st.checkbox("Debug Mode"):
    st.json({
        "session_state": dict(st.session_state),
        "chat_history_length": len(st.session_state.get('chat_history', [])),
        "storage_status": session_mgr.get_session_status()
    })
```

## Next Steps

1. **Enhance Storage**: Implement proper bidirectional JavaScript communication
2. **Add Export**: Allow users to download conversation history
3. **Improve UI**: Add better styling and message formatting
4. **Add Tests**: Create unit tests for each module
5. **Performance**: Optimize for larger conversations

## Support

For issues or questions:
- Check the specification documents in `specs/001-session-state-chat-history/`
- Review the constitution for compliance guidelines
- Test with the provided example scenarios

This quickstart provides a working foundation for session state chat history that you can build upon and customize for your specific needs.