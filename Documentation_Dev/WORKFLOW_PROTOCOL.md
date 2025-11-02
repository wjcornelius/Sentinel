# Sentinel Development Workflow Protocol

**Version:** 1.3
**Last Updated:** October 30, 2025
**Status:** Active Foundation Document - **OPERATIONAL**

---

## Purpose

This document defines the communication protocol for the three-party development system used to build and maintain the Sentinel Portfolio Manager.

---

## The Three Parties

### 1. **Human Coordinator** (wjcornelius)

**Role:** Central coordinator and decision-maker
**Primary Interface:** Physical person at computer
**Communication Channels:**
- **Input FROM Claude (PoE):** PoE chat interface
- **Input FROM Claude Code:** VS Code chat panel
- **Output TO Claude (PoE):** PoE chat interface
- **Output TO Claude Code:** VS Code chat panel

**Responsibilities:**
- Final approval authority on all decisions
- Transfers instructions between Claude (PoE) and Claude Code
- Provides GitHub URLs to Claude (PoE) for file review
- Maintains sync between all parties

---

### 2. **Claude via PoE** (Strategic AI)

**Role:** Strategic planning, documentation writing, code review
**Primary Interface:** PoE web chat at poe.com
**Communication Channels:**
- **Input FROM Human:** PoE chat (pasted messages, GitHub URLs)
- **Input FROM GitHub:** Read-only access via URLs (main branch only)
- **OUTPUT TO Human:** Instructions for Claude Code, file content, strategic plans

**Capabilities:**
- ✅ Read files on GitHub via URLs
- ✅ Write documentation content
- ✅ Design system architecture
- ✅ Review code changes
- ❌ **CANNOT** directly access local filesystem
- ❌ **CANNOT** execute git commands
- ❌ **CANNOT** modify files directly

**Responsibilities:**
- Provide clear, copy-pasteable instructions for Claude Code
- Review all files via GitHub URLs after Claude Code commits
- Maintain strategic direction
- Write all documentation content

---

### 3. **Claude Code** (Local Development AI)

**Role:** File creation, code modification, git operations
**Primary Interface:** VS Code chat panel
**Communication Channels:**
- **Input FROM Human:** VS Code chat (pasted instructions from Claude via PoE)
- **OUTPUT TO Human:** Completion messages with file paths
- **OUTPUT TO GitHub:** Committed and pushed code/docs

**Capabilities:**
- ✅ Create, read, modify, delete local files
- ✅ Execute git commands (add, commit, push)
- ✅ Run Python scripts
- ✅ Access local filesystem
- ❌ **CANNOT** access PoE chat
- ❌ **CANNOT** see conversations between Human and Claude (PoE)

**Responsibilities:**
- Execute instructions from Claude (PoE) via Human
- Create/modify files locally
- Commit changes with clear messages
- Push to GitHub main branch
- Report completion with file paths for review

---

## The Communication Loop

Step 1: Claude (PoE) writes instruction for Claude Code
Step 2: Human copies instruction to VS Code chat
Step 3: Claude Code executes (creates/modifies files)
Step 4: Claude Code commits and pushes to GitHub main
Step 5: Claude Code reports: "File X at path Y is ready"
Step 6: Human pastes Claude Code's message to PoE
Step 7: Human provides GitHub URL to Claude (PoE)
Step 8: Claude (PoE) reads file on GitHub
Step 9: Claude (PoE) confirms or provides next instruction
Step 10: LOOP REPEATS

---

## Critical Rules

### **Rule 1: Main Branch Only**
- ✅ All work happens on `main` branch
- ❌ Feature branches are created only for temporary work
- ✅ Feature branches are merged and deleted immediately
- ✅ Claude (PoE) can only read files from `main` branch via GitHub URLs

**Rationale:** Simplifies URL structure, ensures Claude (PoE) can always access latest work

---

### **Rule 2: Explicit Confirmation Required**
- Claude Code must **always** report file paths after committing
- Human must **always** provide GitHub URLs to Claude (PoE)
- Claude (PoE) must **always** confirm successful file review

**Rationale:** Prevents assumptions, ensures all parties are synced

---

