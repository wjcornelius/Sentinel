# PoE URL Capability Test Protocol

**Date:** October 30, 2025
**Purpose:** Systematically test what URLs Claude (PoE) can and cannot access
**Tester:** wjcornelius
**Test Subject:** Claude 4.5 Sonnet via PoE

---

## How to Use This Document

**For each test below:**
1. Copy the "Prompt to PoE" text
2. Paste into PoE chat with Claude 4.5 Sonnet
3. Record Claude's response in the "Result" column
4. Mark ✅ (success), ❌ (failure), or ⚠️ (partial)

---

## Test Suite 1: Basic GitHub File Access

### Test 1A: Small Markdown File (README)
**Hypothesis:** Should work perfectly (simple, small, text-only)

**Prompt to PoE:**
```
Can you read and summarize this file?

https://github.com/wjcornelius/Sentinel/blob/main/README.md

Please tell me:
1. Can you access it? (Yes/No)
2. What is the first heading in the file?
3. Approximately how many lines is it?
```

**Expected Result:** ✅ Should see content
**Actual Result:** _[Record here]_

---

### Test 1B: Large Documentation File (CHANGELOG)
**Hypothesis:** Should work (text-only, but larger ~600 lines)

**Prompt to PoE:**
```
Can you read this file and tell me what the most recent version entry is?

https://github.com/wjcornelius/Sentinel/blob/main/CHANGELOG.md

Please tell me:
1. Can you access it? (Yes/No)
2. What is the most recent version number?
3. What date is listed for that version?
```

**Expected Result:** ✅ Should see content
**Actual Result:** _[Record here]_

---

### Test 1C: Python Source Code (Main Workflow)
**Hypothesis:** Should work (code is just text)

**Prompt to PoE:**
```
Can you read this Python file and identify the main function?

https://github.com/wjcornelius/Sentinel/blob/main/sentinel_morning_workflow.py

Please tell me:
1. Can you access it? (Yes/No)
2. What is the name of the main function?
3. How many "STEP" comments do you see?
```

**Expected Result:** ✅ Should see content
**Actual Result:** _[Record here]_

---

### Test 1D: Python Module (Portfolio Optimizer)
**Hypothesis:** Should work (new file, critical module)

**Prompt to PoE:**
```
Can you read this Python module and tell me what AI model it uses?

https://github.com/wjcornelius/Sentinel/blob/main/sentinel/portfolio_optimizer.py

Please tell me:
1. Can you access it? (Yes/No)
2. What OpenAI model does it use? (Search for "model=" in the code)
3. What is the main class name?
```

**Expected Result:** ✅ Should see content
**Actual Result:** _[Record here]_

---

## Test Suite 2: Edge Cases

### Test 2A: File in Subdirectory
**Hypothesis:** Should work (just a deeper path)

**Prompt to PoE:**
```
Can you read this file in a subdirectory?

https://github.com/wjcornelius/Sentinel/blob/main/sentinel/tier1_technical_filter.py

Please tell me:
1. Can you access it? (Yes/No)
2. What is the main class name?
3. What does this module do? (1 sentence)
```

**Expected Result:** ✅ Should see content
**Actual Result:** _[Record here]_

---

### Test 2B: File with Spaces in Name
**Hypothesis:** Might fail (URL encoding issues)

**Prompt to PoE:**
```
Can you read this file with spaces in the filename?

https://github.com/wjcornelius/Sentinel/blob/main/Project%20Charter%20-%20The%20Sentinel%20Portfolio%20Manager%20-%20Version%202.0

Please tell me:
1. Can you access it? (Yes/No)
2. If yes, what is the first line?
```

**Expected Result:** ⚠️ Might fail (URL encoding)
**Actual Result:** _[Record here]_

---

### Test 2C: Config Example File
**Hypothesis:** Should work (Python file)

**Prompt to PoE:**
```
Can you read this config example file?

https://github.com/wjcornelius/Sentinel/blob/main/config.example.py

Please tell me:
1. Can you access it? (Yes/No)
2. What API keys does it define? (List the variable names)
```

**Expected Result:** ✅ Should see content
**Actual Result:** _[Record here]_

---

## Test Suite 3: Multiple URLs (Critical Test)

### Test 3A: Two URLs in Same Message
**Hypothesis:** Will FAIL or only read first URL

