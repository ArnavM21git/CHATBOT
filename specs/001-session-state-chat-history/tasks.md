# Tasks: Session State Chat History

**Input**: Design documents from `/specs/001-session-state-chat-history/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Constitution Compliance**: All tasks must align with project principles:
- UX-FIRST: Prioritize user experience and simplicity
- INCREMENTAL-COMPLEXITY: Basic features before advanced
- TECH-STACK-LOCK: Use approved stack only (Python, Streamlit, LangChain, Gemini, FAISS, PyPDF2)
- TEST-DISCIPLINE: Include test tasks for critical paths
- DATA-PROTECTION: Secure API keys, protect user data

**Tests**: Tests are OPTIONAL for this feature - focusing on implementation and manual testing via quickstart scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single Streamlit project**: Root-level Python files with supporting modules
- **Test structure**: `tests/unit/`, `tests/integration/`, `tests/smoke/`
- Follows existing ChatBot.py structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for session state chat history

- [X] T001 Create project directory structure per implementation plan from specs/001-session-state-chat-history/plan.md
- [X] T002 [P] Create tests/unit/ directory for chat history unit tests
- [X] T003 [P] Create tests/integration/ directory for chat session integration tests
- [X] T004 [P] Create tests/smoke/ directory for Streamlit component smoke tests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core session management infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Implement StorageHandler class for browser sessionStorage operations in storage_handler.py
- [X] T006 Implement SessionManager class for session state coordination in session_manager.py
- [X] T007 Implement ChatHistoryManager class for chat history management in chat_history.py
- [X] T008 Create ChatMessage data structure validation utilities in chat_history.py
- [X] T009 Implement sessionStorage JavaScript integration via Streamlit components in storage_handler.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Persistent Chat Conversation (Priority: P1) 🎯 MVP

**Goal**: Enable users to maintain conversation context across page refreshes within browser sessions, with chat history displayed in sidebar and full context preservation

**Independent Test**: Upload a document, ask 3-5 questions in sequence, refresh page, and verify all previous exchanges remain visible and contextually available

### Implementation for User Story 1

- [X] T010 [P] [US1] Create chat history display component in sidebar section of ChatBot.py
- [X] T011 [P] [US1] Implement message input widget with submit handling in ChatBot.py
- [X] T012 [US1] Integrate ChatHistoryManager.add_message() calls for user questions in ChatBot.py
- [X] T013 [US1] Integrate ChatHistoryManager.add_message() calls for AI responses in ChatBot.py
- [X] T014 [US1] Implement chat history persistence across page refreshes using SessionManager in ChatBot.py
- [X] T015 [US1] Add visual indicators for user vs assistant messages in chat display
- [X] T016 [US1] Implement conversation context building for follow-up questions using ChatHistoryManager.get_conversation_context()
- [X] T017 [US1] Add LangChain integration for contextual responses using conversation history

**Checkpoint**: At this point, User Story 1 should be fully functional - users can have persistent conversations with context across page refreshes

---

## Phase 4: User Story 2 - Session Isolation (Priority: P2)

**Goal**: Ensure complete isolation between different browser sessions/tabs, with automatic session cleanup and privacy protection

**Independent Test**: Open two browser sessions/tabs, upload different documents, have conversations in each, verify no cross-contamination, then close/reopen browser to verify session clearing

### Implementation for User Story 2

- [X] T018 [P] [US2] Implement session ID generation and uniqueness in SessionManager.initialize_session()
- [X] T019 [P] [US2] Add session isolation validation in SessionManager
- [X] T020 [US2] Implement session data clearing on browser close behavior via sessionStorage in StorageHandler
- [X] T021 [US2] Add session status indicators in sidebar of ChatBot.py
- [X] T022 [US2] Implement cross-session data validation and isolation checks in SessionManager
- [X] T023 [US2] Add privacy protection measures for session data in StorageHandler

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - persistent conversations with complete session isolation

---

## Phase 5: User Story 3 - Context-Aware Responses (Priority: P3)

**Goal**: Enable AI to use conversation history for more relevant responses, avoiding repetition and building on previous exchanges

**Independent Test**: Ask follow-up questions that require context from previous exchanges, ask same question twice, verify responses acknowledge conversation history appropriately

### Implementation for User Story 3

- [X] T024 [P] [US3] Implement conversation context aggregation in ChatHistoryManager.get_conversation_context()
- [X] T025 [P] [US3] Create conversation summary generation utilities in chat_history.py
- [X] T026 [US3] Integrate conversation context into LangChain prompt templates in ChatBot.py
- [X] T027 [US3] Implement context-aware response generation using previous conversation history
- [X] T028 [US3] Add conversation context validation and formatting for AI prompts
- [X] T029 [US3] Implement repetition detection and acknowledgment in responses

**Checkpoint**: All user stories should now be independently functional - full conversational AI with memory, isolation, and contextual awareness

---

## Phase 6: Edge Cases & Error Handling

**Purpose**: Handle edge cases and error scenarios defined in specification

- [X] T030 [P] Implement 50-message limit with Q&A pair cleanup in ChatHistoryManager._cleanup_if_needed()
- [X] T031 [P] Add storage failure graceful degradation with warning messages in StorageHandler
- [X] T032 [P] Implement new document upload history clearing in SessionManager.handle_new_document_upload()
- [X] T033 Add browser storage quota exceeded error handling in StorageHandler.save_to_storage()
- [X] T034 Implement session recovery from corrupted storage data in SessionManager
- [X] T035 Add performance monitoring for large conversation histories in ChatHistoryManager

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [X] T036 [P] Add status indicators for storage availability and message count in ChatBot.py sidebar
- [X] T037 [P] Implement clear history button functionality in ChatBot.py
- [X] T038 [P] Add timestamp display formatting for chat messages in chat display component
- [X] T039 Add comprehensive error message improvements across all components
- [X] T040 Optimize chat history rendering performance for 50+ messages
- [X] T041 Run quickstart.md validation scenarios end-to-end
- [X] T042 [P] Add debug mode with session state inspection (if checkbox enabled)
- [X] T043 [P] Code cleanup and documentation improvements across all modules

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Edge Cases (Phase 6)**: Depends on all user stories being complete
- **Polish (Phase 7)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but integrates with SessionManager
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on ChatHistoryManager from US1

### Within Each User Story

- UI components before integration with managers
- Manager method calls after manager implementations exist
- Core functionality before visual enhancements
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks can run sequentially (dependencies between managers)
- Once Foundational phase completes, all user stories can start in parallel
- UI components within stories marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch parallel UI components for User Story 1:
Task: "Create chat history display component in sidebar section of ChatBot.py"
Task: "Implement message input widget with submit handling in ChatBot.py"

# Then sequential integration tasks:
Task: "Integrate ChatHistoryManager.add_message() calls for user questions in ChatBot.py"
Task: "Integrate ChatHistoryManager.add_message() calls for AI responses in ChatBot.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - CRITICAL foundation
3. Complete Phase 3: User Story 1 (T010-T017)
4. **STOP and VALIDATE**: Test persistent chat conversation independently using quickstart.md scenarios
5. Deploy/demo basic conversational memory capability

### Incremental Delivery

1. Complete Setup + Foundational → Session management foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP conversational memory!)
3. Add User Story 2 → Test independently → Deploy/Demo (+ session isolation)
4. Add User Story 3 → Test independently → Deploy/Demo (+ contextual AI responses)
5. Add Edge Cases → Handle error scenarios → Deploy/Demo (production-ready)
6. Add Polish → Final improvements → Deploy/Demo (feature complete)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (sequential dependencies)
2. Once Foundational is done:
   - Developer A: User Story 1 (persistent conversations)
   - Developer B: User Story 2 (session isolation)
   - Developer C: User Story 3 (contextual responses)
3. Stories complete and integrate independently

---

## Testing Strategy

### Manual Testing (Primary)

- Use quickstart.md scenarios for each user story
- Test all acceptance scenarios from spec.md
- Validate success criteria measurements
- Test edge cases and error conditions

### Validation Checklist Per Story

**User Story 1**:
- ✅ Upload document, ask 5 questions, verify all visible
- ✅ Refresh page, verify conversation history preserved  
- ✅ Ask "Can you elaborate on that?", verify context reference works

**User Story 2**:
- ✅ Open two browser sessions, verify isolated conversations
- ✅ Close browser, reopen, verify fresh session starts
- ✅ Multiple tabs show independent chat histories

**User Story 3**:
- ✅ Ask follow-up questions requiring previous context
- ✅ Ask same question twice, verify AI acknowledges repetition
- ✅ Complex multi-turn conversation maintains coherent context

### Performance Validation

- ✅ Conversation history renders in <2s for 50 messages
- ✅ Response generation stays <10s with 20+ exchanges  
- ✅ Document processing + vector setup completes <30s
- ✅ Storage operations complete <50ms per save/load

---

## Total Summary

- **Total Tasks**: 43 tasks across 7 phases
- **User Story 1 Tasks**: 8 tasks (T010-T017) - MVP foundation
- **User Story 2 Tasks**: 6 tasks (T018-T023) - Session isolation  
- **User Story 3 Tasks**: 6 tasks (T024-T029) - Contextual AI
- **Parallel Opportunities**: 15 tasks marked [P] can run in parallel within their phases
- **Independent Test Criteria**: Each user story has clear validation scenarios from quickstart.md
- **MVP Scope**: Phases 1-3 (Setup + Foundational + User Story 1) = 17 tasks for basic conversational memory

**Format Validation**: ✅ All tasks follow required checklist format with task IDs, [P] markers where applicable, [US#] story labels for user story phases, and specific file paths in descriptions.

**Ready for Implementation**: Each task is specific enough for immediate execution with clear deliverables and file locations based on the technical design from research.md, data-model.md, and contracts/api-contracts.md.