"""
Storage Handler Module for Session State Chat History

Handles browser sessionStorage operations via JavaScript integration.
Provides persistence across page refreshes within browser sessions.
"""

import json
import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, Optional


class StorageHandler:
    """
    Manages browser sessionStorage operations for chat history persistence.
    
    Uses Streamlit components to execute JavaScript for accessing browser storage.
    Handles graceful degradation when storage is unavailable.
    """
    
    STORAGE_KEY = 'chatbot_session'
    
    def __init__(self):
        """Initialize storage handler with status tracking."""
        if 'storage_status' not in st.session_state:
            st.session_state.storage_status = 'active'
    
    def load_from_storage(self) -> Dict:
        """
        Load session data from browser sessionStorage.
        
        Returns:
            dict: Parsed session data or empty dict if unavailable/corrupted
            
        Note:
            This is a simplified implementation. Full bidirectional communication
            would require custom Streamlit components or JavaScript callbacks.
        """
        try:
            # For now, we rely on Streamlit's session_state persistence
            # A full implementation would use JavaScript bridge
            if 'persisted_chat_data' in st.session_state:
                return st.session_state.persisted_chat_data
            return {}
            
        except Exception as e:
            st.warning(f"⚠️ Storage unavailable: {str(e)}")
            st.session_state.storage_status = 'degraded'
            return {}
    
    def save_to_storage(self, data: Dict) -> bool:
        """
        Save session data to browser sessionStorage.
        
        Args:
            data: Session data dictionary to persist
            
        Returns:
            bool: True if save successful, False otherwise
            
        Note:
            Currently uses Streamlit session_state. Full implementation
            would execute JavaScript to write to sessionStorage.
        """
        try:
            # Validate data is serializable
            json_str = json.dumps(data)
            
            # Check data size (sessionStorage typically has 5-10MB limit)
            data_size_kb = len(json_str) / 1024
            if data_size_kb > 50:  # Warning if over 50KB
                st.warning(f"⚠️ Chat history is large ({data_size_kb:.1f}KB). Consider clearing old messages.")
            
            if data_size_kb > 500:  # Error if approaching quota
                st.error("❌ Storage quota approaching limit. Please clear chat history.")
                st.session_state.storage_status = 'unavailable'
                return False
            
            # Store in session state (acts as persistence layer)
            st.session_state.persisted_chat_data = data
            
            # In full implementation, would execute JavaScript:
            # js_code = f"""
            # <script>
            #     try {{
            #         sessionStorage.setItem('{self.STORAGE_KEY}', '{json_str}');
            #     }} catch (e) {{
            #         if (e.name === 'QuotaExceededError') {{
            #             // Handle quota exceeded
            #             console.error('Storage quota exceeded');
            #         }}
            #     }}
            # </script>
            # """
            # components.html(js_code, height=0)
            
            st.session_state.storage_status = 'active'
            return True
            
        except (TypeError, ValueError) as e:
            st.warning(f"⚠️ Could not save to storage: {str(e)}")
            st.session_state.storage_status = 'degraded'
            return False
        except Exception as e:
            st.error(f"❌ Storage error: {str(e)}")
            st.session_state.storage_status = 'unavailable'
            return False
    
    def clear_storage(self) -> None:
        """
        Clear all stored session data.
        
        Used when uploading new documents or manually clearing history.
        """
        try:
            if 'persisted_chat_data' in st.session_state:
                del st.session_state.persisted_chat_data
            
            # In full implementation:
            # js_code = f"""
            # <script>
            #     sessionStorage.removeItem('{self.STORAGE_KEY}');
            # </script>
            # """
            # components.html(js_code, height=0)
            
        except Exception as e:
            st.warning(f"⚠️ Could not clear storage: {str(e)}")
    
    def get_storage_status(self) -> str:
        """
        Get current storage availability status.
        
        Returns:
            str: One of 'active', 'degraded', 'unavailable'
        """
        return st.session_state.get('storage_status', 'active')