**Prompt to PoE:**
```
Can you read both of these files and compare them?

File 1: https://github.com/wjcornelius/Sentinel/blob/main/README.md
File 2: https://github.com/wjcornelius/Sentinel/blob/main/WORKFLOW_PROTOCOL.md

Please tell me:
1. Can you see both files? (Yes/No)
2. If no, which one can you see?
3. If yes, what do they have in common?
```

**Expected Result:** ❌ Likely only sees first URL
**Actual Result:** _[Record here]_

---

### Test 3B: Sequential URLs (Two Messages)
**Hypothesis:** Should work (one at a time)

**First Message to PoE:**
```
Can you read this file?

https://github.com/wjcornelius/Sentinel/blob/main/README.md

Tell me the first heading.
```

**Second Message to PoE (after he responds):**
```
Now can you read this file?

https://github.com/wjcornelius/Sentinel/blob/main/WORKFLOW_PROTOCOL.md

Tell me the first heading.
```

**Expected Result:** ✅ Both should work
**Actual Result (First):** _[Record here]_
**Actual Result (Second):** _[Record here]_

---

## Test Suite 4: Invalid URLs (Error Handling)

### Test 4A: Non-Existent File
**Hypothesis:** Should report "can't access" gracefully

**Prompt to PoE:**
```
Can you read this file?

https://github.com/wjcornelius/Sentinel/blob/main/THIS_FILE_DOES_NOT_EXIST.py

What happens?
```

**Expected Result:** ❌ Error message
**Actual Result:** _[Record here]_

---

### Test 4B: Wrong Branch Name
**Hypothesis:** Should fail (you mentioned non-main branches don't work)

**Prompt to PoE:**
```
Can you read this file on a feature branch?

https://github.com/wjcornelius/Sentinel/blob/feature-that-doesnt-exist/README.md

What happens?
```

**Expected Result:** ❌ Error message
**Actual Result:** _[Record here]_

---

### Test 4C: Directory URL (Not File)
**Hypothesis:** Should fail or show partial info

**Prompt to PoE:**
```
Can you read this directory?

https://github.com/wjcornelius/Sentinel/tree/main/sentinel

What do you see?
```

**Expected Result:** ❌ Can't browse directory
**Actual Result:** _[Record here]_

---

## Test Suite 5: Performance & Size Limits

### Test 5A: Very Large File
**Hypothesis:** Might truncate or timeout

**Prompt to PoE:**
```
Can you read this database setup file?

https://github.com/wjcornelius/Sentinel/blob/main/database_setup.py

Please tell me:
1. Can you access it? (Yes/No)
2. How many table definitions do you see?
3. Did you see the entire file or was it truncated?
```

**Expected Result:** ⚠️ Might truncate
**Actual Result:** _[Record here]_

---

## Test Suite 6: Special Characters & Encoding

### Test 6A: File with Emoji in Content
**Hypothesis:** Should handle Unicode fine (it's 2025)

**Prompt to PoE:**
```
Can you read this changelog?

https://github.com/wjcornelius/Sentinel/blob/main/CHANGELOG.md

Search for any emoji characters (🏆, ✅, ❌, etc.) and tell me:
1. Can you see emoji?
2. How many different emoji do you find?
```

**Expected Result:** ✅ Should see emoji
**Actual Result:** _[Record here]_

---

## Summary Template

After running all tests, summarize:

**What Works Reliably:**
- [ ] Small markdown files (< 100 lines)
- [ ] Large markdown files (> 500 lines)
- [ ] Python source files
- [ ] Files in subdirectories
- [ ] Files with spaces in names (URL encoded)
- [ ] Sequential URL access (one per message)

**What Doesn't Work:**
- [ ] Multiple URLs in same message
- [ ] Non-existent files
- [ ] Non-main branches
- [ ] Directory URLs
- [ ] Very large files (truncation)

**Observed Limitations:**
- Max file size: _____ lines
- URLs per message: _____ (likely 1)
- Rate limiting: _____ (yes/no)
- Encoding issues: _____ (describe)

**Conclusion:**
_[Your overall assessment of PoE's URL capabilities for the Sentinel workflow]_

---

## Next Steps Based on Results

**If most tests pass:**
→ Current workflow protocol is validated, continue using it

**If multiple URLs work:**
→ Update workflow protocol to allow batch file reviews

**If size limits found:**
→ Split large files or provide line ranges to Claude (PoE)

**If encoding issues:**
→ Avoid special characters in filenames, use URL encoding

---

**Test Session Started:** _[Date/Time]_
**Test Session Completed:** _[Date/Time]_
**Total Tests Run:** _[Number]_
**Success Rate:** _[Percentage]_
