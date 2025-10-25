# API Contracts: Session State Chat History

**Feature**: Session state chat history implementation  
**Date**: 2025-10-25  
**Phase**: Phase 1 - Design & Contracts  

## Internal Python API

Since this is a Streamlit application, we define internal function contracts rather than REST endpoints.

### ChatHistoryManager

#### `add_message(role: str, content: str, metadata: dict = None) -> None`

**Purpose**: Add a new message to chat history

**Parameters**:
- `role`: Message sender ("user" | "assistant")
- `content`: Message text content (max 10,000 chars)
- `metadata`: Optional metadata dictionary

**Behavior**:
- Validates input parameters
- Generates timestamp and message ID
- Adds to session state chat history
- Triggers storage save operation
- Enforces 50-message limit with cleanup

**Error Handling**:
- `ValueError`: Invalid role or empty content
- `StorageError`: Storage save failure (non-fatal)

#### `get_chat_history() -> List[dict]`

**Purpose**: Retrieve current chat history

**Returns**: List of ChatMessage dictionaries in chronological order

**Behavior**:
- Returns copy of current session state
- Includes all messages from current session
- Preserves message ordering

#### `clear_history() -> None`

**Purpose**: Clear all chat history (new document upload)

**Behavior**:
- Clears session state chat history
- Resets document metadata
- Updates storage with empty state
- Resets vector store status

#### `get_conversation_context(last_n: int = 5) -> dict`

**Purpose**: Generate conversation context for AI responses

**Parameters**:
- `last_n`: Number of recent exchanges to include

**Returns**: ConversationContext dictionary

**Behavior**:
- Extracts recent Q&A pairs
- Generates conversation summary
- Includes document context
- Formats for LangChain consumption

### SessionManager

#### `initialize_session() -> str`

**Purpose**: Initialize new session or restore existing one

**Returns**: Session ID string

**Behavior**:
- Generates new session ID if needed
- Loads chat history from sessionStorage
- Validates and cleans loaded data
- Sets up session state variables

**Error Handling**:
- Corrupted data: Reset to clean state
- Storage unavailable: Continue with in-memory only

#### `save_session_data() -> bool`

**Purpose**: Save current session to browser storage

**Returns**: Success status

**Behavior**:
- Serializes session state to JSON
- Saves to sessionStorage via JavaScript
- Updates storage status indicator
- Handles quota exceeded gracefully

#### `get_session_status() -> dict`

**Purpose**: Get current session and storage status

**Returns**: Status information dictionary

**Example**:
```python
{
    "session_id": "session_abc123",
    "storage_status": "active",
    "message_count": 12,
    "document_loaded": True,
    "vector_store_ready": True
}
```

### StorageHandler

#### `load_from_storage() -> dict`

**Purpose**: Load chat data from browser sessionStorage

**Returns**: Parsed session data or empty dict

**Behavior**:
- Executes JavaScript via Streamlit components
- Retrieves sessionStorage data
- Validates and parses JSON
- Handles missing or corrupted data

#### `save_to_storage(data: dict) -> bool`

**Purpose**: Save chat data to browser sessionStorage

**Parameters**:
- `data`: Session data dictionary to save

**Returns**: Success status

**Behavior**:
- Serializes data to JSON
- Executes JavaScript storage operation
- Handles quota exceeded errors
- Updates storage status

#### `clear_storage() -> None`

**Purpose**: Clear all stored session data

**Behavior**:
- Removes sessionStorage entries
- Resets storage status
- Used for new document uploads

## UI Component Contracts

### Chat Display Components

#### `render_chat_history(messages: List[dict]) -> None`

**Purpose**: Render chat history in sidebar

**Parameters**:
- `messages`: List of ChatMessage dictionaries

**Behavior**:
- Displays messages in chronological order
- Shows user/assistant role indicators
- Includes timestamps for each message
- Handles empty state gracefully

#### `render_message_input() -> str`

**Purpose**: Render message input field and return user input

**Returns**: User input string or None

**Behavior**:
- Creates text input widget
- Handles submit button/enter key
- Validates input length
- Clears input after submission

#### `render_status_indicators(status: dict) -> None`

**Purpose**: Display session and storage status

**Parameters**:
- `status`: Status dictionary from SessionManager

**Behavior**:
- Shows document loaded indicator
- Displays message count
- Shows storage status warnings
- Renders vector store readiness

### Error Handling Components

#### `show_storage_warning(error_type: str) -> None`

**Purpose**: Display storage-related warnings to user

**Parameters**:
- `error_type`: Type of storage error ("quota", "disabled", "corrupted")

**Behavior**:
- Shows appropriate warning message
- Explains impact on functionality
- Provides actionable guidance
- Non-blocking display

## Integration Contracts

### LangChain Integration

#### `format_for_langchain(context: dict) -> List[dict]`

**Purpose**: Format conversation context for LangChain chains

**Parameters**:
- `context`: ConversationContext from ChatHistoryManager

**Returns**: LangChain-compatible message list

**Example Output**:
```python
[
    {"role": "human", "content": "What is renewable energy?"},
    {"role": "ai", "content": "Renewable energy refers to..."},
    {"role": "human", "content": "Tell me about solar panels"}
]
```

#### `extract_ai_response(chain_response: dict) -> str`

**Purpose**: Extract response content from LangChain output

**Parameters**:
- `chain_response`: Response from LangChain chain execution

**Returns**: Clean response text for chat history

**Behavior**:
- Extracts content from chain response
- Strips formatting artifacts
- Handles error responses
- Validates response format

### Streamlit Integration

#### `sync_session_state() -> None`

**Purpose**: Synchronize Streamlit session state with chat data

**Behavior**:
- Updates st.session_state variables
- Maintains consistency between UI and data
- Handles Streamlit rerun scenarios
- Preserves user interaction state

## Error Response Contracts

### Standard Error Format

All error responses follow consistent format:

```python
{
    "error": True,
    "error_type": "validation|storage|system",
    "message": "Human-readable error description",
    "details": {
        "field": "specific field with error",
        "value": "problematic value",
        "constraint": "violated constraint"
    },
    "recoverable": True,  # Whether user can retry
    "timestamp": "2025-10-25T14:30:15Z"
}
```

### Error Categories

#### Validation Errors
- Invalid role values
- Empty message content
- Oversized content
- Malformed metadata

#### Storage Errors
- sessionStorage quota exceeded
- Browser storage disabled
- Data serialization failures
- Corrupted stored data

#### System Errors
- Streamlit component failures
- Session state inconsistencies
- JavaScript execution errors
- Memory allocation issues

## Testing Contracts

### Unit Test Interfaces

Each function must be testable with:
- Valid input scenarios
- Invalid input handling
- Edge case behavior
- Error condition responses
- Performance characteristics

### Integration Test Scenarios

- Full chat session lifecycle
- Storage persistence across page refreshes
- Error recovery workflows
- Multi-message conversations
- Document upload with history clearing

### Mock Interfaces

For testing without browser dependencies:

```python
class MockStorageHandler:
    def __init__(self):
        self._storage = {}
    
    def load_from_storage(self) -> dict:
        return self._storage.copy()
    
    def save_to_storage(self, data: dict) -> bool:
        self._storage.update(data)
        return True
```

This contract specification ensures all components have clear, testable interfaces while maintaining flexibility for implementation details.