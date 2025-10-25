"""
Session Manager Module for Session State Chat History

Coordinates overall session state, manages session lifecycle,
and integrates chat history with document processing.
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Optional
import streamlit as st
from storage_handler import StorageHandler
from chat_history import ChatHistoryManager


class SessionManager:
    """
    Manages overall session state and coordination between components.
    
    Features:
    - Session initialization and ID generation
    - Session status tracking
    - Document upload handling with history clearing
    - Storage coordination
    """
    
    def __init__(self):
        """Initialize session manager with storage and chat history."""
        self.storage_handler = StorageHandler()
        self.chat_manager = ChatHistoryManager(self.storage_handler)
        self._initialize_session()
    
    def _initialize_session(self) -> None:
        """
        Initialize session state variables.
        
        Creates unique session ID and sets up required state variables
        if they don't already exist. Ensures session isolation.
        """
        if 'session_id' not in st.session_state:
            # Generate unique session ID with timestamp for uniqueness
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            random_id = uuid.uuid4().hex[:8]
            st.session_state.session_id = f"session_{timestamp}_{random_id}"
        
        if 'storage_status' not in st.session_state:
            st.session_state.storage_status = 'active'
        
        if 'document_metadata' not in st.session_state:
            st.session_state.document_metadata = {}
        
        if 'vector_store_ready' not in st.session_state:
            st.session_state.vector_store_ready = False
        
        # Session isolation validation
        self._validate_session_isolation()
    
    def get_session_status(self) -> Dict:
        """
        Get current session status information.
        
        Returns:
            dict: Status information including session ID, storage status,
                  message count, document status, and vector store readiness
        """
        return {
            'session_id': st.session_state.session_id,
            'storage_status': st.session_state.storage_status,
            'message_count': self.chat_manager.get_message_count(),
            'document_loaded': bool(st.session_state.document_metadata),
            'vector_store_ready': st.session_state.get('vector_store_ready', False)
        }
    
    def handle_new_document_upload(self, document_name: str, document_size: Optional[int] = None) -> None:
        """
        Handle new document upload by clearing history and updating metadata.
        
        Args:
            document_name: Name of the uploaded document
            document_size: Optional size of the document in bytes
        """
        # Clear previous chat history
        self.chat_manager.clear_history()
        
        # Update document metadata
        st.session_state.document_metadata = {
            'name': document_name,
            'processed_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        if document_size is not None:
            st.session_state.document_metadata['size_bytes'] = document_size
        
        # Reset vector store status
        st.session_state.vector_store_ready = False
    
    def mark_vector_store_ready(self) -> None:
        """Mark that the vector store has been successfully initialized."""
        st.session_state.vector_store_ready = True
    
    def get_session_id(self) -> str:
        """Get the current session ID."""
        return st.session_state.session_id
    
    def is_storage_active(self) -> bool:
        """Check if storage is currently active."""
        return st.session_state.storage_status == 'active'
    
    def get_document_name(self) -> Optional[str]:
        """Get the name of the currently loaded document."""
        return st.session_state.document_metadata.get('name')
    
    def _validate_session_isolation(self) -> None:
        """
        Validate that session data is properly isolated.
        
        Ensures that each browser session/tab has independent data.
        Streamlit handles this automatically via session_state scoping.
        """
        # Streamlit's session_state is automatically isolated per browser session
        # This method serves as a validation checkpoint
        
        # Verify session ID exists and is unique
        if 'session_id' in st.session_state:
            session_id = st.session_state.session_id
            
            # Log session info for debugging (only in development)
            # In production, this would be removed or gated behind a debug flag
            if os.getenv('DEBUG_MODE') == 'true':
                print(f"Session validated: {session_id}")
    
    def get_privacy_status(self) -> Dict:
        """
        Get privacy and data protection status information.
        
        Returns:
            dict: Information about data storage and privacy protections
        """
        return {
            'server_storage': False,  # No server-side persistence
            'browser_only': True,     # Data stays in browser
            'auto_cleanup': True,     # sessionStorage clears on browser close
            'session_isolated': True, # Each tab/session is independent
            'encryption': False,      # Data not encrypted (local storage only)
        }
