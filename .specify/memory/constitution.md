<!--
Sync Impact Report:
- Version change: initial → 1.0.0
- Modified principles: N/A (initial creation)
- Added sections: Core Principles (5), Technology Stack, Development Standards, Governance
- Removed sections: N/A
- Templates requiring updates:
  ✅ constitution.md (created)
  ✅ plan-template.md (updated with constitution checks and tech context)
  ⚠ spec-template.md (no changes needed - generic template)
  ✅ tasks-template.md (updated with constitution compliance note)
- Follow-up TODOs: None
-->

# NoteBot ChatBot Constitution

## Core Principles

### I. User Experience First (UX-FIRST)

**All features MUST prioritize simple, intuitive user experience.**

- Clean Streamlit interface with minimal friction points
- Chat-based interaction pattern (familiar to users)
- Clear error messages with actionable guidance
- Single-file upload with instant feedback
- Progressive disclosure: basic features visible, advanced features accessible
- Mobile-responsive design where applicable

**Rationale**: User adoption depends on eliminating complexity. A confused user is a lost user.

### II. Basic Features Before Advanced (INCREMENTAL-COMPLEXITY)

**Core functionality MUST be implemented and stable before adding enhancements.**

Basic features (MUST have before v1.0):
- PDF upload and text extraction
- Text chunking and embedding
- Vector search via FAISS
- Question answering with context
- Chat history (session state)

Advanced features (MAY add after v1.0):
- Multiple file support
- Conversation export
- Advanced retrieval strategies
- Custom chunk parameters
- Source citation with page numbers

**Rationale**: Ship working software fast. Iterate based on real usage, not assumptions.

### III. Python-First Stack (TECH-STACK-LOCK)

**The project MUST use the following locked technology stack:**

- **Python 3.10+** for all application code
- **Streamlit** for web interface (mandatory)
- **LangChain** for LLM orchestration (mandatory)
- **Google Generative AI (Gemini)** for embeddings and chat (mandatory)
- **FAISS** (faiss-cpu) for vector storage (mandatory)
- **PyPDF2** for PDF processing (mandatory)

Stack changes require constitution amendment (MAJOR version bump).

**Rationale**: Consistency across codebase. No framework sprawl. Clear dependencies.

### IV. Testing & Quality (TEST-DISCIPLINE)

**All code paths MUST be testable; critical paths MUST have tests.**

- `pytest` is the test framework (mandatory)
- Unit tests for utility functions (parsers, chunkers, validators)
- Integration tests for LangChain chains (mock LLM responses)
- Smoke tests for Streamlit components (basic rendering)
- CI/CD pipeline MUST pass before merge to main
- Test coverage target: 70% for core logic (aspirational)

**Rationale**: Quality gates prevent regressions. Tests document intent.

### V. Security & Privacy (DATA-PROTECTION)

**User data and API keys MUST be protected at all times.**

- API keys MUST use environment variables or Streamlit secrets (never hardcoded)
- Uploaded PDFs processed in-memory only (no persistent storage unless explicitly designed)
- Session state isolated per user (Streamlit default behavior)
- No telemetry or tracking without explicit user consent
- Dependencies scanned for CVEs (via GitHub Dependabot)

**Rationale**: Trust is earned through responsible data handling. Security by default.

## Technology Stack

**Core Dependencies** (pinned in requirements.txt):

```
streamlit==1.39.0          # Web interface
PyPDF2==3.0.1              # PDF text extraction
langchain==0.2.16          # LLM orchestration
langchain-core==0.2.38     # LangChain core abstractions
langchain-google-genai==1.0.10    # Gemini integration
langchain-community==0.2.16       # Community integrations
langchain-text-splitters==0.2.4   # Text chunking
faiss-cpu==1.9.0.post1     # Vector similarity search
python-dotenv==1.0.1       # Environment variable management
pytest==8.3.3              # Testing framework
```

**Dependency Updates**:
- PATCH version updates: automatic (via Dependabot)
- MINOR version updates: manual review required
- MAJOR version updates: constitution review + migration plan required

## Development Standards

### Code Style

- Follow PEP 8 conventions (Python style guide)
- Use descriptive variable names (no single-letter except loop counters)
- Add docstrings for functions/classes with non-obvious behavior
- Inline comments for complex LangChain operations
- Keep functions focused (single responsibility)

### Documentation Requirements

- `README.md` MUST include: project description, setup instructions, usage guide, deployment steps
- `requirements.txt` MUST be up-to-date and pinned
- `.env.example` MUST document all required environment variables
- Significant features MUST have usage examples

### Version Control

- **Branching strategy**: Feature branches → PR → main
- **Commit messages**: Conventional Commits format preferred (`feat:`, `fix:`, `docs:`, `test:`)
- **Pull Requests**: Require passing CI checks before merge
- **Main branch**: Always deployable to Streamlit Cloud

### Deployment

- **Platform**: Streamlit Community Cloud (primary)
- **Environment**: Python 3.10+ (match development)
- **Secrets**: Managed via Streamlit Cloud secrets (TOML format)
- **Monitoring**: Application logs via Streamlit Cloud dashboard

## Governance

**Amendment Process**:
1. Propose change via GitHub issue (label: `constitution-amendment`)
2. Document rationale and impact analysis
3. Update constitution with version bump:
   - MAJOR: Breaking changes to principles or tech stack
   - MINOR: New principles or expanded guidance
   - PATCH: Clarifications or typo fixes
4. Update dependent templates/docs
5. Commit with message: `docs: amend constitution to vX.Y.Z (summary)`

**Compliance Validation**:
- All PRs MUST reference constitution principles if introducing new patterns
- CI/CD checks enforce testing standards (Principle IV)
- Code reviews verify UX-first approach (Principle I)
- Dependency updates follow tech stack rules (Principle III)

**Constitution Supremacy**:
This constitution overrides all other project documentation in case of conflict. When in doubt, refer here first.

**Version**: 1.0.0 | **Ratified**: 2025-10-23 | **Last Amended**: 2025-10-23