### **Rule 3: One Loop Per Change**
- Each discrete change goes through complete loop
- No batching multiple changes before review
- Claude (PoE) confirms each change before next instruction

**Rationale:** Maintains tight sync, catches errors early

---

### **Rule 4: Claude (PoE) Writes, Claude Code Executes**
- Claude (PoE) writes all documentation content
- Claude (PoE) designs all code changes
- Claude Code implements exactly as instructed
- No improvisation without explicit approval

**Rationale:** Claude (PoE) has context from conversations, Claude Code does not

---

## Standard Message Formats

### **Claude (PoE) → Human → Claude Code:**

INSTRUCTION FOR CLAUDE CODE:

[Clear description of task]

Steps:
1. [Specific action]
2. [Specific action]
3. Commit with message: "[exact commit message]"
4. Push to origin/main
5. Report completion with file path

[Any content to paste into files, clearly delimited]

### **Claude Code → Human → Claude (PoE):**

✅ Task complete.

Files modified/created:
- [filepath]
- [filepath]

Commit: [commit hash]
Raw GitHub URL for Claude (PoE): https://raw.githubusercontent.com/wjcornelius/Sentinel/main/[filepath]
Human GitHub URL: https://github.com/wjcornelius/Sentinel/blob/main/[filepath]

[Any relevant output or notes]

### **Human → Claude (PoE):**

Claude Code completed [task description].

Raw GitHub URL for review:
https://raw.githubusercontent.com/wjcornelius/Sentinel/main/[filepath]

