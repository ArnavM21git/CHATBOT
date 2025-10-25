"""
Chat History Manager Module for Session State Chat History

Manages chat message storage, retrieval, and conversation context generation.
Implements message limit enforcement and automatic cleanup.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
import uuid
import streamlit as st


class ChatMessage:
    """
    Data structure for a single chat message.
    
    Attributes:
        role: Message sender role ("user" or "assistant")
        content: The message text content
        timestamp: ISO 8601 timestamp of message creation
        metadata: Optional metadata dictionary
    """
    
    def __init__(self, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Create a new chat message.
        
        Args:
            role: Must be "user" or "assistant"
            content: Message text (non-empty, max 10,000 chars)
            metadata: Optional metadata dictionary
            
        Raises:
            ValueError: If role is invalid or content is empty/oversized
        """
        if role not in ("user", "assistant"):
            raise ValueError(f"Invalid role: {role}. Must be 'user' or 'assistant'")
        
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
        
        if len(content) > 10000:
            raise ValueError("Message content exceeds 10,000 character limit")
        
        self.role = role
        self.content = content.strip()
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.metadata = metadata or {}
        self.metadata['message_id'] = str(uuid.uuid4())
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary for serialization."""
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatMessage':
        """Create message from dictionary."""
        msg = cls.__new__(cls)
        msg.role = data['role']
        msg.content = data['content']
        msg.timestamp = data['timestamp']
        msg.metadata = data.get('metadata', {})
        return msg


class ChatHistoryManager:
    """
    Manages chat history with automatic persistence and cleanup.
    
    Features:
    - Automatic message limit enforcement (50 messages max)
    - Q&A pair boundary preservation during cleanup
    - Storage persistence via StorageHandler
    - Conversation context generation for AI
    """
    
    MAX_MESSAGES = 50
    
    def __init__(self, storage_handler):
        """
        Initialize chat history manager.
        
        Args:
            storage_handler: StorageHandler instance for persistence
        """
        self.storage_handler = storage_handler
        self._initialize_history()
    
    def _initialize_history(self):
        """Initialize chat history from storage or create empty."""
        if 'chat_history' not in st.session_state:
            try:
                stored_data = self.storage_handler.load_from_storage()
                chat_data = stored_data.get('chat_history', [])
                
                # Validate loaded data
                if isinstance(chat_data, list):
                    # Validate each message has required fields
                    validated_messages = []
                    for msg in chat_data:
                        if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                            validated_messages.append(msg)
                    
                    st.session_state.chat_history = validated_messages
                else:
                    st.session_state.chat_history = []
                    
            except Exception as e:
                # Corrupted data recovery
                st.warning(f"⚠️ Could not load chat history. Starting fresh. Error: {str(e)}")
                st.session_state.chat_history = []
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Add a new message to chat history.
        
        Args:
            role: Message sender ("user" or "assistant")
            content: Message text content
            metadata: Optional metadata dictionary
            
        Raises:
            ValueError: If message validation fails
        """
        # Create and validate message
        message = ChatMessage(role, content, metadata)
        
        # Add to session state
        st.session_state.chat_history.append(message.to_dict())
        
        # Cleanup if needed
        self._cleanup_if_needed()
        
        # Persist to storage
        self.storage_handler.save_to_storage({
            'chat_history': st.session_state.chat_history
        })
    
    def _cleanup_if_needed(self) -> None:
        """
        Remove oldest Q&A pairs if over message limit.
        
        Maintains conversation coherence by removing complete Q&A pairs
        rather than individual messages.
        """
        messages = st.session_state.chat_history
        
        if len(messages) <= self.MAX_MESSAGES:
            return
        
        # Calculate how many pairs to remove
        excess_messages = len(messages) - self.MAX_MESSAGES
        pairs_to_remove = (excess_messages + 1) // 2  # Round up
        messages_to_remove = pairs_to_remove * 2
        
        # Remove from beginning (oldest messages)
        st.session_state.chat_history = messages[messages_to_remove:]
    
    def get_chat_history(self) -> List[Dict]:
        """
        Get current chat history.
        
        Returns:
            List of ChatMessage dictionaries in chronological order
        """
        return st.session_state.chat_history.copy()
    
    def clear_history(self) -> None:
        """
        Clear all chat history.
        
        Used when uploading new documents or manual clear action.
        """
        st.session_state.chat_history = []
        self.storage_handler.clear_storage()
    
    def get_conversation_context(self, last_n: int = 5) -> Dict:
        """
        Generate conversation context for AI responses.
        
        Args:
            last_n: Number of recent exchanges to include
            
        Returns:
            ConversationContext dictionary with recent exchanges,
            summary, and document context
        """
        messages = st.session_state.chat_history
        
        # Extract recent Q&A pairs
        recent_exchanges = []
        i = len(messages) - 1
        pairs_collected = 0
        
        while i >= 1 and pairs_collected < last_n:
            if messages[i]['role'] == 'assistant' and messages[i-1]['role'] == 'user':
                recent_exchanges.insert(0, {
                    'user': messages[i-1]['content'],
                    'assistant': messages[i]['content'],
                    'timestamp': messages[i]['timestamp']
                })
                pairs_collected += 1
                i -= 2
            else:
                i -= 1
        
        # Generate conversation summary
        topics = set()
        for exchange in recent_exchanges:
            # Simple topic extraction (first few words of questions)
            question_words = exchange['user'].split()[:5]
            topics.add(' '.join(question_words))
        
        conversation_summary = f"Discussion about: {', '.join(list(topics)[:3])}" if topics else ""
        
        # Document context
        document_context = {
            'document_name': st.session_state.get('document_metadata', {}).get('name', 'Unknown'),
            'main_topics': list(topics)[:5]
        }
        
        return {
            'recent_exchanges': recent_exchanges,
            'conversation_summary': conversation_summary[:500],  # Max 500 chars
            'document_context': document_context,
            'total_messages': len(messages)
        }
    
    def get_message_count(self) -> int:
        """Get total number of messages in current session."""
        return len(st.session_state.get('chat_history', []))
