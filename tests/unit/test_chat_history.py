"""
Unit tests for ChatHistoryManager
"""

import pytest
from unittest.mock import Mock, MagicMock
from chat_history import ChatMessage, ChatHistoryManager


class TestChatMessage:
    """Test ChatMessage data structure."""
    
    def test_create_valid_user_message(self):
        """Test creating a valid user message."""
        msg = ChatMessage("user", "What is this document about?")
        
        assert msg.role == "user"
        assert msg.content == "What is this document about?"
        assert msg.timestamp is not None
        assert 'message_id' in msg.metadata
    
    def test_create_valid_assistant_message(self):
        """Test creating a valid assistant message."""
        msg = ChatMessage("assistant", "This document is about renewable energy.")
        
        assert msg.role == "assistant"
        assert msg.content == "This document is about renewable energy."
    
    def test_invalid_role_raises_error(self):
        """Test that invalid role raises ValueError."""
        with pytest.raises(ValueError, match="Invalid role"):
            ChatMessage("invalid_role", "Some content")
    
    def test_empty_content_raises_error(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ChatMessage("user", "")
    
    def test_whitespace_content_raises_error(self):
        """Test that whitespace-only content raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ChatMessage("user", "   ")
    
    def test_oversized_content_raises_error(self):
        """Test that oversized content raises ValueError."""
        large_content = "x" * 10001  # Over 10,000 char limit
        with pytest.raises(ValueError, match="exceeds 10,000 character limit"):
            ChatMessage("user", large_content)
    
    def test_to_dict_conversion(self):
        """Test message conversion to dictionary."""
        msg = ChatMessage("user", "Test question")
        msg_dict = msg.to_dict()
        
        assert msg_dict['role'] == "user"
        assert msg_dict['content'] == "Test question"
        assert 'timestamp' in msg_dict
        assert 'metadata' in msg_dict
    
    def test_from_dict_conversion(self):
        """Test creating message from dictionary."""
        data = {
            'role': 'assistant',
            'content': 'Test answer',
            'timestamp': '2025-10-25T10:30:00Z',
            'metadata': {'message_id': '12345'}
        }
        
        msg = ChatMessage.from_dict(data)
        
        assert msg.role == "assistant"
        assert msg.content == "Test answer"
        assert msg.timestamp == '2025-10-25T10:30:00Z'


class TestChatHistoryManager:
    """Test ChatHistoryManager functionality."""
    
    @pytest.fixture
    def mock_storage_handler(self):
        """Create a mock storage handler."""
        handler = Mock()
        handler.load_from_storage.return_value = {'chat_history': []}
        handler.save_to_storage.return_value = True
        return handler
    
    def test_initialization_empty_history(self, mock_storage_handler, monkeypatch):
        """Test initialization with empty history."""
        # Mock streamlit session_state
        mock_session_state = {}
        monkeypatch.setattr("chat_history.st.session_state", mock_session_state)
        
        manager = ChatHistoryManager(mock_storage_handler)
        
        assert 'chat_history' in mock_session_state
        assert mock_session_state['chat_history'] == []
    
    def test_add_message(self, mock_storage_handler, monkeypatch):
        """Test adding a message to history."""
        mock_session_state = {'chat_history': []}
        monkeypatch.setattr("chat_history.st.session_state", mock_session_state)
        
        manager = ChatHistoryManager(mock_storage_handler)
        manager.add_message("user", "Test question")
        
        assert len(mock_session_state['chat_history']) == 1
        assert mock_session_state['chat_history'][0]['role'] == "user"
        assert mock_session_state['chat_history'][0]['content'] == "Test question"
    
    def test_cleanup_when_over_limit(self, mock_storage_handler, monkeypatch):
        """Test cleanup removes oldest Q&A pairs when over limit."""
        # Create 52 messages (26 Q&A pairs)
        messages = []
        for i in range(26):
            messages.append({'role': 'user', 'content': f'Question {i}', 'timestamp': f'2025-10-25T10:{i:02d}:00Z'})
            messages.append({'role': 'assistant', 'content': f'Answer {i}', 'timestamp': f'2025-10-25T10:{i:02d}:00Z'})
        
        mock_session_state = {'chat_history': messages}
        monkeypatch.setattr("chat_history.st.session_state", mock_session_state)
        
        manager = ChatHistoryManager(mock_storage_handler)
        manager._cleanup_if_needed()
        
        # Should have removed 1 Q&A pair (2 messages) to get to 50
        assert len(mock_session_state['chat_history']) == 50
        # Oldest messages should be removed
        assert 'Question 0' not in str(mock_session_state['chat_history'])
    
    def test_clear_history(self, mock_storage_handler, monkeypatch):
        """Test clearing all history."""
        mock_session_state = {
            'chat_history': [
                {'role': 'user', 'content': 'Test', 'timestamp': '2025-10-25T10:00:00Z'}
            ]
        }
        monkeypatch.setattr("chat_history.st.session_state", mock_session_state)
        
        manager = ChatHistoryManager(mock_storage_handler)
        manager.clear_history()
        
        assert len(mock_session_state['chat_history']) == 0
        mock_storage_handler.clear_storage.assert_called_once()
    
    def test_get_conversation_context(self, mock_storage_handler, monkeypatch):
        """Test generating conversation context."""
        messages = [
            {'role': 'user', 'content': 'What is AI?', 'timestamp': '2025-10-25T10:00:00Z'},
            {'role': 'assistant', 'content': 'AI is...', 'timestamp': '2025-10-25T10:00:01Z'},
            {'role': 'user', 'content': 'Tell me more', 'timestamp': '2025-10-25T10:00:02Z'},
            {'role': 'assistant', 'content': 'AI involves...', 'timestamp': '2025-10-25T10:00:03Z'},
        ]
        
        mock_session_state = {'chat_history': messages}
        monkeypatch.setattr("chat_history.st.session_state", mock_session_state)
        
        manager = ChatHistoryManager(mock_storage_handler)
        context = manager.get_conversation_context(last_n=5)
        
        assert 'recent_exchanges' in context
        assert 'conversation_summary' in context
        assert 'document_context' in context
        assert 'total_messages' in context
        assert context['total_messages'] == 4
        assert len(context['recent_exchanges']) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