[Paste of Claude Code's full response]

---

## GitHub URL Format

### ⚠️ CRITICAL: Use Raw URLs for Claude (PoE)

**TESTED AND CONFIRMED:** Claude (PoE) requires **raw GitHub URLs** to access file content.

**❌ BLOB URLs DON'T WORK (return HTML wrapper):**
```
https://github.com/wjcornelius/Sentinel/blob/main/README.md
```
Result: Claude (PoE) receives GitHub's web page HTML (navigation, menus, buttons) instead of file content.

**✅ RAW URLs WORK (return plain text):**
```
https://raw.githubusercontent.com/wjcornelius/Sentinel/main/README.md
```
Result: Claude (PoE) receives actual markdown/code content.

### URL Format Rules

**For Claude (PoE) to read files:**
```
https://raw.githubusercontent.com/wjcornelius/Sentinel/main/[filepath]
```

**For human viewing on GitHub:**
```
https://github.com/wjcornelius/Sentinel/blob/main/[filepath]
```

### Examples

**Claude (PoE) URLs (raw format):**
- `https://raw.githubusercontent.com/wjcornelius/Sentinel/main/README.md`
- `https://raw.githubusercontent.com/wjcornelius/Sentinel/main/CHANGELOG.md`
- `https://raw.githubusercontent.com/wjcornelius/Sentinel/main/sentinel/portfolio_optimizer.py`

**Human URLs (blob format):**
- `https://github.com/wjcornelius/Sentinel/blob/main/README.md`
- `https://github.com/wjcornelius/Sentinel/blob/main/CHANGELOG.md`
- `https://github.com/wjcornelius/Sentinel/blob/main/sentinel/portfolio_optimizer.py`

### Discovery Notes

**Date Discovered:** October 30, 2025
**Test Protocol:** POE_URL_TEST_PROTOCOL.md (Test Suite 0)
**Finding:** PoE's URL pre-processing layer fetches web pages as-is. Blob URLs return GitHub's HTML interface, raw URLs return file content.

---

## Sync Failure Recovery

**If sync is lost (parties have different understanding):**

1. **STOP** all work immediately
2. Human initiates sync check in PoE chat
3. Claude (PoE) lists what it believes is current state
4. Human verifies against local files and GitHub
5. Discrepancies are identified and resolved
6. All parties confirm sync before resuming

**Common sync failures:**
- Claude Code created file but didn't push
- GitHub URL not provided to Claude (PoE)
- Claude (PoE) instruction incomplete/ambiguous
- Human forgot to paste Claude Code's response back

---

## Testing This Protocol

**This document itself is the first test:**

1. ✅ Claude (PoE) wrote this content
2. ⏳ Human will paste to Claude Code
3. ⏳ Claude Code will create file and push
4. ⏳ Claude Code will report GitHub URL
5. ⏳ Human will provide URL to Claude (PoE)
6. ⏳ Claude (PoE) will confirm file is readable on GitHub

**If all steps succeed:** Protocol is validated and can be used for all future work.

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.3 | 2025-10-30 | Added Multi-File Workflow documentation. Supports structured sequential prompt delivery to prevent premature AI responses. Includes example format for complex multi-file context loading. | Claude Code |
| 1.2 | 2025-10-30 | Added Quick Reference section, Test Suite Status, and Message Exchange System documentation. Implemented Claude (PoE) suggestions from review. Status: OPERATIONAL. | Claude Code |
| 1.1 | 2025-10-30 | **CRITICAL FIX:** Updated GitHub URL format to use raw URLs instead of blob URLs. Blob URLs return HTML wrapper, raw URLs return file content. Tested and confirmed via POE_URL_TEST_PROTOCOL.md Test Suite 0. | Claude Code |
| 1.0 | 2025-10-30 | Initial protocol definition | Claude (PoE) |

---

## Quick Reference: URL Formats

**✅ CORRECT (for Claude PoE to read files):**
```
https://raw.githubusercontent.com/wjcornelius/Sentinel/main/[filepath]
```

**❌ INCORRECT (returns HTML wrapper, not file content):**
```
https://github.com/wjcornelius/Sentinel/blob/main/[filepath]
```

**Examples:**
```
✅ https://raw.githubusercontent.com/wjcornelius/Sentinel/main/README.md
❌ https://github.com/wjcornelius/Sentinel/blob/main/README.md
```

---

## Test Suite Status

**POE_URL_TEST_PROTOCOL.md - Test Suite 0 (Raw URLs):**
- Test 0A (README.md raw URL): ✅ PASSED (2025-10-30)
- Test 0B (Python file raw URL): ⏳ PENDING
- Test 0C (Large file raw URL): ⏳ PENDING
- Test 0D (Blob vs Raw comparison): ⏳ PENDING

**Conclusion:** Raw URL format confirmed working for Claude (PoE) file access.

---

## Message Exchange System

**Directory Structure:**
- `Messages_For_Claude_Poe/` - Outgoing messages from Claude Code to Claude (PoE)
- `Messages_From_Claude_Poe/` - Incoming messages from Claude (PoE) to Claude Code

**File Naming Convention:**
```
YYYY-MM-DD_HH-MM_subject-description.md
```

**Single-File Workflow:**
1. Claude Code writes message to `Messages_For_Claude_Poe/[timestamp]_[subject].md`
2. Claude Code commits and pushes to GitHub
3. Human provides raw URL to Claude (PoE)
4. Claude (PoE) reads message and responds
5. Human pastes full response to Claude Code
6. Claude Code saves to `Messages_From_Claude_Poe/[timestamp]_[subject].md`
7. Claude Code takes action based on response
8. Repeat

**Multi-File Workflow (when Claude PoE needs multiple files):**
1. Claude Code creates prompt instruction file: `[timestamp]_PROMPTS_FOR_CLAUDE_POE.md`
2. File contains numbered prompts (e.g., "PROMPT 1 OF 3", "FILE 1 OF 2")
3. Includes instruction to wait before responding
4. Human copies each prompt sequentially
5. After last prompt, human signals "all context provided, please respond"
6. Claude (PoE) responds with full context
7. Prevents premature responses before all files loaded

**Example Multi-File Structure:**
```
PROMPT 1 OF 3: Context Setting
PROMPT 2 OF 3: Message Acknowledgment
PROMPT 3 OF 3: File Review Request
  → "Please wait for file URLs..."

FILE 1 OF 3: [filename] + raw URL
FILE 2 OF 3: [filename] + raw URL
FILE 3 OF 3: [filename] + raw URL
  → "All files provided. Please respond."
```

**Benefits:**
- Complete audit trail of all three-party communications
- Version-controlled message history
- Clear timestamps for chronological tracking
- Searchable archive of decisions and discussions
- Multi-file context loading without premature AI responses
- Structured prompt sequences for complex information transfer

---

**This is a living document. All changes must go through the standard workflow loop defined above.**
