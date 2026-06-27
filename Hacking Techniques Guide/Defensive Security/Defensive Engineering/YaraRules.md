# YARA Rules — Defensive Engineering Master Guide

## Table of Contents
1. [What is YARA?](#what-is-yara)
2. [Core Rule Anatomy](#core-rule-anatomy)
3. [Rule Sections in Depth](#rule-sections-in-depth)
4. [String Types](#string-types)
5. [Condition Operators & Expressions](#condition-operators--expressions)
6. [YARA Modules](#yara-modules)
7. [Advanced Features](#advanced-features)
8. [Performance Optimization](#performance-optimization)
9. [Defensive Engineering Use Cases](#defensive-engineering-use-cases)
10. [Rule Development Lifecycle](#rule-development-lifecycle)
11. [YARA Command-Line Reference](#yara-command-line-reference)
12. [Integration Ecosystem](#integration-ecosystem)
13. [Writing Robust Rules — Patterns & Anti-Patterns](#writing-robust-rules--patterns--anti-patterns)
14. [Real-World Rule Examples](#real-world-rule-examples)
15. [YARA 4.x Features](#yara-4x-features)
16. [Common Pitfalls](#common-pitfalls)
17. [YARA Engine Architecture](#yara-engine-architecture)
18. [Complete YARA Syntax Specification](#complete-yara-syntax-specification)
19. [Python yara-python API](#python-yara-python--full-api-reference)
20. [Rule Management at Scale](#rule-management-at-scale)
21. [YARA as a Service](#yara-as-a-service-rest-api)
22. [Memory Analysis](#yara-for-memory-analysis--process-memory-scanning)
23. [Linux/macOS Forensics](#yara-for-linuxmacos-forensics)
24. [Container Security](#yara-for-container-security)
25. [OT/ICS](#yara-for-otics)
26. [Mobile](#yara-for-mobile-androidios)
27. [Sigma Translation](#sigma--yara-translation-guide)
28. [OpenIOC Translation](#openioc--yara-translation)
29. [Network PCAP Analysis](#yara-for-network-pcap-analysis)
30. [Registry Scanning](#yara-for-registry-hive-scanning)
31. [Event Log Scanning](#yara-for-evtx-windows-event-log-scanning)
32. [Anti-Forensics Detection](#yara-for-anti-forensics-detection)
33. [PDF Analysis](#yara-for-pdf-analysis)
34. [Office Documents Deep Dive](#yara-for-office-documents-deep-dive)
35. [Anti-YARA Detection](#yara-obfuscation--evasion-detection)
36. [Benchmarking & Profiling](#yara-benchmarking--profiling)
37. [Cloud Deployments](#yara-in-cloud-environments)
38. [Alternative Implementations](#yara-alternative-implementations)
39. [Event-Driven Architecture](#yara-event-driven-architecture-kafka)
40. [osquery Integration](#yara-with-osquery-integration)
41. [Limits & Hardening](#yara-limits--hardening)
42. [3.x → 4.x Migration](#yara-3x--4x-migration-guide)
43. [Complete Function Reference](#complete-yara-built-in-function-reference)
44. [Scoring & Confidence System](#yara-rule-scoring--confidence-system)
45. [Rule Templates](#yara-rule-templates-for-rapid-development)
46. [Quality Checklist](#yara-rule-quality-checklist)
47. [CI/CD Automation](#yara-rule-lifecycle-automation-cicd)
48. [Error Codes & Debugging](#yara-error-codes--debugging)
49. [Redis Caching](#yara-caching-layer-redis)
50. [Appendix A: Quick Reference Card](#appendix-a-quick-reference-card)
51. [Appendix B: Installation Guide](#appendix-b-yara-installation-guide)
52. [Appendix C: Benign Corpora](#appendix-c-sample-benign-corpus-sources)
53. [References & Further Reading](#references--further-reading)

---

## What is YARA?

YARA (Yet Another Ridiculous Acronym) is a pattern-matching Swiss Army knife for malware researchers and defenders, created by Victor M. Alvarez at VirusTotal. It identifies malware families by describing patterns in **files** or **process memory** using declarative rules.

**Core Capabilities:**
- Scan files, directories, process memory, network streams
- Match text (ASCII/wide), hex byte sequences, and regular expressions
- Parse PE, ELF, Mach-O, Cuckoo sandbox JSON, and more via modules
- Compute hashes, entropy, file metadata, and numeric conditions
- Chain rules via dependencies (`rule A : B`)
- Parallel scanning with multi-threaded `-j` flag

**Why YARA in Defensive Engineering?**
- **Signature-based detection** — bridges the gap between AV signatures (limited) and behavioral detection (expensive)
- **Indicator of Compromise (IOC) sharing** — YARA is the de facto standard for sharing detection logic across teams and communities
- **Flexibility** — rules can target file content, memory, packet payloads, or any byte stream
- **Lightweight** — low overhead, suitable for endpoint scanning at scale
- **Integrations** — native support in Velociraptor, Volatility, THOR, Rekall, Cortex XSOAR, TheHive, MISP, Elastic, and custom pipelines

---

## Core Rule Anatomy

A YARA rule is a single file (`.yar` or `.yara`) containing one or more rule blocks:

```yara
rule RuleName : Tag1 Tag2 {
    meta:
        author = "name"
        date = "2026-06-27"
        description = "Detects thing"
        hash = "8a8f9f..."
        reference = "https://..."
        severity = "high"
        mitre_technique = "T1055"

    strings:
        $text_string = "malicious string"
        $hex_string  = { 6A 40 68 00 30 00 00 6A 14 8D 91 }
        $regex       = /evil\d{2}\.exe/i

    condition:
        $text_string or $hex_string or $regex
}
```

---

## Rule Sections in Depth

### `meta:`
Free-form key-value metadata. Informational only — not evaluated by the engine. Common fields: `author`, `date`, `description`, `hash`, `reference`, `severity`, `mitre_attack_id`, `false_positive`, `tlp`, `score`.

### `strings:`
Named or anonymous pattern definitions. Strings are identifiers starting with `$` or `@`.

### `condition:`
Boolean expression that determines if the rule matches. Supports full logical algebra, arithmetic, counts, iterations, and module access.

---

## String Types

### Text Strings
```yara
$s1 = "malware"                  // case-sensitive ASCII
$s2 = "malware" nocase           // case-insensitive
$s3 = "MALWARE" wide             // UTF-16LE (2 bytes per char)
$s4 = "malware" ascii            // explicit ASCII (default)
$s5 = "malware" wide ascii       // both encodings
$s6 = "malware" xor(0x00-0xff)  // single-byte XOR brute (0x00 = identity)
$s7 = "malware" fullword         // surrounded by non-alphanumeric
$s8 = "Mal"    xor(0x01-0x40) nocase wide
```
- `nocase` — case-insensitive matching (ASCII only)
- `wide` — match UTF-16LE encoding (common in Windows PE files with `L"..."` strings)
- `ascii` — explicit ASCII (default, not needed unless combined with `wide`)
- `xor` — brute-force single-byte XOR at scan time (costly, use sparingly)
- `fullword` — ensures boundaries (non-alphanumeric on both sides)

### Hex Strings
```yara
// Wildcards
$h1 = { 6A 40 ?? 68 00 30 00 00 }    // ?? matches any byte

// Jump (variable-length wildcard)
$h2 = { 6A 40 [2-4] 68 00 30 }       // Any 2 to 4 bytes between
$h3 = { 6A 40 [5] 68 00 }             // Exactly 5 bytes

// Alternation
$h4 = { 6A (40|41|42) 68 00 }        // Byte 40, 41, or 42

// Nested hex (masks — YARA 4.x+)
$h5 = { 8D ?? A0 5E 00 00 00 ?? ?? 48 63 C0
        48 8B 04 C2 48 8D 14 ?? 8B ?? ?? ?? A0
        5E 00 00 00 48 03 ?? ?? 89 ?? 24 28 ?? 8B
        04 8A 48 8D 14 ?? 8B ?? ?? ?? 5E 00 00 00
        48 03 D1 ?? 8B ?? ?? ?? C0 5E 00 00 00 48
        03 ?? ?? 24 08 }
```

**Jump ranges:**
- `[N]` — exactly N bytes
- `[N-]` — N or more bytes (use with extreme caution — expensive)
- `[N-M]` — between N and M bytes
- `[N-M]` combined with alternation inside — very expressive

### Regex Strings
```yara
$re1 = /[Hh][Tt][Tt][Pp][Ss]?:\/\//
$re2 = /[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]+/  // IP:port
$re3 = /\\[a-z]{4}\\[a-z0-9]{8,16}\.exe/i   // pattern like \temp\random.exe
```
- Delimiters: `/pattern/flags`
- Flags: `i` (case insensitive), `s` (dot matches newline)
- Use `$re@idx` to reference match position
- Regex engine is limited — no backreferences, no lookahead/lookbehind
- Performance: **static strings are fastest**, regex is slowest. Prefer hex patterns where possible.

---

## Condition Operators & Expressions

| Operator / Construct | Example | Meaning |
|---|---|---|
| `and`, `or`, `not` | `$a and ($b or not $c)` | Boolean logic |
| `of` | `2 of ($a,$b,$c)` | At least N strings match |
| `of` | `any of them` | At least 1 string matches |
| `of` | `all of them` | All strings match |
| `of` | `all of ($a*)` | All strings starting with `$a` |
| `of` | `1 of ($a,$b) and 2 of ($c*)` | Mix matching |
| `for..of` | `for any of ($a*) : ($ @)` | Iterate & evaluate sub-condition |
| `for..of` | `for all of them : (# > 2)` | Each string must match >2 times |
| `#` | `#a` | Count of matches for string `$a` |
| `@` | `@a` | First offset of match for `$a` (signed int) |
| `@a[i]` | `@a[1]` | Offset of i-th match |
| `!` | `!a` | Match length for `$a` (YARA 4.x+) |
| `defined` | `defined($a)` | True if string `$a` exists in rule |
| `uint8/16/32/64` | `uint32(0) == 0x5A4D` | Read integer at offset (LE default) |
| `int8/16/32/64be` | `uint32be(0) == 0x7F454C46` | Big-endian integer read |
| `uint8/16/32/64` | `uint16(0) == 0x5A4D` | Various sizes |
| `filesize` | `filesize < 500KB` | File size in bytes |
| `entrypoint` | `uint16(entrypoint) == 0xFFFF` | PE entry point offset |
| `matches` | `$a matches /regex/` | Test string against regex |
| `icontains` | `$a icontains "sub"` | Case-insensitive substring |
| `startswith` | `$a startswith "MZ"` | String starts with |
| `endswith` | `$a endswith "\x00\x00"` | String ends with |
| `iequals` | `$a iequals "malware"` | Case-insensitive equality |
| Arithmetic | `#a + #b > 5` | Add/match counts |
| Bitwise | `uint32(0) & 0xFF == 0x4D` | Masking |
| Comparison | `#a > 3 and #a < 10` | Range |

**`of` keyword variants:**
```yara
condition:
    any of them                    // at least 1 string matches
    all of them                    // every defined string matches
    any of ($a,$b,$c)              // at least 1 in the set
    all of ($a*)                   // all strings prefixed $a
    3 of ($a,$b,$c,$d,$e)         // exactly 3 out of 5
    2 of ($a*)                    // 2 of the $a-prefixed strings
    any of ($a,$b*) and 1 of ($c*)
```

**`for..of` iterator (advanced):**
```yara
condition:
    for any of ($a,$b,$c) : ($ at entrypoint and # > 5)
    // Each of the strings must appear >5 times and at least one match at EP

    for all of ($evil*) : (# > 2)
    // Every $evil* string matches more than twice

    for any s in ($a,$b,$c) : (s at 0)
    // Any string at offset 0 (rarely used)

    for any i in (0..100) : (uint16(i * 2) == 0x5A4D)
    // Check every 2-byte chunk for PE header (memory dump scanning)
```

---

## YARA Modules

Modules add structured metadata parsing.

### PE Module
```yara
import "pe"

condition:
    pe.is_pe
    pe.entry_point == 0x1000
    pe.sections[0].name == ".text"
    pe.number_of_sections == 3
    pe.characteristics & pe.IMAGE_FILE_DLL
    pe.sections[1].name == ".rsrc" and pe.sections[1].raw_data_offset == 0x1000
    pe.imports("kernel32.dll","CreateRemoteThread")
    pe.exports("DllMain")
    pe.major_subsystem_version > 5
    pe.suspicious_imports()          // heuristic: known-bad import combos
    pe.imphash() == "abc123..."
    pe.rich_signature.raw_data contains "Rich"
    pe.rich_signature.clear_data contains "Rich"
    pe.overlay.data contains "base64"
    pe.version_info["CompanyName"] contains "Microsoft Corporation"
    pe.number_of_resources > 10
    pe.linker_version.major == 14
```
**Key PE attributes:**
- `.is_pe`, `.is_dll`, `.is_driver`, `.is_exe`, `.is_console`, `.is_gui`
- `.machine` — `pe.MACHINE_I386`, `pe.MACHINE_AMD64`
- `.sections[N].name`, `.virtual_size`, `.raw_size`, `.entropy`, `.characteristics`
- `.imports(dll, [api])` — supports wildcards: `pe.imports("kernel32.dll", "Write*")`
- `.exports(func_name)`, `.number_of_exports`
- `.rich_signature` — Compiler fingerprint (Pdb, Id, Count, Tools)
- `.suspicious_imports()` — heuristics: WriteProcessMemory+CreateRemoteThread
- `.overlay` — data appended after PE signature
- `.imphash()`, `.exphash()`

### ELF Module
```yara
import "elf"

condition:
    elf.is_elf
    elf.type == elf.ET_EXEC
    elf.machine == elf.EM_X86_64
    elf.sections[0].name == ".text"
    elf.sections[0].entropy > 7.0
    elf.dynamic.entries_count > 10
    elf.number_of_sections == 28
    elf.imports("libc.so.6", "system")
    elf.symbols("main")
    elf.segments[0].type == elf.PT_LOAD
    elf.sections[1].name contains "got"
```

### Magic Module
```yara
import "magic"

condition:
    magic.type() contains "PE32"          // libmagic output
    magic.type() contains "PDF document"
    magic.type() contains "Composite Document File V2"  // OLE2/CFB
    magic.mime_type() == "application/x-dosexec"
    magic.mime_type() contains "zip"
```

### Math Module
```yara
import "math"

condition:
    math.entropy(0, filesize) > 7.5      // high entropy → packed/encrypted
    math.entropy(pe.sections[1].offset, pe.sections[1].raw_size) > 7.0
    math.mean(0, filesize) > 127
    math.standard_deviation(0, filesize) < 20
    math.mode(0, filesize) == 0x00
    math.count_in_range(0, filesize, 0x00, 0x1F) > 500
    // Unprintable char count
    math.percentage(0, filesize, 0x00) > 0.5
```

### Hash Module
```yara
import "hash"

condition:
    hash.md5(0, filesize) == "d41d8cd98f00b204e9800998ecf8427e"
    hash.sha1(0, filesize) == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    hash.sha256(0, filesize) == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    // Range hashing
    hash.md5(pe.overlay.offset, pe.overlay.length) == "..."
    // Other: crc32, sha256
```

### String Module
```yara
import "string"

condition:
    string.replacement("old", "new")       // testerino (useful in 4.x)
```

### Cuckoo Module
```yara
import "cuckoo"

condition:
    cuckoo.network.http_request("http://evil.com/")
    cuckoo.network.dns_lookup("evil.com")
    cuckoo.registry.key_exists("HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    cuckoo.filesystem.file_created("C:\\evil.exe")
    cuckoo.sync.mutex("Global\\EvilMutex")
    cuckoo.process("svchost.exe")
```

### DotNET Module
```yara
import "dotnet"

condition:
    dotnet.is_dotnet
    dotnet.assembly_name contains "Trojan"
    dotnet.guid == "F72B1B1B-1B1B-1B1B-1B1B-1B1B1B1B1B1B"
    dotnet.number_of_assemblies > 1
    dotnet.streams["#Strings"].size > 1000
    dotnet.entry_point_rva > 0
    dotnet.strong_name_signature
    dotnet.version.major == 4
```
- Access module tables via `.user_strings`, `.assembly_refs`, `.typedefs`, `.methods`, etc.

### Console/Keyb Modules
```yara
import "console"
// Captures stderr/stdout from external scanner scripts (advanced pipeline use)
```

### Debug Module
```yara
import "debug"
// Debug-only — prints values during rule evaluation. Never used in production.
```

---

## Advanced Features

### Loops `for..of` Iterators

```yara
// Structural iteration over sections
condition:
    for any i in (0..pe.number_of_sections - 1) : (
        pe.sections[i].entropy > 7.5
        and pe.sections[i].name == ".text"
    )

// Iterate with "of" keyword
condition:
    for any of ($a,$b,$c) : (# > 3)

// Iterate over all strings starting with prefix
condition:
    for all of ($import*) : (# > 1)

// Count matches per string with sub-condition
condition:
    for any of ($evil*) : ($ at entrypoint)
```

### Rule Dependencies & Private Rules

```yara
// Private rules — not evaluated unless referenced
private rule PrivateHelper {
    strings:
        $a = "config"
    condition:
        $a
}

// Public rule with dependency
rule DetectC2 : T1071 {
    meta:
        description = "Detects Cobalt Strike"
    strings:
        $b = "MZ"
    condition:
        PrivateHelper and $b
}
```

- `private` keyword suppresses direct matching
- `rule A : B` means `A` extends/inherits from `B` (tag inheritance)
- Rules can reference other rules by name in conditions

### External Variables

Passed at scan time via `-d flag=value`:

```yara
// In rule:
condition:
    #a > EXT_MIN_COUNT

// CLI:
// yara -d EXT_MIN_COUNT=5 rule.yar target
```

Common external variables: `EXTENSION`, `MAX_SIZE`, `MIN_SCORE`, `ENVIRONMENT`, `WHITELIST_MODE`

### Anonymous Strings

```yara
condition:
    "literal string" or { 6A 40 68 00 30 }
```
No `$` identifier needed. Simplifies one-off rules but cannot reference count/offset.

### Global Rules

```yara
global rule GenericPreFilter {
    condition:
        filesize < 10MB
        and (uint16(0) == 0x5A4D or uint32(0) == 0x464C457F)
}
```
- `global` rules run **first** on every file
- If a global rule returns false, the file is **skipped** entirely
- Useful for pre-filtering (e.g., only scan PE/ELF files)

### Modules (Full Reference)

| Module | Source | Scope |
|---|---|---|
| `pe` | YARA built-in | Win PE headers, imports, exports, sections, resources, rich header |
| `elf` | YARA built-in | Linux ELF headers, sections, segments, dynamic linking |
| `macho` | YARA built-in | macOS Mach-O headers, load commands, sections |
| `magic` | libmagic (optional) | File type detection via magic bytes |
| `math` | YARA built-in | Entropy, mean, stddev, percentage statistical analysis |
| `hash` | YARA built-in | MD5, SHA1, SHA256, CRC32 |
| `string` | YARA built-in | String replacement/manipulation (4.x) |
| `dotnet` | YARA built-in | .NET assembly metadata, streams, types, methods |
| `cuckoo` | Cuckoo sandbox | Sandbox behavioral report fields |
| `console` | YARA built-in | Console output capture |
| `debug` | YARA built-in | Debug logging during scanning |

---

## Performance Optimization

YARA scanning speed is dominated by **string matching**. Rules are compiled into an Aho-Corasick automaton.

### Rule Ordering & Aho-Corasick
- All text strings from all rules are compiled into a single Aho-Corasick automaton
- Adding more strings **does not significantly slow down** the automaton (amortized O(n))
- But adding strings increases compile time and memory

### Atomic String Selection
- Prefer short, unique, high-entropy strings (12–32 bytes ideal)
- Avoid very common substrings: `http://`, `www.`, `.exe`, `\x00\x00`, `GetProcAddress`
- Use `fullword` to reduce false-positive matches, which reduces condition evaluation
- Wide strings match 2x the data — use only when necessary
- `xor` strings are **expensive** — YARA brute-forces 256 keys. Limit xor ranges: `xor(0x01-0x40)`

### Condition Short-Circuiting
YARA evaluates conditions left-to-right with short-circuit logic:
```yara
condition:
    // Filesize check is cheap — put it first
    filesize < 1MB and uint16(0) == 0x5A4D and pe.number_of_sections < 5 and $a
```

### Module Usage Costs
- `pe` — fast (parsed once per PE)
- `math.entropy` — O(n) scan of the range; avoid on full filesize when possible
- `hash.md5/sha1/sha256` — O(n); avoid on large files unless necessary
- `magic` — calls libmagic; moderate cost
- `cuckoo` — only on JSON; negligible

### Avoiding False Positives
False positives erode defender trust. Best practices:
1. Combine multiple indicators: `$malicious_string and pe.imports("wininet.dll")`
2. Use entropy checks: `math.entropy(0, filesize) > 6.0` (packed)
3. Add size constraints: `filesize < 2MB`
4. Whitelist known-safe versions via `pe.version_info["ProductVersion"]`
5. Use `fullword` to avoid substring matches in benign strings
6. **Test against a benign corpus** — this is non-negotiable

---

## Defensive Engineering Use Cases

### Malware Detection on Endpoints
- Deployed via YARA-based scanners (THOR, Velociraptor, osquery's YARA table)
- Scan `C:\Windows\Temp`, `%TEMP%`, `%APPDATA%`, `%PROGRAMDATA%`, startup folders
- Scan all running process memory for injected code
- Example: `yara -r -s rules.yar C:\Windows\Temp --scan-list`

### Phishing Document Analysis
- Macro-enabled Office docs (`.docm`, `.xlsm`, `.pptm`) — detect AutoOpen, Shell, URLDownloadToFile
- OLE objects embedded in docx/pptx
- JavaScript/VBScript in `.hta`, `.lnk` attachments
- PDF with embedded JavaScript, `/Launch` actions, or obfuscated `/OpenAction`

### Memory Forensics & Volatility Integration
```bash
# Volatility 3 plugin
volatility -f memory.dmp -o output yarascan.YaraScan --rules=malware.yar
```
- Scan process memory (`yarascan` in Volatility 2, `YaraScan` in Vol 3)
- Scan MFT entries, registry hives
- Extract injected code regions and match against known shellcode patterns

### Network Traffic Analysis
- HTTP response bodies from malware C2
- DNS query names (DGA detection via regex)
- TLS SNI fields with known bad domains
- Using `yara` on `tcpdump` / `pcap` / Zeek logs:
  ```bash
  tshark -r capture.pcap -Y "http.request" -T fields -e http.file_data | yara rules.yar -
  ```

### Supply Chain / Software Composition Analysis
- Detect known malicious DLLs in signed binaries
- Validate binaries against expected rich header hashes
- Flag unsigned executables in critical directories
- CI/CD pipeline gate: `yara rules.yar built-artifact.exe`

### Incident Response Triage
- Run on 10,000+ endpoints via EDR
- Classify files by family: `CobaltStrike`, `Emotet`, `Trickbot`
- Generate IOC lists from matching files
- Automate with `yara` + `jq` + Python for IR workflows

### Hunting & Threat Intelligence Feeds
- Consume public rule sets: **YARA-Rules project**, **YARA Forge**, **Valhalla**, **Inquest**, **NCSC**, **malpedia**
- Convert OpenIOC, STIX, Sigma to YARA
- Correlate across feeds in MISP or ThreatConnect
- Create watchlists for `.gitignore` scanning, config file exfiltration

### YARA in SIEM / SOAR Pipelines
- **Elastic Security:** YARA rules run via Elastic Endpoint integration
- **TheHive / Cortex:** YARA analyzer scans files in case management
- **MISP:** YARA export from event attributes
- **Splunk ES:** Custom YARA scanner app
- **Palo Alto XSOAR:** `YARA-Scan` playbook integration
- **dfir-IRIS:** File scanning with YARA during investigation
- **GRR / Velociraptor:** YARA hunt across all endpoints

---

## Rule Development Lifecycle

### 1. Threat Research Phase
- Obtain sample (malware repository, sandbox, threat feed)
- Analyze: strings, imports, structure, behavior, packing
- Identify discriminators: unique strings, APIs, sections, offsets

### 2. Drafting the Rule
- Start with most unique IOC (high-weight string)
- Add secondary IOCs as safety
- Choose module if PE/ELF-specific

### 3. Testing Against Benign Corpora
- **Critical step** — run against clean Windows/Linux system files, common applications
- Use large, diverse benign sets (e.g., `C:\Windows\System32`, `/usr/bin`)
- Monitor false positive rate; reject if > 0.1%

### 4. Validation Against Ground Truth
- Test against known positives (the sample + variants)
- Confirm recall > 90% on family variants
- Test against packed/unpacked versions

### 5. False Positive Tuning
- Add exclusions via `and not`, `pe.version_info`, file metadata
- Raise threshold: `2 of` → `3 of`
- Tighten regex bounds
- Document known FPs in `meta:`

### 6. Deployment & Monitoring
- Deploy to staging → observe → promote to production
- Monitor alert volume daily for first week
- Maintain alert feedback loop for tuning

### 7. Retirement
- Rules for deprecated/eradicated threats should be moved to archive
- Avoid rule bloat — inactive rules slow compile times and consume memory
- Tag with `status = "retired"` or remove

---

## YARA Command-Line Reference

```bash
# Basic scanning
yara rule.yar target.exe
yara rule.yar directory/                    # Scan directory
yara rule.yar -r directory/                 # Recursive

# Multiple rule files
yara rule1.yar rule2.yar target.exe
yara -s rules/*.yar target.exe             # Globbing

# Output options
yara -s rule.yar target.exe                 # Print matching strings
yara -m rule.yar target.exe                 # Print module metadata
yara -e rule.yar target.exe                 # Print rule namespace
yara -c rule.yar target.exe                 # Print only count
yara -d variable=value rule.yar target      # External vars
yara -x module=key=value rule.yar target    # Module key overrides

# Performance
yara -p 30 rule.yar directory/             # Parallel threads
yara -t rule.yar target.exe                # Tags only
yara --fail-on-warnings rule.yar target    # Strict mode

# Advanced
yara --scan-list targets.txt               # File list
yara --print-meta                          # Meta only
yara --print-identifier                    # Print rule identifier
yara --no-warnings                         # Suppress warnings
yara --max-rules=1000                      # Limit loaded rules

# Scan stdin / pipe
cat file | yara rule.yar -
strings -n 8 malware.bin | yara rule.yar -
```

**Exit codes:** `0` = match found, `1` = error, `2` = no match

---

## Integration Ecosystem

| Tool | Integration Type | Notes |
|---|---|---|
| **Velociraptor** | Native artifact | `Windows.Detection.Yara.Process`, `Windows.Detection.Yara.Files` |
| **Volatility 3** | Plugin | `yarascan.YaraScan` |
| **THOR / Loki** | Built-in scanner | Uses YARA + IOCs |
| **Elastic** | Elastic Endpoint | YARA rule actions in policy |
| **Splunk ES** | App | YARA scanning via TA |
| **osquery** | Table | `yara_events`, `yara_scan` |
| **MISP** | Export | YARA export from attributes |
| **TheHive / Cortex** | Analyzer | `Cortex_analyzer_Yara` |
| **Cuckoo / CAPE** | Processing module | YARA on behavioral artifacts |
| **GRR** | Client action | `YaraProcessScan`, `YaraFileScan` |
| **dfir-IRIS** | Integration | File scanning during case work |
| **ClamAV** | Rules conversion | `clamscan --yara` (experimental) |

---

## Writing Robust Rules — Patterns & Anti-Patterns

### ✅ GOOD patterns

```yara
// Specific, constrained, multi-factor
rule Good_Example {
    meta:
        description = "Specific malware family"
    strings:
        $s1 = { 8B ?? 24 10 8B 40 0C 8B 40 1C 8B 00 8B 40 08 8B 40 20 }
        $s2 = "unique_config_string" fullword
    condition:
        uint16(0) == 0x5A4D and filesize < 2MB and
        #s1 == 1 and $s2
}

// PE-aware, module-gated
rule PE_Aware {
    meta:
        description = "Targets specific PE behavior"
    condition:
        pe.is_pe and
        pe.imports("kernel32.dll", "WriteProcessMemory") and
        pe.imports("kernel32.dll", "CreateRemoteThread") and
        pe.number_of_sections < 6
}

// Entropy-gated (packed malware)
rule High_Entropy_Shellcode {
    condition:
        math.entropy(0, filesize) > 7.0 and
        $shellcode_pattern
}

// Memory scan — loose but focused
rule Injected_Code {
    condition:
        $mz at 0 or uint16(0) == 0x5A4D
}
```

### ❌ BAD anti-patterns

```yara
// Too broad — matches almost anything
rule Bad_TooBroad {
    strings:
        $s = "http://"
    condition:
        $s
}

// No bounds — runs forever
rule Bad_OpenEnded {
    strings:
        $h = { 00 [1000000-] FF }
    condition:
        $h
}

// Only meta-no actual detection logic
rule Bad_MetaOnly {
    meta:
        description = "Catch all"
    condition:
        true          // NEVER do this
}

// Way too many strings, all generic
rule Bad_Fifteen_Strings {
    strings:
        $s1 = ".exe"
        $s2 = ".dll"
        $s3 = "MZ"
        // ...
        $s15 = "kernel32"
    condition:
        any of them    // matches almost every PE
}

// No size check on huge file (OOM risk)
rule Bad_NoSizeCheck {
    condition:
        $a
}

// Overly specific — breaks on minor version changes
rule Bad_Brittle {
    condition:
        hash.md5(0, filesize) == "abc123..."
}
```

---

## Real-World Rule Examples

### Cobalt Strike Beacon
```yara
rule CobaltStrike_Beacon : T1055 T1090 {
    meta:
        author = "Defensive Engineering Team"
        date = "2026-06-27"
        description = "Detects Cobalt Strike Beacon payload"
        mitre_attack_id = "T1055.012, T1090.002"
        reference = "https://www.cobaltstrike.com/"
        severity = "critical"
    strings:
        // Common Beacon config markers
        $s1 = "MZ" wide ascii
        $s2 = { 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 }
        $s3 = "Beacon" fullword
        $s4 = "kerberos" nocase
        $s5 = "msf" fullword
        $s6 = { 3C 00 00 00 00 00 00 00 ?? ?? ?? ?? ?? ?? ?? ??
                ?? ?? ?? ?? ?? ?? ?? ?? 00 00 00 00 00 00 00 00 }
        // Named pipe patterns
        $s7 = "\\\\.\\pipe\\msf" nocase
        $s8 = "\\\\.\\pipe\\status_" nocase
        // Sleep mask
        $s9 = "Sleep" nocase
        // Malleable C2 profile artifacts
        $s10 = "POST /" nocase
    condition:
        uint16(0) == 0x5A4D and filesize < 1MB and
        (
            // Shellcode in memory
            (uint16(0) == 0x5A4D and $s2)
            or
            // PE with 2+ indicators
            (#s1 > 1 and #s2 > 1)
            or
            // Named pipe / post
            ($s7 or $s8)
        )
}
```

### Emotet Macro
```yara
rule Emotet_Macro_Obfuscated : T1204 {
    meta:
        description = "Detects Emotet dropper macros"
        severity = "high"
        mitre_attack_id = "T1204.002, T1059.001"
    strings:
        // Common VBA obfuscation patterns
        $vba1 = "AutoOpen" nocase
        $vba2 = "Auto_Open" nocase
        $vba3 = "Document_Open" nocase
        $vba4 = "Shell" nocase
        $vba5 = "URLDownloadToFile" nocase
        $vba6 = "WinHttp.WinHttpRequest" nocase
        $vba7 = "Adodb.Stream" nocase
        $vba8 = "XMLHTTP" nocase
        // Emotet-specific obfuscation
        $e1 = "Chr(" nocase
        $e2 = "Asc(" nocase
        $e3 = "Mid(" nocase
        $e4 = "Split(" nocase
        $e5 = "& Chr" nocase
        // Common variable names in Emotet macros
        $v1 = "strDownload" nocase
        $v2 = "sFilePath" nocase
        // String splitting for evasion
        $sp1 = "Replace(" nocase
        // OLE auto macros
        $ole1 = "AutoExec" nocase
    condition:
        magic.type() contains "Composite Document File V2" and
        (
            // Obfuscated macro with download
            ($e1 and $e2 and (#e5 > 5)) or
            // Auto-open macro with shell/download
            (any of ($vba1,$vba2,$vba3,$vba4) and any of ($vba5,$vba6,$vba7,$vba8)) or
            // Extensive character code obfuscation
            (#e1 > 20 and $vba4)
        )
}
```

### Mimikatz
```yara
rule Mimikatz_Win32 : T1003 {
    meta:
        description = "Detects Mimikatz credential dumping tool"
        author = "Defensive Engineering"
        severity = "critical"
        mitre_attack_id = "T1003.001, T1003.002, T1003.005"
        reference = "https://github.com/gentilkiwi/mimikatz"
    strings:
        // Known Mimikatz strings
        $s1 = "mimikatz" nocase
        $s2 = "sekurlsa::logonpasswords" nocase
        $s3 = "kerberos::golden" nocase
        $s4 = "lsadump::sam" nocase
        $s5 = "wdigest" nocase
        $s6 = "\\_kraken\\_" nocase
        $s7 = "kiwi" fullword
        $s8 = "gentilkiwi" nocase
        // Privilege escalation
        $s9 = "token::elevate" nocase
        $s10 = "privilege::debug" nocase
        // Output markers
        $s11 = "NTLM" nocase
        $s12 = "AUTH"

        // Memory-only patterns (injected)
        $h1 = { 48 83 EC 28 48 8B 05 ?? ?? ?? ?? 48 85 C0 74 ?? 48 83 C4 28 48 FF E0 48 83 C4 28 C3 }

    condition:
        // Full PE scan
        (uint16(0) == 0x5A4D and filesize < 3MB and
         pe.is_exe and any of ($s1,$s2,$s3,$s4,$s5,$s7,$s8)) or
        // Memory scan (reflective/injected)
        ($h1 and any of ($s1,$s2,$s3,$s4,$s5,$s6,$s9,$s10,$s11,$s12)) or
        // Aggressive: any 3 module command strings
        3 of ($s2,$s3,$s4,$s9,$s10)
}
```

### Web Shell
```yara
rule Web_Shell_Generic : T1505 {
    meta:
        description = "Generic web shell detection"
        author = "Defensive Engineering"
        severity = "high"
        mitre_attack_id = "T1505.003"
    strings:
        // Common web shell function calls
        $f1 = "eval(" nocase
        $f2 = "assert(" nocase
        $f3 = "system(" nocase
        $f4 = "exec(" nocase
        $f5 = "shell_exec(" nocase
        $f6 = "passthru(" nocase
        $f7 = "popen(" nocase
        $f8 = "proc_open(" nocase
        $f9 = "base64_decode(" nocase
        $f10 = "str_rot13(" nocase
        $f11 = "gzinflate(" nocase
        $f12 = "create_function(" nocase
        // HTTP parameter access
        $p1 = "$_GET" nocase
        $p2 = "$_POST" nocase
        $p3 = "$_REQUEST" nocase
        $p4 = "$_FILES" nocase
        $p5 = "$HTTP_GET_VARS" nocase
        $p6 = "Request.Form" nocase
        $p7 = "Request.QueryString" nocase
        $p8 = "Request.Item" nocase
        // File manipulation
        $w1 = "fwrite(" nocase
        $w2 = "fputs(" nocase
        $w3 = "file_put_contents(" nocase
        $w4 = "move_uploaded_file(" nocase
        // Obfuscation
        $o1 = "chr(" nocase
        $o2 = "ord(" nocase
        $o3 = "hexdec(" nocase
        $o4 = "dechex(" nocase
        // ASP specific
        $a1 = "CreateObject(" nocase
        $a2 = "Server.CreateObject" nocase
        $a3 = "WScript.Shell" nocase
        $a4 = "FileSystemObject" nocase
    condition:
        // PHP webshell
        (
            magic.type() contains "PHP script" or
            magic.type() contains "HTML"
        ) and
        (
            // Dangerous functions + parameter input
            (any of ($f1,$f2,$f3,$f4,$f5,$f6,$f7,$f8) and any of ($p1,$p2,$p3,$p4,$p5,$p6,$p7,$p8)) or
            // Obfuscated code execution
            (any of ($f9,$f10,$f11,$f12) and any of ($p1,$p2)) or
            // Write to web directory
            (any of ($w1,$w2,$w3,$w4) and any of ($p1,$p2,$p3)) or
            // Heavy obfuscation
            (#o1 > 20)
        )
}
```

### Ransomware Common Strings
```yara
rule Ransomware_Generic : T1486 {
    meta:
        description = "Generic ransomware indicators"
        severity = "critical"
        mitre_attack_id = "T1486"
    strings:
        // Extension lists
        $e1 = ".encrypted"
        $e2 = ".locked"
        $e3 = ".crypted"
        $e4 = ".crypto"
        $e5 = ".ransom"
        $e6 = ".pay"
        // Ransom notes
        $n1 = "README" nocase
        $n2 = "HOW_TO_DECRYPT" nocase
        $n3 = "YOUR_FILES" nocase
        $n4 = "bitcoin" nocase
        $n5 = "monero" nocase
        $n6 = "decrypt" nocase
        $n7 = "ransom" nocase
        $n8 = "payment" nocase
        $n9 = "wallet" nocase
        // Encryption API
        $c1 = "CryptEncrypt"
        $c2 = "CryptDecrypt"
        $c3 = "CryptAcquireContext"
        $c4 = "CryptGenKey"
        $c5 = "CryptDeriveKey"
        $c6 = "BCryptEncrypt"
        // Shadow copy deletion
        $v1 = "vssadmin" nocase
        $v2 = "wmic" nocase
        $v3 = "shadowcopy" nocase
        $v4 = "delete shadows" nocase
        // Known ransomware mutexes
        $m1 = "Global\\MsWinZonesCacheCounterMutexA"   // common
        $m2 = "Global\\WininetStartupMutex"             // common
        // Persistence
        $p1 = "RunOnce" nocase
        $p2 = "CurrentVersion\\Run" nocase
    condition:
        uint16(0) == 0x5A4D and filesize < 5MB and
        (
            // Encryption APIs + ransom note behavior
            (any of ($c1,$c2,$c3,$c4,$c5,$c6) and any of ($n1,$n2,$n3,$n4,$n5)) or
            // Shadow copy deletion + any ransom string
            (any of ($v1,$v2,$v3,$v4) and any of ($n6,$n7,$n8,$n9)) or
            // File extension listing in binary + crypto
            (#e* > 3 and any of ($c1,$c2,$c3,$c4,$c5,$c6))
        )
}
```

### Process Injection Indicators
```yara
rule Process_Injection : T1055 {
    meta:
        description = "Detects process injection APIs in PE"
        severity = "high"
        mitre_attack_id = "T1055.001, T1055.002, T1055.012"
    strings:
        // Classic injection
        $api1 = "OpenProcess"
        $api2 = "VirtualAllocEx"
        $api3 = "WriteProcessMemory"
        $api4 = "CreateRemoteThread"
        $api5 = "NtCreateThreadEx"
        $api6 = "QueueUserAPC"
        // Process hollowing
        $api7 = "ZwUnmapViewOfSection"
        $api8 = "SetThreadContext"
        $api9 = "ResumeThread"
        // Reflective DLL
        $api10 = "LoadLibraryA"
        $api11 = "GetProcAddress"
        // Process enumeration
        $api12 = "CreateToolhelp32Snapshot"
        $api13 = "Process32First"
        $api14 = "Process32Next"
        $api15 = "NtGetNextProcess"
        // Token manipulation
        $api16 = "OpenProcessToken"
        $api17 = "DuplicateTokenEx"
        $api18 = "ImpersonateLoggedOnUser"
    condition:
        pe.is_pe and
        (
            // Classic injection trio
            (pe.imports("kernel32.dll", "VirtualAllocEx") or
             pe.imports("kernel32.dll", "VirtualAlloc")) and
            pe.imports("kernel32.dll", "WriteProcessMemory") and
            pe.imports("kernel32.dll", "CreateRemoteThread") and
            // Not a debugger tool
            not pe.imports("kernel32.dll", "WaitForDebugEvent")
        ) or
        (
            // Process hollowing
            pe.imports("ntdll.dll", "ZwUnmapViewOfSection") and
            pe.imports("kernel32.dll", "CreateProcessA")
        ) or
        (
            // Any 4 process enumeration + injection APIs
            pe.imports("kernel32.dll", "CreateToolhelp32Snapshot") and
            pe.imports("kernel32.dll", "VirtualAllocEx") and
            pe.imports("kernel32.dll", "WriteProcessMemory")
        ) or
        // Thread hijacking (QueueUserAPC)
        (pe.imports("kernel32.dll", "QueueUserAPC") and
         pe.imports("kernel32.dll", "OpenThread"))
}
```

### DLL Sideloading
```yara
rule DLL_Sideloading : T1574 {
    meta:
        description = "Detects DLL sideloading patterns"
        severity = "medium"
        mitre_attack_id = "T1574.001, T1574.002"
    strings:
        // Common sideloaded DLL names
        $n1 = "version.dll" nocase
        $n2 = "winrnr.dll" nocase
        $n3 = "wlbsctrl.dll" nocase
        $n4 = "nwsapagent.dll" nocase
        $n5 = "UXTheme.dll" nocase
        $n6 = "apphelp.dll" nocase
        $n7 = "dbghelp.dll" nocase
        $n8 = "mscories.dll" nocase
        $n9 = "Setupapi.dll" nocase
        $n10 = "activeds.dll" nocase
        $n11 = "shimeng.dll" nocase
        // Known sideloading exports
        $e1 = "Ordinal" nocase
        $e2 = "DllMain"
        // Spy on original export names
        $o1 = "SvchostPushServiceGlobals" nocase
        $o2 = "ServiceMain" nocase
    condition:
        pe.is_dll and
        (
            // Not a Microsoft-signed DLL
            not pe.version_info["CompanyName"] contains "Microsoft" and
            // Sideloaded name match
            any of ($n*) and
            // Has at least some exports
            pe.number_of_exports > 0 and
            // Suspicious characteristics
            (pe.imports("kernel32.dll", "WinExec") or
             pe.imports("kernel32.dll", "ShellExecuteA") or
             pe.imports("wininet.dll") or
             pe.imports("urlmon.dll"))
        ) or
        // Mimics a known Microsoft DLL export
        (pe.is_dll and pe.exports("SvchostPushServiceGlobals") and
         not pe.version_info["CompanyName"] contains "Microsoft")
}
```

### Supply Chain Attack — SolarWinds Style
```yara
rule SupplyChain_SolarWinds : T1195 {
    meta:
        description = "Detects indicators from SolarWinds-style supply chain compromise"
        severity = "critical"
        mitre_attack_id = "T1195.001, T1195.002"
        reference = "https://www.cisa.gov/supply-chain-compromise"
    strings:
        // Obfuscated backdoor strings (Sunburst style)
        $s1 = "background" nocase
        $s2 = "orion" nocase
        $s3 = "admintool" nocase
        $s4 = "burn" nocase
        $s5 = "Inventory" nocase
        $s6 = "App_Data" nocase
        // Obfuscated C2 via DNS/FQDN
        $d1 = ".api." nocase
        $d2 = ".app." nocase
        // API patterns
        $a1 = "HttpWebRequest" nocase
        $a2 = "ServicePointManager" nocase
        $a3 = "ServerCertificateValidationCallback" nocase
        // Sleeper / time-based evasion
        $t1 = "Thread.Sleep" nocase
        $t2 = "DateTime.UtcNow" nocase
        // Obfuscated config
        $c1 = "CompressedConfig" nocase
        $c2 = "CompressedInventory" nocase
    condition:
        (dotnet.is_dotnet or pe.is_pe) and
        (
            // Orion-related + suspicious API usage
            (any of ($s2,$s3,$s5) and
             #a1 > 0 and
             $t1 and
             $t2) or
            // Obfuscated configuration
            ($c1 and $c2) or
            // Hard-coded domain patterns with compression
            ($d1 and any of ($c1,$c2))
        )
}
```

---

## YARA 4.x Features

| Feature | Description | Example |
|---|---|---|
| **Module index access** | `pe.sections[0]` syntax | `pe.sections[0].name` |
| **String length** | `!var` operator | `!s1 > 10` |
| **String module** | `import "string"` | `string.replacement("old","new")` |
| **Numeric loops** | `for i in (0..100)` | Iterate over ranges |
| **Hex alternation** | `{ (41|42) 43 }` | Byte choices in hex |
| **Anonymous strings** | Condition literals | `$ at entrypoint` |
| **Multi-module** | Multiple `import` | PE + math + hash |
| **Faster Aho-Corasick** | Optimized engine | ~2x faster scanning |
| **`contains` operator** | Substring | `$a contains "sub"` |
| **`starts/endswith`** | String matching | `$a startswith "MZ"` |
| **`iequals`** | Case-insensitive equality | `$a iequals "malware"` |
| **`defined`** | String existence | `defined($a)` |
| **Improved error messages** | Better debugging | Line numbers and context |
| **Max string size** | Extended | Up to 4KB text strings |

---

## Common Pitfalls

| Pitfall | Explanation | Fix |
|---|---|---|
| Overly broad strings | `http://` matches everything | Combine with context (imports, size) |
| No size limits | Scans huge files, OOM | `filesize < 10MB` |
| `nocase` on wide strings | Case and encoding don't mix | Use `ascii nocase` or `wide` separate |
| Open-ended jumps | `{00 [100000-] FF}` — huge backtracking | Set reasonable bounds `[0-1000]` |
| Trusting `entrypoint` in memory | EP is file-relative; memory may differ | Use `pe.is_pe` guard or check both |
| Over-reliance on hashes | One variant change breaks rule | Use generic patterns + hash as belt |
| No false-positive testing | Deploy → infinite alerts | Always test on benign corpus |
| Too many regex strings | Regex is 10-100x slower than hex | Prefer hex with wildcards/alternation |
| Forgetting `pe.is_pe` guard | Non-PE files crash PE module | Always gate: `pe.is_pe and ...` |
| `global` rules that are too restrictive | Skip valid files | Make globals broad (size, type) |
| Using `$` in hex strings | `$` is only for text strings | Use `$` for text, `{ }` for hex |
| Case sensitivity in hex | Hex is always literal | No `nocase` in hex; use regex/text |
| Negative lookahead in regex | Not supported | Use `not` in condition |
| Rule naming collisions | Two rules same name | Use prefixes/namespaces |

---

## References & Further Reading

- **Official YARA docs:** https://yara.readthedocs.io/
- **YARA-Rules project:** https://github.com/YARA-Rules/rules
- **YARA Forge:** https://yaraify.abuse.ch/
- **Valhalla (Nextron):** https://valhalla.nextron-systems.com/
- **InQuest YARA:** https://github.com/InQuest/yara-rules
- **Malpedia YARA:** https://malpedia.caad.fkie.fraunhofer.de/
- **NCSC YARA:** https://github.com/ncscuk/dfir-yara-rules
- **Elastic YARA:** https://github.com/elastic/protections-artifacts
- **Neo23x0's signature-base:** https://github.com/Neo23x0/signature-base
- **CISA YARA:** https://github.com/cisagov/ymir (YARA management)
- **Volatility YARA plugin:** Volatility 3 `yarascan.YaraScan`
- **YARA vs. Sigma:** https://www.nextron-systems.com/2024/01/15/sigma-vs-yara/
- **YARA Performance Guide:** https://yara.readthedocs.io/en/stable/writingrules.html#performance-notes

---

## YARA Engine Architecture

### Internal Compilation Pipeline

```
Source (.yar files)
        │
        ▼
  Lexer ──→ Token stream (keywords, identifiers, strings, hex)
        │
        ▼
  Parser ──→ Abstract Syntax Tree (AST) — rules, sections, expressions
        │
        ▼
  Compiler ──→ IR (intermediate representation)
        │
        ├──→ Aho-Corasick Automaton Builder
        │       └── All text strings from ALL rules compiled into single DFA
        │           (deterministic finite automaton — trie with failure links)
        │
        ├──→ Regex Compiler (internal NFA/DFA per regex pattern)
        │
        ├──→ Hex Pattern Compiler (byte-level automaton with jumps)
        │
        └──→ Module Preprocessors (PE, ELF, etc. — run at scan time)
                    │
                    ▼
            Compiled Rules Object (binary blob in memory or .yarc file)
```

### Scanning Flow

```
Input File / Memory
        │
        ▼
  1. Global rule pre-filter  ─── false → SKIP file entirely
        │
        ▼
  2. Module parsing (if any rule imports PE/ELF/etc.)
        │
        ▼
  3. Aho-Corasick automaton scan  →  produces list of string matches
        │                            (string_id, offset, length)
        │
        ▼
  4. For each rule that has matched strings:
        ├── Evaluate `condition` expression (short-circuit)
        ├── Access module data (pe.sections, math.entropy, etc.)
        └── If condition true → MATCH (emit rule name + tags + offsets)
```

### Aho-Corasick Deep Dive

- All text strings across all rules are combined into a **single automaton**
- Complexity: O(n + m + z) where n = input length, m = total pattern length, z = total matches
- The automaton is **deterministic** — no backtracking, one pass over the data
- Adding strings doesn't slow scanning (amortized O(1) per character)
- But: strings must be unique — duplicate strings are de-duplicated
- **Wide strings**: YARA stores both ASCII and wide versions in the automaton
- **XOR strings**: YARA generates 256 versions at compile time (one per XOR key)
- **Nocase strings**: YARA generates case-normalized versions

### YARA Binary Compilation (.yarc)

```bash
# Compile rules to binary form
yarac rule.yar compiled.yarc

# Scan with compiled rules
yara -C compiled.yarc target.exe
```

**Benefits of `.yarc`**:
- Faster load times (no re-parsing)
- Obfuscation of rule logic (harder to reverse)
- Smaller distribution size
- Consistent behavior across versions
- Can distribute to endpoints without source rules

---

## Complete YARA Syntax Specification (Informal Grammar)

```
ruleset       = { rule | import_statement }
import_statement = "import" STRING
rule          = [ "private" ] "rule" IDENTIFIER [ ":" TAG_LIST ]
                "{" [ meta_section ] [ strings_section ] condition_section "}"
meta_section  = "meta:" { META_KEY "=" meta_value }
meta_value    = STRING | INTEGER | BOOLEAN
strings_section = "strings:" { string_declaration }
string_declaration = "$" IDENTIFIER [ "(" INTEGER ")" ] "=" string_definition
string_definition = text_string | hex_string | regex_string
text_string   = STRING [ string_modifiers ]
string_modifiers = modifier { modifier }
modifier      = "nocase" | "ascii" | "wide" | "fullword" | xor_modifier
xor_modifier  = "xor" [ "(" XOR_RANGE ")" ]
XOR_RANGE     = INTEGER "-" INTEGER
hex_string    = "{" hex_sequence "}"
hex_sequence  = { hex_token }
hex_token     = BYTE | WILDCARD | JUMP | ALTERNATION
WILDCARD      = "??"
JUMP          = "[" INTEGER [ "-" [ INTEGER ] ] "]"
ALTERNATION   = "(" BYTE { "|" BYTE } ")"
regex_string  = "/" regex_pattern "/" [ regex_flags ]
regex_flags   = { "i" | "s" }

condition_section = "condition:" expression
expression    = BOOLEAN_LITERAL
              | INTEGER_LITERAL
              | STRING_LITERAL
              | IDENTIFIER
              | string_ref
              | "(" expression ")"
              | expression AND expression
              | expression OR expression
              | NOT expression
              | expression OP expression        // + - * / % & | ^ << >> == != < > <= >=
              | of_expression
              | for_expression
              | function_call
              | module_access
              | "filesize"
              | "entrypoint"

string_ref    = "$" IDENTIFIER [ "(" INTEGER ")" ]
              | "#" IDENTIFIER
              | "@" IDENTIFIER [ "[" INTEGER "]" ]
              | "!" IDENTIFIER

of_expression = [ INTEGER ] "of" string_set
              | "any" "of" string_set
              | "all" "of" string_set
string_set    = "them" | "(" string_ref_list ")"

for_expression = "for" quantifier IDENTIFIER "in" "(" range ")" ":" "(" expression ")"
               | "for" quantifier "of" string_set ":" "(" expression ")"
quantifier    = "any" | "all" | INTEGER

function_call = IDENTIFIER "(" [ argument_list ] ")"
module_access = IDENTIFIER "." member { "." member }
```

### Reserved Keywords

```
all, and, any, ascii, at, condition, console, contains, defined,
else, endswith, entrypoint, false, filesize, for, fullword, global,
icontains, iequals, import, in, include, int8, int16, int32,
int8be, int16be, int32be, int64be, matches, meta, nocase, not,
of, or, private, rule, startswith, strings, them, true, uint8,
uint16, uint32, uint64, uint8be, uint16be, uint32be, uint64be,
wide, xor
```

---

## Python `yara-python` — Full API Reference

### Installation
```bash
pip install yara-python
# Verify
python -c "import yara; print(yara.__version__)"
```

### Compiling Rules

```python
import yara

# From file
rules = yara.compile(filepath="malware.yar")

# From string
rules = yara.compile(source="""
rule Test {
    condition:
        true
}
""")

# From filepath with namespaces
rules = yara.compile(filepaths={
    'namespace1': '/path/to/rules1.yar',
    'namespace2': '/path/to/rules2.yar',
})

# From external variables
rules = yara.compile(
    filepath="rule.yar",
    externals={
        "MAX_SIZE": 1024 * 1024,
        "ENVIRONMENT": "production"
    }
)

# Compile to binary .yarc
rules.save("compiled.yarc")

# Load compiled rules
rules = yara.load("compiled.yarc")
```

### Scanning API

```python
# Scan a file
result = rules.match(filepath="/path/to/sample.exe")

# Scan a memory buffer
with open("sample.exe", "rb") as f:
    data = f.read()
result = rules.match(data=data)

# Scan with timeout
result = rules.match(data=data, timeout=30)  # seconds

# Scan process (Linux: /proc/pid/mem)
result = rules.match(pid=1234)

# Scan with callbacks
def callback(data):
    rule_name = data['rule']
    if rule_name == "Interesting_Rule":
        print(f"Match: {rule_name}")
        return yara.CALLBACK_CONTINUE  # or CALLBACK_ABORT
    return yara.CALLBACK_CONTINUE

result = rules.match(filepath="sample.exe", callback=callback)

# Scan with fast mode (skip condition evaluation for non-matching rules)
result = rules.match(filepath="sample.exe", fast=True)

# Scan with match tags filter
result = rules.match(filepath="sample.exe", tags=["T1055", "T1003"])
```

### Match Result Objects

```python
for match in result:
    # Rule-level
    print(match.rule)           # Rule name
    print(match.namespace)      # Namespace
    print(match.tags)           # List of tags
    print(match.meta)           # Dict of meta fields

    # String-level
    for s in match.strings:
        print(s.identifier)     # e.g., "$s1"
        print(s.instances)      # List of Match instances
        for inst in s.instances:
            print(inst.offset)  # Offset in data
            print(inst.matched_data)  # Bytes that matched (YARA 4.x)
            print(inst.length)  # Length of match

# Boolean match
if rules.match(filepath="clean.exe"):
    print("Malicious!")
else:
    print("Clean")
```

### Advanced Python Patterns

```python
# Concurrent scanning
import concurrent.futures
import yara
import os

rules = yara.compile(filepath="rules.yar")

def scan_file(filepath):
    try:
        matches = rules.match(filepath=filepath, timeout=30)
        return filepath, matches
    except yara.Error as e:
        return filepath, []

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for root, _, files in os.walk("/path/to/scan"):
        for f in files:
            fp = os.path.join(root, f)
            futures.append(executor.submit(scan_file, fp))

    for future in concurrent.futures.as_completed(futures):
        filepath, matches = future.result()
        if matches:
            print(f"[!] {filepath}: {[m.rule for m in matches]}")

# YARA as a generator (streaming large files)
def yara_scan_stream(rules, filepath, chunk_size=64*1024):
    with open(filepath, "rb") as f:
        data = f.read(chunk_size)
        offset = 0
        while data:
            matches = rules.match(data=data)
            if matches:
                yield offset, matches
            offset += len(data)
            data = f.read(chunk_size)

# Integration with MISP API
def yara_from_misp(misp_url, misp_key, event_id):
    import requests
    headers = {"Authorization": misp_key, "Accept": "application/json"}
    resp = requests.get(f"{misp_url}/events/{event_id}", headers=headers)
    event = resp.json()
    yara_rules = []
    for attr in event["Event"]["Attribute"]:
        if attr["type"] == "yara":
            yara_rules.append(attr["value"])
    combined = "\n".join(yara_rules)
    return yara.compile(source=combined)
```

### yara-python Error Handling

```python
try:
    rules = yara.compile(filepath="rules.yar")
except yara.SyntaxError as e:
    print(f"Syntax error in rules: {e}")
except yara.Error as e:
    print(f"General YARA error: {e}")

# Runtime errors
try:
    result = rules.match(filepath="huge_file.bin", timeout=5)
except yara.TimeoutError:
    print("Scan timed out")
except yara.Error as e:
    print(f"Scan error: {e}")
```

---

## Rule Management at Scale

### Namespace Strategy

```bash
# Scan with namespace isolation
yara -e -s namespace1::rules.yar namespace2::rules2.yar target.exe
```

```yara
// In rules.yar — namespace prefix is appended as identifier
// namespace "malware_family_x"
rule MalwareX_Detect : TXXXX {
    ...
}

// Python namespace usage
rules = yara.compile(filepaths={
    'malware': '/etc/yara/rules/malware.yar',
    'exploit': '/etc/yara/rules/exploit.yar',
    'tool': '/etc/yara/rules/tools.yar',
})

for match in rules.match(filepath="sample.exe"):
    print(f"[{match.namespace}] {match.rule}")
```

### Recommended Directory Layout

```
/etc/yara/
├── rules/
│   ├── malware/
│   │   ├── c2_frameworks.yar       # Cobalt Strike, Metasploit, Empire
│   │   ├── ransomware.yar          # LockBit, BlackCat, REvil, Conti
│   │   ├── loaders.yar             # Emotet, Qakbot, IcedID, Bumblebee
│   │   ├── stealers.yar            # RedLine, Vidar, Raccoon, AgentTesla
│   │   ├── backdoors.yar           # PlugX, ShadowPad, Gh0stRAT
│   │   ├── worms.yar               # Stuxnet-style, self-replicating
│   │   └── apt.yar                 # APT-specific (Lazarus, APT29, etc.)
│   ├── exploit/
│   │   ├── cve_exploits.yar        # CVE-specific patterns
│   │   ├── web_shells.yar          # PHP/JSP/ASP webshells
│   │   └── office_exploits.yar     # Zero-day document exploits
│   ├── tool/
│   │   ├── hacktools.yar           # Mimikatz, BloodHound, CrackMapExec
│   │   ├── scanners.yar            # Nmap, Nessus, Nuclei
│   │   └── c2_clients.yar          # C2 client binaries
│   ├── phishing/
│   │   ├── macro_docs.yar          # Malicious Office macros
│   │   ├── pdf_malware.yar         # Malicious PDFs
│   │   └── html_phishing.yar       # Phishing pages
│   ├── indicator/
│   │   ├── ip_patterns.yar         # Hardcoded IPs
│   │   ├── domain_patterns.yar     # DGA, domain generation
│   │   └── crypto_wallets.yar      # BTC/Monero addresses
│   └── generic/
│       ├── packed.yar              # UPX, Themida, VMProtect
│       ├── anti_debug.yar          # Anti-debug tricks
│       └── obfuscated.yar          # Generic obfuscation
├── compiled/                        # .yarc files for deployment
├── tests/
│   ├── positives/                   # Known malware samples
│   ├── negatives/                   # Benign corpus
│   └── test_runner.py              # Automated test harness
├── scripts/
│   ├── fp_checker.py               # False positive scanner
│   ├── rule_benchmark.py           # Performance profiler
│   └── feed_importer.py            # Import from MISP/ThreatFeeds
├── config/
│   ├── exclusions.lst              # FP exclusions
│   └── scan_profiles.json          # Profile definitions
└── CHANGELOG.md                    # Rule version history
```

### Rule Versioning with Git

```yara
// In meta section:
rule Example : T1003 {
    meta:
        author = "BlueTeam"
        created = "2026-01-15"
        modified = "2026-06-27"
        version = "2.1"
        changelog = "v2.1: Added FP exclusion for WinDBG; v2.0: Broadened to 64-bit"
        status = "active"            // active | testing | retired | draft
        false_positives = "Known FPs: SysInternals procdump.exe v3.0+"
        tlp = "amber"
        confidence = 85              // 0-100 confidence score
}
```

**Git workflow:**
```bash
# Feature branch per rule/change
git checkout -b rule/detect-new-malware
# Edit rule
git add rules/malware/c2_frameworks.yar
git commit -m "feat: add detection for NewMalware variant X"

# PR → code review → merge to staging
git checkout staging && git merge rule/detect-new-malware

# Test on staging → merge to production
git checkout production && git merge staging

# Tag releases
git tag -a v2026.06.27 -m "Rule set update 2026-06-27"
```

---

## YARA as a Service (REST API)

### Flask Implementation

```python
from flask import Flask, request, jsonify
import yara
import os
import tempfile
import base64

app = Flask(__name__)

# Load rules on startup
RULES = yara.compile(filepaths={
    'malware': '/etc/yara/rules/malware.yar',
    'tool': '/etc/yara/rules/tool.yar',
})

@app.route('/v1/scan', methods=['POST'])
def scan_file():
    data = request.get_json()

    if 'file' in data:
        # Base64-encoded file content
        raw = base64.b64decode(data['file'])
        try:
            matches = RULES.match(data=raw, timeout=30)
        except yara.TimeoutError:
            return jsonify({'error': 'timeout'}), 408
    elif 'path' in data:
        # Server-local file path
        try:
            matches = RULES.match(filepath=data['path'], timeout=30)
        except yara.TimeoutError:
            return jsonify({'error': 'timeout'}), 408
    else:
        return jsonify({'error': 'provide file or path'}), 400

    results = []
    for m in matches:
        strings_detail = []
        for s in m.strings:
            for inst in s.instances:
                strings_detail.append({
                    'identifier': s.identifier,
                    'offset': inst.offset,
                    'data': inst.matched_data.hex() if hasattr(inst, 'matched_data') else ''
                })
        results.append({
            'rule': m.rule,
            'namespace': m.namespace,
            'tags': list(m.tags),
            'meta': dict(m.meta),
            'strings': strings_detail
        })

    return jsonify({'matches': results, 'count': len(results)})

@app.route('/v1/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'rules_loaded': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### FastAPI Async Implementation

```python
from fastapi import FastAPI, HTTPException, UploadFile, File
import yara
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
import io

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)
RULES = yara.compile(filepath="/etc/yara/rules/all.yar")

@app.post("/api/v2/scan")
async def scan_upload(file: UploadFile = File(...), timeout: Optional[int] = 30):
    content = await file.read()
    loop = asyncio.get_event_loop()

    try:
        matches = await loop.run_in_executor(
            executor,
            lambda: RULES.match(data=content, timeout=timeout)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "filename": file.filename,
        "size": len(content),
        "matches": [{
            "rule": m.rule,
            "namespace": m.namespace,
            "tags": list(m.tags),
            "meta": {k: str(v) for k, v in m.meta.items()}
        } for m in matches],
        "matched": len(matches) > 0
    }
```

### Go Implementation (using `yara` C bindings via cgo)

```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "encoding/json"
    "github.com/hillu/go-yara/v4"
)

var rules *yara.Rules

func scanHandler(w http.ResponseWriter, r *http.Request) {
    body, _ := ioutil.ReadAll(r.Body)
    var results []yara.MatchRule
    err := rules.ScanMem(body, 0, 30, &results)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    json.NewEncoder(w).Encode(results)
}

func main() {
    compiler, _ := yara.NewCompiler()
    compiler.AddFile("rules.yar", nil)
    rules, _ = compiler.GetRules()
    http.HandleFunc("/scan", scanHandler)
    http.ListenAndServe(":8080", nil)
}
```

---

## YARA for Memory Analysis — Process Memory Scanning

### Linux Process Memory

```yara
// Detect /dev/mem access in process memory
rule DevMemAccess : T1003 {
    strings:
        $s1 = "/dev/mem" fullword
        $s2 = "/dev/kmem" fullword
        $s3 = "mmap" fullword
        $s4 = "phys" fullword
    condition:
        uint32(0) == 0x464C457F and  // ELF magic
        $s1 or $s2
}

// Detect LD_PRELOAD injection
rule LDPRELOAD_Injection : T1055 {
    strings:
        $s1 = "LD_PRELOAD" fullword
        $s2 = "LD_LIBRARY_PATH" fullword
        $s3 = "dlopen" fullword
    condition:
        $s1 and ($s2 or $s3)
}

// Detect shellcode markers
rule Linux_Execve_Shellcode {
    strings:
        // xor eax, eax; push eax; push 0x68732f2f; push 0x6e69622f;
        // mov ebx, esp; xor ecx, ecx; xor edx, edx; mov al, 0xb; int 0x80
        $linux_execve = {
            31 C0 50 68 2F 2F 73 68 68 2F 62 69 6E 89 E3
            31 C9 31 D2 B0 0B CD 80
        }
        // 64-bit execve
        $linux_execve64 = {
            48 31 FF 48 31 F6 48 31 D2 48 BB 2F 62 69 6E 2F
            73 68 00 53 54 5F B0 3B 0F 05
        }
    condition:
        any of them
}
```

### Windows Process Memory

```bash
# Scan all running processes
for pid in $(tasklist /FO CSV | tail -n +2 | cut -d',' -f2 | tr -d '"'); do
    yara rules.yar $pid
done
```

```yara
// Reflective DLL injection in memory
rule ReflectiveDLL : T1055 {
    strings:
        $mz = "MZ"
        $ref1 = "ReflectiveLoader" nocase
        $ref2 = { 55 8B EC 83 EC 10 53 56 57 64 A1 30 00 00 00 }
        // Syscall stub pattern
        $syscall = { 0F 05 C3 }
    condition:
        // PE header in process memory (not at file start)
        $mz and ($ref1 or $ref2 or $syscall) and not pe.is_pe
}

// APC injection
rule APCInjection : T1055.004 {
    strings:
        $n1 = "NtTestAlert"
        $n2 = "QueueUserAPC"
        $h1 = { 48 83 EC 28 48 8B ?? ?? ?? ?? ?? 48 85 ?? 74 ??
                48 83 C4 28 48 FF E0 48 83 C4 28 C3 }
        // NtQueueApcThread syscall
        $h2 = { 4C 8B D1 B8 ?? ?? ?? ?? F6 04 25 ?? ?? ?? ?? ?? 75 02 0F 05 C3 }
    condition:
        ($n1 or $n2) and ($h1 or $h2)
}

// Process hollowing
rule ProcessHollowing : T1055.012 {
    strings:
        $s1 = "ZwUnmapViewOfSection" fullword
        $s2 = "SetThreadContext" fullword
        $s3 = "ResumeThread" fullword
        $s4 = "NtCreateProcessEx" fullword
        $h1 = { 48 8B C4 48 89 58 08 48 89 68 10 48 89 70 18
                48 89 78 20 41 54 41 56 41 57 48 83 EC 40 }
    condition:
        // Hollowing API combination
        (pe.imports("ntdll.dll", "ZwUnmapViewOfSection") or
         $s1) and
        (pe.imports("kernel32.dll", "CreateProcessA") or
         pe.imports("kernel32.dll", "ResumeThread")) and
        not pe.version_info["OriginalFileName"] contains "svchost"
}
```

### Windows Kernel Memory (Volatility + YARA)

```bash
# Scan kernel modules
volatility -f memory.dmp windows.modules | awk '{print $1}' > modules.txt
volatility -f memory.dmp yarascan.YaraScan --yara-rules=kernel_rules.yar

# Scan specific processes
volatility -f memory.dmp yarascan.YaraScan --pid 1234,5678 --yara-rules=malware.yar
```

```yara
// Kernel driver artifacts
rule KernelDriverSuspicious : T1014 {
    strings:
        $s1 = "\\\\.\\" nocase
        $s2 = "\\Device\\" nocase
        $s3 = "IRP_MJ_DEVICE_CONTROL" nocase
        $s4 = "DriverEntry" fullword
        $s5 = "MmMapIoSpace" fullword
        $s6 = "ZwOpenProcess" fullword
        // Rootkit markers
        $r1 = "SSDT" nocase
        $r2 = "inline hook" nocase
        $r3 = "DKOM" nocase
    condition:
        elf.is_elf and  // kernel modules on Linux
        (($s3 and $s4 and $s5) or  // device control + MM access
         (any of ($r1,$r2,$r3)))
}
```

---

## YARA for Linux/macOS Forensics

### macOS Mach-O Scanning

```yara
import "macho"

rule MachO_Ransomware : T1486 {
    condition:
        macho.is_macho and
        macho.filetype == macho.MH_EXECUTE and
        // Common macOS ransomware file access
        macho.cmd("LC_LOAD_DYLIB", "/usr/lib/libz.1.dylib") and
        macho.cmd("LC_LOAD_DYLIB", "/System/Library/Frameworks/Foundation.framework")
}

rule XPC_Service_Abuse : T1055 {
    strings:
        $s1 = "XPC" nocase
        $s2 = "xpc_connection_create" nocase
        $s3 = "xpc_connection_send_message" nocase
        // Authorization hooks
        $s4 = "AuthorizationCreate" nocase
        $s5 = "SMJobBless" nocase
    condition:
        macho.is_macho and
        any of ($s1,$s2,$s3) and
        ($s4 or $s5)
}

// macOS persistence
rule LaunchAgents_Persistence : T1543 {
    strings:
        $p1 = ".plist" fullword
        $p2 = "Label" fullword
        $p3 = "ProgramArguments" fullword
        $p4 = "KeepAlive" fullword
        $p5 = "RunAtLoad" fullword
        $p6 = "LaunchDaemons" fullword
        $p7 = "LaunchAgents" fullword
    condition:
        $p2 and $p3 and ($p4 or $p5) and
        ($p6 or $p7)
}
```

### Linux Log Tampering Detection

```yara
// Detect log wiper / anti-forensics tools
rule LogWiper : T1070 {
    strings:
        $s1 = "/var/log" fullword
        $s2 = "shred" fullword
        $s3 = "wipe" fullword
        $s4 = "logrotate" fullword
        $s5 = "rm -rf" fullword
        $s6 = "journalctl" fullword
        $s7 = "history -c" fullword
        $s8 = "bash_history" fullword
        $s9 = ".bash_history" fullword
        $s10 = "auth.log" fullword
        $s11 = "syslog" fullword
        $s12 = "secure" fullword
    condition:
        elf.is_elf and
        // Log path references + destructive commands
        ($s1 or $s10 or $s11 or $s12) and
        ($s2 or $s3 or $s5 or $s7 or $s8 or $s9) and
        not pe.version_info["CompanyName"] contains "Red Hat"
}

// Detect timestomping tools
rule Timestomping : T1070.006 {
    strings:
        $s1 = "touch" fullword
        $s2 = "utimes" fullword
        $s3 = "futimens" fullword
        $s4 = "utimensat" fullword
        $s5 = "-t" fullword  // touch -t flag
        $s6 = "stat" fullword
        $s7 = "--date=" fullword    // touch --date=
        $s8 = "-d" fullword         // touch -d
    condition:
        elf.is_elf and
        ($s2 or $s3 or $s4) and
        ($s5 or $s7 or $s8)
}
```

---

## YARA for Container Security

### Docker Image Scanning

```yaml
# docker-compose.yml for YARA scanner service
version: '3.8'
services:
  yara-scanner:
    build: .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./rules:/rules
      - ./compiled:/compiled
    environment:
      - RULES_PATH=/rules/all.yar
      - LOG_LEVEL=INFO
```

```yara
// Detect secrets in container images
rule Container_Secret_Leak {
    meta:
        description = "Detects secrets/hardcoded credentials in container images"
        severity = "high"
    strings:
        $s1 = "-----BEGIN RSA PRIVATE KEY-----" fullword
        $s2 = "-----BEGIN OPENSSH PRIVATE KEY-----" fullword
        $s3 = "-----BEGIN DSA PRIVATE KEY-----" fullword
        $s4 = "-----BEGIN EC PRIVATE KEY-----" fullword
        $s5 = "AKIA" ascii fullword            // AWS Access Key prefix
        $s6 = "sk_live_" ascii fullword         // Stripe live key
        $s7 = "pk_live_" ascii fullword         // Stripe live publishable
        $s8 = "ghp_" ascii fullword             // GitHub personal access token
        $s9 = "gho_" ascii fullword             // GitHub OAuth
        $s10 = "xoxb-" ascii fullword           // Slack bot token
        $s11 = "xoxp-" ascii fullword           // Slack user token
        $s12 = "ghs_" ascii fullword            // GitHub app token
        $s13 = "ghr_" ascii fullword            // GitHub refresh token
        $s14 = "token=" nocase
        $s15 = "password=" nocase
        $s16 = "secret=" nocase
        $s17 = "api_key" nocase
        $s18 = "api_secret" nocase
    condition:
        any of ($s1,$s2,$s3,$s4) or  // Private keys
        any of ($s5,$s6,$s7,$s8,$s9,$s10,$s11,$s12,$s13) or  // API tokens
        2 of ($s14,$s15,$s16,$s17,$s18)  // Credential patterns
}

// Detect shell in container
rule Container_Shell_Injection {
    strings:
        $s1 = "/bin/sh" fullword
        $s2 = "/bin/bash" fullword
        $s3 = "bash -c" fullword
        $s4 = "sh -c" fullword
        $s5 = "/dev/tcp/" fullword
        $s6 = "exec /bin" fullword
        $s7 = "wget" fullword
        $s8 = "curl" fullword
        $s9 = "nc -e" fullword
        $s10 = "bash -i" fullword
    condition:
        // Shell command execution outside expected patterns
        any of ($s1,$s2,$s3,$s4) and
        (any of ($s5,$s6,$s7,$s8,$s9,$s10))
}

// Detect vulnerable packages in container layers
rule Known_Malicious_Package {
    meta:
        description = "Detects known malicious npm/PyPI packages in images"
        severity = "high"
    strings:
        // Known malicious npm packages
        $n1 = "eslint-scope" fullword   // (compromised version)
        $n2 = "flatmap-stream" fullword
        $n3 = "event-stream" fullword
        // Known malicious PyPI packages
        $p1 = "colourama" fullword
        $p2 = "urllib" fullword
        $p3 = "keylogger" fullword
    condition:
        any of ($n1,$n2,$n3,$p1,$p2,$p3)
}
```

---

## YARA for OT/ICS

```yara
// Detect ICS/SCADA-specific malware
rule ICS_Modbus_Scanner {
    strings:
        // Modbus function codes
        $m1 = { 00 01 00 00 00 06 01 01 }   // Read Coils
        $m2 = { 00 01 00 00 00 06 01 03 }   // Read Holding Registers
        $m3 = { 00 01 00 00 00 06 01 05 }   // Write Single Coil
        $m4 = { 00 01 00 00 00 06 01 0F }   // Write Multiple Coils
        $m5 = { 00 01 00 00 00 06 01 10 }   // Write Multiple Registers
        // S7Comm (Siemens)
        $s7 = { 32 03 00 00 45 72 03 00 }   // S7Comm header
        // CIP (Rockwell)
        $cip = { 65 00 04 00 00 00 00 00 }
        // DNP3
        $dnp3 = { 05 64 05 }                 // DNP3 start + length
        // IEC 104
        $iec = { 68 04 07 00 00 00 }
    condition:
        // Modbus scanning tool
        any of ($m1,$m2,$m3,$m4,$m5) or
        // Any ICS protocol embedded
        any of ($s7,$cip,$dnp3,$iec)
}

rule PLC_Backdoor : T838 {
    meta:
        description = "Detects PLC backdoor/rootkit code"
        severity = "critical"
    strings:
        // Common PLC malware strings
        $s1 = "TRITON" nocase
        $s2 = "TRISIS" nocase
        $s3 = "INCONTROLLER" nocase
        $s4 = "PIPEDREAM" nocase
        // CODESYS exploitation
        $c1 = "CoDeSys" nocase
        $c2 = "CmpApp" nocase
        $c3 = "CmpSrv" nocase
        // Industrial protocol manipulation
        $p1 = "Modbus" nocase
        $p2 = "Profibus" nocase
        $p3 = "Profinet" nocase
        $p4 = "EtherNet/IP" nocase
    condition:
        any of ($s1,$s2,$s3,$s4) or
        ($c1 and ($c2 or $c3) and any of ($p1,$p2,$p3,$p4))
}

rule Firmware_Backdoor {
    strings:
        // U-Boot modification markers
        $u1 = "U-Boot" fullword
        $u2 = { 27 05 19 56 }                   // Common firmware magic
        // Backdoor shell in embedded firmware
        $b1 = "telnetd" fullword
        $b2 = "-l /bin/sh" fullword
        $b3 = "dropbear" fullword
        $b4 = "busybox" fullword
        $b5 = "nc -l -p" fullword
        $b6 = "reverse shell" nocase
        // Firmware modification
        $f1 = "firmware" fullword
        $f2 = "squashfs" fullword
        $f3 = "jffs2" fullword
        $f4 = "yaffs2" fullword
        $f5 = "ubifs" fullword
    condition:
        $u1 and (any of ($b1,$b2,$b3,$b4,$b5,$b6)) or
        ($u2 and any of ($b1,$b2,$b3,$b4,$b5,$b6)) or
        (any of ($f1,$f2,$f3,$f4,$f5) and any of ($b1,$b2,$b3,$b4,$b5,$b6))
}
```

---

## YARA for Mobile (Android/iOS)

### Android APK Analysis

```yara
import "andro"  // Hypothetical — Android parsing via dex module or external tool

rule Android_Trojan : T1404 {
    strings:
        // Overlay attack permissions
        $p1 = "SYSTEM_ALERT_WINDOW" fullword
        $p2 = "BIND_ACCESSIBILITY_SERVICE" fullword
        $p3 = "REQUEST_INSTALL_PACKAGES" fullword
        $p4 = "RECEIVE_SMS" fullword
        $p5 = "READ_SMS" fullword
        $p6 = "INTERNET" fullword
        // Known malicious packages
        $pkg1 = "com.google.update" nocase
        $pkg2 = "com.android.system.update" nocase
        $pkg3 = "com.security.service" nocase
        // SMS interception
        $sm1 = "onReceive" nocase
        $sm2 = "android.provider.Telephony.SMS_RECEIVED" nocase
        $sm3 = "abortBroadcast" nocase
        // Accessibility abuse
        $a1 = "onAccessibilityEvent" nocase
        $a2 = "AccessibilityService" nocase
        $a3 = "TYPE_WINDOW_STATE_CHANGED" nocase
        $a4 = "getRootInActiveWindow" nocase
        // C2 communication
        $c1 = "http://" nocase
        $c2 = "https://" nocase
        $c3 = "encrypt" nocase
        $c4 = "base64" nocase
        // DexClassLoader (dynamic loading)
        $d1 = "DexClassLoader" nocase
        $d2 = "PathClassLoader" nocase
    condition:
        // Overlay Trojan: overlay + SMS + accessibility
        (all of ($p1,$p2,$p4,$p5) and 2 of ($a1,$a2,$a3,$a4)) or
        // SMS stealer
        (all of ($p4,$p5,$p6) and $sm1 and $sm2 and $sm3 and $c1) or
        // Dynamic loader with suspicious package name
        ($d1 and any of ($pkg1,$pkg2,$pkg3)) or
        // Accessibility abuse + C2
        (3 of ($a1,$a2,$a3,$a4) and $c1 and $c3 and $c4)
}

// Detection of Flutter/Dart-based malware
rule Flutter_Malware {
    strings:
        // Flutter reverse shell pattern
        $f1 = "dart:io" fullword
        $f2 = "Socket" fullword
        $f3 = "RawSocket" fullword
        $f4 = "HttpClient" fullword
        $f5 = "Process.run" fullword
        $f6 = "Process.start" fullword
        $f7 = "Directory" fullword
        $f8 = "FileSystemEntity" fullword
    condition:
        // Flutter app doing suspicious things
        ($f1 and $f2 and $f4 and $f5) or
        ($f5 and $f6 and $f7 and $f8)
}
```

### iOS IPA Analysis

```yara
rule iOS_Jailbreak_Detection_Bypass {
    strings:
        // Jailbreak detection bypass
        $j1 = "MobileSubstrate" nocase
        $j2 = "CydiaSubstrate" nocase
        $j3 = "SubstrateLoader" nocase
        $j4 = "dlopen" fullword
        $j5 = "dlsym" fullword
        // Integrity check bypass
        $c1 = "FairPlay" fullword
        $c2 = "encrypted" nocase
        $c3 = "SC_Info" fullword
        // Private API usage
        $p1 = "UIApplication" nocase
        $p2 = "private" nocase
        $p3 = "UIPasteboard" fullword
        $p4 = "UIDevice" fullword
    condition:
        2 of ($j1,$j2,$j3,$j4,$j5) or
        ($c1 and $c3) or
        ($p1 and $p2 and $p4)
}
```

---

## Sigma → YARA Translation Guide

Sigma is a generic signature format for SIEM logs. While YARA matches binary content, Sigma maps to log events. You can translate detection logic:

| Sigma Field | YARA Equivalent | Notes |
|---|---|---|
| `logsource.category` | `magic.type()` | File type matching |
| `detection.selection` | `$string` | Pattern definitions |
| `detection.condition` | `condition` | Boolean logic |
| `falsepositives` | `meta.false_positives` | Documentation |
| `level` | `meta.severity` | Critical/high/medium/low |
| `tags` | rule tags | MITRE ATT&CK mapping |
| `EventID` | Module-specific | e.g., `pe.is_pe` for Image/Process |
| `CommandLine` | Text string | Match on CLI args |

**Sigma to YARA mapping example:**

```yaml
# Sigma rule (Windows PowerShell execution)
title: PowerShell Execution
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
    condition: selection
falsepositives:
    - Administrative scripts
level: low
tags:
    - attack.execution
    - attack.t1059.001
```

```yara
// YARA equivalent (for binaries that invoke PowerShell)
rule Sigma_PowerShell_Execution : T1059 {
    meta:
        description = "Binary that may execute PowerShell (Sigma translation)"
        severity = "low"
        false_positives = "Administrative scripts"
        sigma_rule = "posh_execution"
    strings:
        $s1 = "powershell.exe" nocase fullword
        $s2 = "powershell" nocase fullword
        $s3 = "-Command" nocase fullword
        $s4 = "-EncodedCommand" nocase fullword
        $s5 = "-ExecutionPolicy" nocase fullword
        $s6 = "PowerShell" fullword
    condition:
        (pe.is_pe or elf.is_elf) and (
            ($s1 and ($s3 or $s4 or $s5)) or
            ($s2 and $s6 and ($s3 or $s4 or $s5))
        )
}
```

---

## OpenIOC → YARA Translation

OpenIOC format (Mandiant) to YARA:

```python
import xml.etree.ElementTree as ET

def openioc_to_yara(ioc_xml):
    root = ET.fromstring(ioc_xml)
    ns = {'ioc': 'http://schemas.mandiant.com/2010/ioc'}
    rule_name = root.find('.//ioc:short_description', ns).text if root.find('.//ioc:short_description', ns) is not None else "IOC_Rule"
    description = root.find('.//ioc:description', ns).text if root.find('.//ioc:description', ns) is not None else ""

    yara_strings = []
    yara_conditions = []
    for idx, indicator in enumerate(root.findall('.//ioc:IndicatorItem', ns)):
        content = indicator.find('ioc:Content', ns).text if indicator.find('ioc:Content', ns) is not None else ""
        if content:
            s_id = f"$ioc{idx}"
            yara_strings.append(f'\t{s_id} = "{content}" nocase')
            yara_conditions.append(s_id)

    if not yara_conditions:
        return None

    condition = " or ".join(yara_conditions)
    yara_rule = f"""
rule {rule_name} {{
    meta:
        description = "{description}"
        source = "OpenIOC"
    strings:
{chr(10).join(yara_strings)}
    condition:
        {condition}
}}
"""
    return yara_rule
```

---

## YARA for Network PCAP Analysis

### Extracting HTTP Payloads to YARA

```bash
# Extract HTTP response bodies → pipe to YARA
tshark -r capture.pcap -Y "http.response" -T fields -e http.file_data \
  | yara rules.yar -

# Extract DNS queries
tshark -r capture.pcap -Y "dns" -T fields -e dns.qry.name \
  | yara rules.yar -

# Extract TLS SNI
tshark -r capture.pcap -Y "tls.handshake.type == 1" -T fields -e tls.handshake.extensions_server_name \
  | yara rules.yar -

# Full packet reassembly + YARA
tshark -r capture.pcap -z follow,tcp,ascii,0 | yara rules.yar -
```

### Network-Specific YARA Rules

```yara
// DGA Detection (Domain Generation Algorithm)
rule DGA_Detection : T1568 {
    strings:
        // Long subdomain with high entropy
        $re_dga = /[a-z]{12,25}\.(com|net|org|info|top|xyz|club|work)\b/ nocase
        // Numeric subdomain
        $re_numdga = /[0-9]{8,}\.(com|net|org|info|top)/ nocase
        // Consonant-heavy domain (no vowels)
        $re_novowel = /[bcdfghjklmnpqrstvwxyz]{10,}\.[a-z]{2,3}\b/
        // Hyphen-heavy
        $re_hyphen = /[a-z]+-[a-z]+-[a-z]+-[a-z]+\.[a-z]{2,3}\b/
    condition:
        any of ($re*)
}

// C2 Beacon Detection
rule C2_Beacon_HTTP : T1071 {
    strings:
        $ua1 = "Mozilla/4.0 (compatible; MSIE 6.0)" nocase
        $ua2 = "Mozilla/4.0 (compatible; MSIE 7.0)" nocase
        $ua3 = "Mozilla/5.0 (Windows NT 6.1)" nocase
        $uri1 = "/admin/" nocase
        $uri2 = "/modules/" nocase
        $uri3 = "/includes/" nocase
        $uri4 = "/images/" nocase
        $uri5 = "/css/" nocase
        $uri6 = "/js/" nocase
        $c1 = "Cookie:" nocase
        $c2 = "Content-Type: application/x-www-form-urlencoded" nocase
        // Common beacon intervals in User-Agent
        $s1 = "sleep=" nocase
        $s2 = "jitter=" nocase
    condition:
        // Old IE UA on modern OS + suspicious URI path
        (any of ($ua1,$ua2,$ua3) and any of ($uri1,$uri2,$uri3,$uri4,$uri5,$uri6)) or
        // Beacon config leak
        ($s1 or $s2)
}

// Malicious TLS certificate fingerprint
rule Malicious_TLS_Cert : T1573 {
    strings:
        // Self-signed markers
        $s1 = "Self-signed" nocase
        $s2 = "localhost" nocase
        $s3 = "Mozilla Fake CA" nocase
        // Known bad issuer strings
        $i1 = "Let's Encrypt" fullword  // (abused by malware too)
        // Suspicious CN
        $cn1 = "CloudFlare" nocase
        $cn2 = "Google Internet Authority" nocase
        // Certificate in binary (DER format inside PE)
        $cert = { 30 82 ?? ?? 30 82 ?? ?? A0 03 02 01 02 }
    condition:
        $cert and ($s1 or $s2 or $s3) or
        ($cn1 and $i1) or $cn2
}
```

---

## YARA for Registry Hive Scanning

```bash
# Extract registry data from hive files
python -c "
import yara
rules = yara.compile(source='''
rule Registry_Persistence {
    strings:
        \$run = \"CurrentVersion\\\\Run\" nocase
        \$runonce = \"CurrentVersion\\\\RunOnce\" nocase
    condition:
        \$run or \$runonce
}')

with open('NTUSER.DAT', 'rb') as f:
    result = rules.match(data=f.read())
    for m in result:
        print(m.rule)
"
```

```yara
// Registry hive scanning rules
rule Registry_Autorun_Persistence : T1547 {
    strings:
        $k1 = "CurrentVersion\\Run" nocase
        $k2 = "CurrentVersion\\RunOnce" nocase
        $k3 = "CurrentVersion\\RunOnceEx" nocase
        $k4 = "CurrentVersion\\RunServices" nocase
        $k5 = "CurrentVersion\\RunServicesOnce" nocase
        $k6 = "CurrentVersion\\Policies\\Explorer\\Run" nocase
        // Startup folder
        $k7 = "Microsoft\\Windows\\Start Menu\\Programs\\Startup" nocase
        // Service
        $k8 = "CurrentVersion\\Services" nocase
        // Winlogon
        $k9 = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon" nocase
        $k10 = "Userinit" nocase
        $k11 = "Shell" nocase
        // Boot execute
        $k12 = "CurrentVersion\\Explorer\\SharedTaskScheduler" nocase
        // Browser helper objects
        $k13 = "CurrentVersion\\Explorer\\Browser Helper Objects" nocase
        // AppInit_DLLs
        $k14 = "CurrentVersion\\Windows\\AppInit_DLLs" nocase
        // Image hijack
        $k15 = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options" nocase
        // Screensaver
        $k16 = "Control Panel\\Desktop\\SCRNSAVE.EXE" nocase
        // Policy
        $k17 = "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" nocase
    condition:
        any of ($k1,$k2,$k3,$k4,$k5,$k6,$k7) or
        (($k9 or $k8) and any of ($k10,$k11)) or
        any of ($k12,$k13,$k14,$k15,$k16,$k17)
}

rule Registry_Execution_Evasion : T1112 {
    strings:
        // Disable UAC
        $u1 = "EnableLUA" fullword
        $u2 = "ConsentPromptBehaviorAdmin" fullword
        // Disable Defender
        $d1 = "DisableAntiSpyware" fullword
        $d2 = "DisableRealtimeMonitoring" fullword
        $d3 = "PUAProtection" fullword
        // Disable firewall
        $f1 = "EnableFirewall" fullword
        // Disable notifications
        $n1 = "EnableNotifications" fullword
        // Safe mode
        $s1 = "SafeBoot" fullword
    condition:
        ($u1 and $u2) or
        any of ($d1,$d2,$d3) or
        $f1 or ($s1 and $u1)
}
```

---

## YARA for EVTX (Windows Event Log) Scanning

```bash
# Extract EVTX content → YARA
python -c "
import yara
import xml.etree.ElementTree as ET
import struct

def parse_evtx_chunks(filepath):
    '''Simple EVTX chunk parser'''
    chunks = []
    with open(filepath, 'rb') as f:
        data = f.read()
        # EVTX chunks start at 0x200 aligned
        for off in range(0x200, len(data), 0x10000):
            if data[off:off+4] == b'ElfChnk\x00':
                chunks.append(data[off:off+0x10000])
    return b' '.join(chunks)

rules = yara.compile(source='''
rule EventLog_Suspicious_Commands {
    strings:
        \$s1 = \"powershell -enc\" nocase
        \$s2 = \"-Hidden\" fullword
        \$s3 = \"Invoke-Expression\" nocase
        \$s4 = \"IEX\" fullword
    condition:
        any of them
}')

data = parse_evtx_chunks('Security.evtx')
result = rules.match(data=data)
"
```

```yara
// Event log content patterns
rule EventLog_PowerShell_Abuse : T1059 {
    strings:
        $e1 = "-EncodedCommand" nocase
        $e2 = "-ExecutionPolicy Bypass" nocase
        $e3 = "-WindowStyle Hidden" nocase
        $e4 = "-NoProfile" nocase
        $e5 = "IEX(" nocase
        $e6 = "Invoke-Expression" nocase
        $e7 = "Invoke-Mimikatz" nocase
        $e8 = "Invoke-ReflectivePEInjection" nocase
        $e9 = "DownloadString(" nocase
        $e10 = "Start-BitsTransfer" nocase
        $e11 = "Net.WebClient" nocase
        $e12 = "System.Net.Sockets.TCPClient" nocase
    condition:
        // Obfuscated PowerShell execution
        $e1 or
        // Bypass + hidden execution
        ($e2 and $e3) or
        // Malicious invocation
        any of ($e5,$e6,$e7,$e8,$e9,$e10,$e11,$e12)
}

rule EventLog_Service_Creation : T1543 {
    strings:
        $s1 = "Service Control Manager" fullword
        $s2 = "Start = " nocase
        $s3 = "binPath = " nocase
        $s4 = "sc create" nocase
        $s5 = "Auto Start" nocase
        $s6 = "LocalSystem" nocase
        $s7 = "DisplayName = " nocase
    condition:
        ($s1 or $s4) and ($s2 or $s3 or $s5 or $s6 or $s7)
}

rule EventLog_Scheduled_Task : T1053 {
    strings:
        $s1 = "schtasks" nocase
        $s2 = "/CREATE" fullword
        $s3 = "/SC ONLOGON" nocase
        $s4 = "/SC DAILY" nocase
        $s5 = "/SC ONIDLE" nocase
        $s6 = "/TN" fullword
        $s7 = "/TR" fullword
        $s8 = "/RU SYSTEM" nocase
    condition:
        $s1 and $s2 and (any of ($s3,$s4,$s5)) and ($s6 or $s7)
}
```

---

## YARA for Anti-Forensics Detection

```yara
// Detect timestamp manipulation
rule Timestomp_Indicators : T1070 {
    strings:
        // SetMace (timestomping tool for Windows)
        $t1 = "SetMace" nocase
        $t2 = "MACE" fullword
        // Change file time APIs
        $t3 = "SetFileTime"
        $t4 = "NtSetInformationFile"
        // Touch for Windows
        $t5 = "touch" fullword
        // Alternate Data Stream
        $ads1 = ":" fullword  // ADS marker in filename
    condition:
        (pe.is_pe and (pe.imports("kernel32.dll", "SetFileTime") or
                       pe.imports("ntdll.dll", "NtSetInformationFile"))) or
        any of ($t1,$t2,$t4,$t5)
}

// Detect log deletion
rule LogDeletion_Tools : T1070 {
    strings:
        // Windows
        $w1 = "wevtutil" nocase
        $w2 = "Clear-EventLog" nocase
        $w3 = "Remove-EventLog" nocase
        $w4 = "del *.log" nocase
        $w5 = "fsutil" nocase
        // Linux
        $l1 = "rm -rf /var/log" nocase
        $l2 = "> /dev/null" nocase
        $l3 = "shred -z" nocase
        $l4 = "wipe -rf" nocase
        $l5 = "logrotate --force" nocase
        // macOS
        $m1 = "sudo rm -rf /var/log" nocase
        $m2 = "aslmanager" nocase
        $m3 = "log erase" nocase
    condition:
        any of ($w1,$w2,$w3,$w4,$w5) or
        any of ($l1,$l2,$l3,$l4,$l5) or
        any of ($m1,$m2,$m3)
}

// Detect VSS (shadow copy) deletion
rule VSS_Deletion : T1490 {
    strings:
        $s1 = "vssadmin delete shadows" nocase
        $s2 = "vssadmin resize shadowstorage" nocase
        $s3 = "wmic shadowcopy delete" nocase
        $s4 = "Get-WmiObject Win32_ShadowCopy" nocase
        $s5 = ".Delete()" fullword
        $s6 = "wbadmin delete catalog" nocase
        $s7 = "bcdedit" nocase
        $s8 = "bootsect" nocase
        // WMIC shadow copy
        $w1 = "shadowcopy" nocase
        $w2 = "VolumeShadowCopy" nocase
    condition:
        any of ($s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8) or
        ($w1 and $w2)
}
```

---

## YARA for PDF Analysis

```yara
rule PDF_Embedded_File : T1204 {
    strings:
        // PDF magic
        $pdf = "%PDF" fullword
        // Embedded file
        $e1 = "/EmbeddedFile" fullword
        $e2 = "/EmbeddedFiles" fullword
        $e3 = "/Type /EmbeddedFile" fullword
        // Launch action
        $l1 = "/Launch" fullword
        $l2 = "/Action" fullword
        // JavaScript
        $j1 = "/JavaScript" fullword
        $j2 = "/JS" fullword
        $j3 = "/OpenAction" fullword
        $j4 = "app.alert" nocase
        $j5 = "app.execCmd" nocase
        // Shell commands in PDF
        $s1 = "cmd.exe" nocase
        $s2 = "powershell" nocase
        $s3 = "wscript" nocase
        $s4 = "cscript" nocase
        // URI
        $u1 = "/URI" fullword
        $u2 = "http://" nocase
        $u3 = "https://" nocase
        // Encoding/obfuscation
        $o1 = "/Filter /FlateDecode" fullword
        $o2 = "/Filter /ASCIIHexDecode" fullword
        $o3 = "/Filter /ASCII85Decode" fullword
        $o4 = "/Filter /RunLengthDecode" fullword
    condition:
        $pdf and
        (
            // Embedded file with executable
            ($e1 or $e2 or $e3) or
            // Launch action
            ($l1 or $l2) or
            // JavaScript with suspicious actions
            (($j1 or $j2 or $j3) and (any of ($s1,$s2,$s3,$s4) or any of ($j4,$j5))) or
            // OpenAction + URI
            ($j3 and ($u1 or $u2 or $u3)) or
            // Multiple filter obfuscation
            (#o* > 2 and ($j1 or $j2 or $j3))
        )
}

rule PDF_Obfuscated_JavaScript {
    strings:
        // Hex-encoded strings
        $hex1 = "\\x" fullword
        // Large string concatenation
        $sc1 = "+" fullword
        // eval with string building
        $e1 = "eval(" nocase
        // unescape
        $u1 = "unescape(" nocase
        // charCode
        $c1 = "String.fromCharCode" nocase
        // long hex strings
        $h1 = /[0-9A-Fa-f]{100,}/
        // document functions
        $d1 = ".submitForm" nocase
        $d2 = ".getURL" nocase
        $d3 = ".mailDoc" nocase
        // Base64 in PDF
        $b1 = /[A-Za-z0-9+/]{50,}={0,2}/
    condition:
        $e1 and ($u1 or $c1 or $h1) and (#sc1 > 50) or
        $e1 and any of ($d1,$d2,$d3) or
        ($e1 and $b1 and $hex1)
}
```

---

## YARA for Office Documents Deep Dive

```yara
// OLE2 / CFB format detection
rule OLE2_Suspicious_Structure {
    strings:
        // OLE2 magic
        $ole = { D0 CF 11 E0 A1 B1 1A E1 }
        // Macro streams
        $m1 = "Macros" fullword
        $m2 = "VBA" fullword
        $m3 = "VBAProject" fullword
        $m4 = "ThisDocument" fullword
        $m5 = "Modules" fullword
        $m6 = "Module1" fullword
        $m7 = "_VBA_PROJECT_CUR" fullword
        $m8 = "PROJECTwm" fullword
        $m9 = "dir" fullword
        // Auto macros
        $a1 = "Auto_Open" nocase
        $a2 = "Auto_Close" nocase
        $a3 = "Auto_Exec" nocase
        $a4 = "AutoOpen" nocase
        $a5 = "AutoClose" nocase
        $a6 = "AutoExec" nocase
        $a7 = "Document_Open" nocase
        $a8 = "Workbook_Open" nocase
        $a9 = "Auto_Activate" nocase
        // OLE objects
        $o1 = "Embedded Object" fullword
        $o2 = "Equation" fullword
        $o3 = "Package" fullword
        // Suspicious VBA keywords
        $v1 = "Declare" nocase  // API declaration
        $v2 = "Lib" nocase
        $v3 = "Private Declare" nocase
        $v4 = "CreateObject" nocase
        $v5 = "WinHttp" nocase
        $v6 = "Shell" nocase
        $v7 = "Exec" nocase
        $v8 = "Run" nocase
    condition:
        $ole and
        (
            // Macro-enabled document
            (any of ($m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9)) or
            // Auto macro with suspicious VBA
            (any of ($a1,$a2,$a3,$a4,$a5,$a6,$a7,$a8,$a9) and
             any of ($v1,$v2,$v3,$v4,$v5,$v6,$v7,$v8)) or
            // Embedded OLE objects
            any of ($o1,$o2,$o3)
        )
}

// DDE attack (Dynamic Data Exchange)
rule Office_DDE_Attack : T1559 {
    strings:
        // DDE field codes
        $d1 = "DDEAUTO" fullword
        $d2 = "DDE" fullword
        // DDE command
        $c1 = "cmd.exe" fullword
        $c2 = "powershell" fullword
        $c3 = "/c " fullword
        $c4 = "/k " fullword
        $c5 = "calc.exe" fullword  // classic test
        // Field codes in OOXML
        $f1 = "<w:fldCode" fullword
        $f2 = "w:instrText" fullword
        // DDE link in OLE
        $l1 = "\\link" fullword
        $l2 = "\\* MERGEFORMAT" fullword
    condition:
        ($d1 or ($d2 and ($c1 or $c2))) or
        ($f1 and ($c1 or $c2 or $c3 or $c4)) or
        ($f2 and any of ($c1,$c2,$c3,$c4,$c5))
}

// Excel 4.0 (XLM) macro
rule Excel_XLM_Macro : T1204 {
    strings:
        $x1 = "\\xl\\macrosheet\\" nocase
        $x2 = "\\xl\\worksheets\\sheet" nocase
        $x3 = "Excel 4.0" fullword
        // XLM function names
        $f1 = "EXEC" fullword
        $f2 = "CALL" fullword
        $f3 = "REGISTER" fullword
        $f4 = "RUN" fullword
        $f5 = "CREATE.OBJECT" fullword
        $f6 = "FOPEN" fullword
        $f7 = "FWRITE" fullword
        $f8 = "FCLOSE" fullword
        // XLM auto-open macros
        $a1 = "Auto_Open" fullword
        $a2 = "Auto_Close" fullword
        // File extensions
        $e1 = ".xlsm" fullword
        $e2 = ".xlsb" fullword
        $e3 = ".xltm" fullword
    condition:
        (magic.type() contains "Excel" or magic.type() contains "Composite") and
        (
            (any of ($x1,$x2,$x3) and any of ($f1,$f2,$f3,$f4,$f5)) or
            (any of ($a1,$a2) and any of ($f1,$f2,$f3,$f4,$f5,$f6,$f7,$f8))
        )
}
```

---

## YARA Obfuscation & Evasion Detection

```yara
// Detect YARA rule evasions
rule Anti_YARA_Techniques {
    meta:
        description = "Detects samples trying to evade YARA pattern matching"
    strings:
        // String splitting evasion
        $s1 = "mal" + "ware"    // Not a real YARA feature, but in binary:
        $s1 = { 6D 61 6C 00 77 61 72 65 }  // "mal\0ware"
        // Null-byte insertion
        $s2 = /m[\\x00]alware/
        // XOR obfuscation of strings
        $s3 = "\\x" fullword
        // Overlapping instructions (disassembly obfuscation)
        $h1 = { EB FF C0 }       // jmp $+1; ret; ... (instruction overlap)
        // Packer markers (attempt to evade string matching)
        $p1 = "UPX0" fullword
        $p2 = "UPX1" fullword
        $p3 = "UPX2" fullword
        $p4 = "UPX!" fullword
        $p5 = "VMP" fullword    // VMProtect
        $p6 = ".themida" fullword
        $p7 = "RSDS" fullword
        // Anti-sandbox
        $a1 = "IsDebuggerPresent"
        $a2 = "CheckRemoteDebuggerPresent"
        $a3 = "NtQueryInformationProcess"
        $a4 = "Sleep" fullword
        $a5 = "GetTickCount" fullword
        $a6 = "rdtsc" fullword
        // String encryption
        $e1 = "XOR" fullword
        $e2 = "RC4" fullword
        $e3 = "AES" fullword
        $e4 = "decrypt" nocase
    condition:
        // Packed binary
        (uint16(0) == 0x5A4D and any of ($p1,$p2,$p3,$p4,$p5,$p6)) or
        // Anti-debug present
        (any of ($a1,$a2,$a3,$a5,$a6) and $a4) or
        // High entropy + obfuscation markers
        (math.entropy(0, filesize) > 7.0 and any of ($e1,$e2,$e3,$e4))
}

// Detect string table obfuscation
rule String_Obfuscation {
    strings:
        // Many short strings with null terminators
        $short = { ?? 00 ?? 00 ?? 00 ?? 00 ?? 00 ?? 00 ?? 00 ?? 00 ?? 00 ?? 00 }
        // Control character sequences (index-based string reconstruction)
        $ctrl = /[\\x01-\\x08\\x0E-\\x1F]{10,}/
        // Stack strings (chars pushed one by one)
        $stack = { 6A ?? 6A ?? 6A ?? 6A ?? 6A ?? 6A ?? }  // push byte; push byte; ...
        // Jump table for obfuscation
        $jt = { FF 24 85 ?? ?? ?? ?? }  // jmp [eax*4+offset]
    condition:
        (#short > 10 and #ctrl > 5) or
        #stack > 5 or
        #jt > 3
}
```

---

## YARA Benchmarking & Profiling

### Rule Performance Measurement

```python
import yara
import time
import os
import statistics

def benchmark_rule(rule_source, test_dir, iterations=5):
    """Benchmark a single rule against a test corpus."""
    compiled = yara.compile(source=f"rule bench {{ strings: $a = \"test\" condition: $a }}\n{rule_source}")
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        for root, _, files in os.walk(test_dir):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    compiled.match(filepath=fp, timeout=10)
                except:
                    pass
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'files_scanned': sum(len(files) for _, _, files in os.walk(test_dir))
    }

# Per-string benchmark
def benchmark_strings(rule_source, data):
    """Test each string individually to find bottlenecks."""
    import re
    strings_found = re.findall(r'(\$\w+)\s*=\s*("[^"]*"|{[^}]*}|/[^/]*/)', rule_source)

    for s_id, s_def in strings_found:
        single_rule = f"""
        rule test {{
            strings:
                {s_id} = {s_def}
            condition:
                {s_id}
        }}
        """
        try:
            compiled = yara.compile(source=single_rule)
            start = time.perf_counter()
            result = compiled.match(data=data)
            elapsed = time.perf_counter() - start
            print(f"{s_id}: {elapsed*1000:.2f}ms {'MATCH' if result else 'no match'}")
        except Exception as e:
            print(f"{s_id}: ERROR - {e}")
```

### YARA Performance Statistics

```bash
# Check YARA version and features
yara --version
yara --help

# Time a full scan
time yara -r rules/ /usr/bin/ > /dev/null

# Profile with perf
perf stat -e cycles,instructions,cache-misses yara -r rules/ /usr/bin/

# Measure compile time
time yara -c rules/all.yar /dev/null  # Compile + scan empty file
```

**Performance characteristics (approximate):**

| Operation | Relative Cost | Notes |
|---|---|---|
| Text string match (Aho-Corasick) | 1x | Base cost, O(n) |
| Hex string match | 2-5x | Per-byte comparison with wildcards |
| Regex match | 10-100x | NFA/DFA backtracking |
| `xor` string | 256x | Brute forces 256 keys |
| `math.entropy(range)` | 5-20x | Scans entire range |
| `hash.md5/file` | 50-100x | Full file read + hash |
| `pe` module parsing | 2-5x | Header parsing only |
| `elf` module parsing | 2-5x | Header parsing only |
| `magic` module | 10-20x | Calls libmagic |
| `dotnet` module | 3-10x | Metadata parsing |
| Filesize check | 0.01x | Stat call only |
| `uint16(0)` check | 0.01x | Single byte read |

---

## YARA in Cloud Environments

### AWS Lambda YARA Scanner

```python
import json
import boto3
import yara
import tempfile
import os

s3 = boto3.client('s3')
RULES = yara.compile(filepath='/opt/yara/rules/all.yar')

def lambda_handler(event, context):
    """Triggered by S3 object creation."""
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download file from S3
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        s3.download_fileobj(bucket, key, tmp)
        tmp_path = tmp.name

    try:
        matches = RULES.match(filepath=tmp_path, timeout=30)
        results = [{
            'rule': m.rule,
            'namespace': m.namespace,
            'tags': list(m.tags),
            'meta': {k: str(v) for k, v in m.meta.items()}
        } for m in matches]

        if matches:
            # Alert to SNS/SQS
            sns = boto3.client('sns')
            sns.publish(
                TopicArn=os.environ['ALERT_TOPIC_ARN'],
                Subject=f"YARA Match: {key}",
                Message=json.dumps({'bucket': bucket, 'key': key, 'matches': results})
            )
            print(f"ALERT: {key} matched {len(matches)} rules")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'file': key,
                'matched': len(matches) > 0,
                'rules_matched': len(matches)
            })
        }
    finally:
        os.unlink(tmp_path)
```

### Azure Function YARA Scanner

```python
import azure.functions as func
import yara
import tempfile
import logging

RULES = yara.compile(filepath='/home/site/wwwroot/rules/all.yar')

def main(req: func.HttpRequest) -> func.HttpResponse:
    file_data = req.get_body()
    if not file_data:
        return func.HttpResponse("No file data", status_code=400)

    matches = RULES.match(data=file_data, timeout=30)

    results = [{
        'rule': m.rule,
        'tags': list(m.tags),
        'meta': m.meta
    } for m in matches]

    logging.info(f"Scanned {len(file_data)} bytes, {len(matches)} matches")

    return func.HttpResponse(
        json.dumps({'matches': results, 'matched': len(matches) > 0}),
        mimetype="application/json"
    )
```

### Kubernetes CronJob for Regular Scanning

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: yara-nightly-scan
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: yara-scanner
            image: yara-scanner:latest
            command:
            - /bin/sh
            - -c
            - |
              yara -r /rules/all.yar /mnt/data > /mnt/results/scan-$(date +%Y%m%d).txt &&
              echo "Scan complete: $(date)"
            volumeMounts:
            - name: rules
              mountPath: /rules
            - name: data
              mountPath: /mnt/data
            - name: results
              mountPath: /mnt/results
            resources:
              limits:
                memory: "512Mi"
                cpu: "500m"
          volumes:
          - name: rules
            configMap:
              name: yara-rules
          - name: data
            hostPath:
              path: /var/lib/docker/volumes
          - name: results
            emptyDir: {}
          restartPolicy: OnFailure
```

---

## YARA Alternative Implementations

| Implementation | Language | Notes |
|---|---|---|
| **Official YARA** | C | Reference implementation, most complete |
| **yara-python** | C/Python | Bindings to official YARA |
| **go-yara** | Go | CGo bindings to official YARA |
| **yara-rust (yara-x)** | Rust | Pure Rust rewrite, sandboxed execution, WASM support |
| **yara-rs** | Rust | Bindings via FFI to libyara |
| **lyara** | LuaJIT | FFI bindings for Lua |
| **yara-java** | Java | JNI bridge to libyara |
| **pyyara** | Python | Alternative pure-Python implementation (limited) |
| **node-yara** | Node.js | N-API bindings |

### yara-x (Rust) — The Future

```rust
// yara-x example (Rust)
use yara_x::Compiler;

fn main() {
    let mut compiler = Compiler::new();
    compiler.add_source(r#"
        rule test {
            meta:
                description = "Test rule"
            strings:
                $a = "malicious"
            condition:
                $a
        }
    "#).unwrap();

    let rules = compiler.build();
    let results = rules.scan(b"this is malicious content");

    for result in results {
        println!("Matched: {}", result.identifier());
    }
}
```

**yara-x advantages:**
- Pure Rust (no C dependency, no FFI)
- Sandboxed rule execution (memory safety)
- WebAssembly compilation support
- Rule isolation (one crash doesn't take down the scanner)
- Stricter parsing (rejects ambiguous rules)
- Better error messages

---

## YARA Event-Driven Architecture (Kafka)

```python
from kafka import KafkaConsumer, KafkaProducer
import yara
import json
import os

consumer = KafkaConsumer(
    'file-uploads',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

RULES = yara.compile(filepath='/etc/yara/all.yar')

for message in consumer:
    event = message.value
    file_path = event.get('path')
    file_data = event.get('data')

    try:
        if file_data:
            data = bytes.fromhex(file_data) if isinstance(file_data, str) else file_data
            matches = RULES.match(data=data, timeout=30)
        elif file_path:
            matches = RULES.match(filepath=file_path, timeout=30)
        else:
            continue

        if matches:
            alert = {
                'type': 'yara_match',
                'source': event.get('source'),
                'timestamp': event.get('timestamp'),
                'file_path': file_path or 'memory',
                'matches': [{
                    'rule': m.rule,
                    'namespace': m.namespace,
                    'tags': list(m.tags)
                } for m in matches]
            }
            producer.send('yara-alerts', value=alert)
            print(f"Alert sent for {file_path}: {len(matches)} matches")

    except Exception as e:
        producer.send('yara-errors', value={
            'error': str(e),
            'event': event
        })
```

---

## YARA with osquery Integration

```sql
-- osquery YARA table (Linux/macOS)
SELECT * FROM yara_scan(
    path := '/usr/bin',
    sigfile := '/etc/yara/rules/all.yar',
    pattern := '%.exe'
);

-- YARA events (realtime file monitoring)
SELECT * FROM yara_events(
    target_path := '/usr/bin',
    category := 'file',
    sigfile := '/etc/yara/rules/all.yar',
    pattern := '%.exe',
    action := 'ATTACH'
);

-- Scan processes in memory
SELECT * FROM yara_scan(
    path := '/proc/self/mem',
    sigfile := '/etc/yara/rules/memory.yar',
    pattern := 'mem'
) WHERE matches != '[]';

-- Join with processes
SELECT p.name, p.pid, y.matches
FROM processes p
JOIN yara_scan(
    path := '/proc/' || cast(p.pid as text) || '/mem',
    sigfile := '/etc/yara/rules/memory.yar',
    pattern := 'mem'
) y;
```

---

## YARA Limits & Hardening

### Configuration for Production

```bash
# Environment variables
export YARA_MAX_STRINGS_PER_RULE=10000
export YARA_MAX_STRING_SIZE=4096
export YARA_MAX_MATCH_DATA=512
export YARA_MAX_PATTERNS=500000

# Safe-mode compilation (disables dangerous features)
yara --fail-on-warnings rules.yar target

# Limit recursion in hex patterns
# (Not directly configurable — avoid open-ended jumps)
```

### Security Considerations

| Threat | Mitigation |
|---|---|
| **Rule file path traversal** | Validate rule paths; don't allow user-supplied rule files |
| **Regex ReDoS** | Avoid catastrophic regex patterns; set timeouts |
| **OOM via huge files** | Always gate with `filesize < MAX` |
| **Infinite condition loops** | Avoid `for any i in (0..filesize)` |
| **Module crash** | Guard module access: `pe.is_pe and pe.sections[N].name == ...` |
| **Rule injection (user input)** | Use compiled `.yarc` files; don't eval user YARA source |
| **Timing side channels** | YARA evaluation is generally constant-time for given input |
| **Resource exhaustion** | Set `timeout` on all scans (Python: `timeout=30`) |

### Safe Defaults for Production Scanning

```yara
// Every production rule should start with these guards
global rule ProductionGuardrails {
    condition:
        filesize < 100 * 1024 * 1024  // 100MB max
}

// Per-rule size gate pattern
rule Safe_Rule {
    condition:
        filesize < 10 * 1024 * 1024 and  // 10MB max for this rule
        ...
}
```

---

## YARA 3.x → 4.x Migration Guide

| 3.x Pattern | 4.x Equivalent | Notes |
|---|---|---|
| `pe.section[0]` | `pe.sections[0]` | Indexed access now requires `sections` |
| Manual entrypoint | `entrypoint` built-in | Still works, but built-in is preferred |
| No string length | `!` operator | New in 4.x |
| No `defined()` | `defined($a)` | Check if string exists in rule |
| No `contains` | `$a contains "sub"` | String method |
| No `startswith` | `$a startswith "prefix"` | String method |
| No `endswith` | `$a endswith "suffix"` | String method |
| No `iequals` | `$a iequals "value"` | Case-insensitive equality |
| No anonymous strings | `"literal"` in condition | Simplify one-off rules |
| No hex alternation | `{ (41|42) 43 }` | Byte alternation |
| No numeric `for` loops | `for i in (0..10)` | Range iteration |
| No `!` in hex | `{ 8D ?? A0 }` | Use `??` instead of `!` |
| No `string` module | `import "string"` | New module |

---

## Complete YARA Built-in Function Reference

### Integer Read Functions

```
uint8(offset)      → unsigned 8-bit integer (little-endian)
uint16(offset)     → unsigned 16-bit integer (little-endian)
uint32(offset)     → unsigned 32-bit integer (little-endian)
uint64(offset)     → unsigned 64-bit integer (little-endian)
uint8be(offset)    → unsigned 8-bit integer (big-endian)
uint16be(offset)   → unsigned 16-bit integer (big-endian)
uint32be(offset)   → unsigned 32-bit integer (big-endian)
uint64be(offset)   → unsigned 64-bit integer (big-endian)
int8(offset)       → signed 8-bit integer (little-endian)
int16(offset)      → signed 16-bit integer (little-endian)
int32(offset)      → signed 32-bit integer (little-endian)
int8be(offset)     → signed 8-bit integer (big-endian)
int16be(offset)    → signed 16-bit integer (big-endian)
int32be(offset)    → signed 32-bit integer (big-endian)
int64be(offset)    → signed 64-bit integer (big-endian)
```

### String Reference Operators

```
$string_name      → True if string matches at least once
#string_name      → Integer count of matches
@string_name      → Integer offset of first match
@string_name[i]   → Integer offset of i-th match (1-indexed)
!string_name      → Integer length of matched data (YARA 4.x+)
```

### String Methods (YARA 4.x+)

```
$s contains "substring"           → True if substring present
$s icontains "substring"          → Case-insensitive contains
$s startswith "prefix"            → True if starts with prefix
$s endswith "suffix"              → True if ends with suffix
$s iequals "value"                → True if case-insensitive equal
$s matches /regex/                → True if matches regular expression
defined($s)                       → True if string $s is defined in rule
```

### Math Module Functions

```
math.entropy(offset, length)      → Float entropy (0.0–8.0)
math.mean(offset, length)         → Float arithmetic mean
math.standard_deviation(offset, length) → Float std dev
math.max(offset, length)          → Float maximum value
math.min(offset, length)          → Float minimum value
math.mode(offset, length)         → Float most common value
math.median(offset, length)       → Float median value
math.count_in_range(offset, length, low, high) → Int count
math.percentage(offset, length, byte) → Float percentage
math.variance(offset, length)     → Float variance
```

### Hash Module Functions

```
hash.md5(offset, length)          → String MD5 hex digest
hash.sha1(offset, length)         → String SHA1 hex digest
hash.sha256(offset, length)       → String SHA256 hex digest
hash.crc32(offset, length)        → String CRC32 hex digest
```

### PE Module Functions

```
pe.is_pe                          → Boolean
pe.is_dll                         → Boolean
pe.is_driver                      → Boolean
pe.is_exe                         → Boolean
pe.is_console                     → Boolean
pe.is_gui                         → Boolean
pe.machine                        → Integer (e.g., pe.MACHINE_I386)
pe.entry_point                    → Integer RVA
pe.image_base                     → Integer
pe.number_of_sections             → Integer
pe.number_of_resources            → Integer
pe.number_of_imports              → Integer
pe.number_of_exports              → Integer
pe.sections[N].name              → String
pe.sections[N].virtual_size      → Integer
pe.sections[N].virtual_address   → Integer
pe.sections[N].raw_size          → Integer
pe.sections[N].raw_data_offset   → Integer
pe.sections[N].entropy           → Float
pe.sections[N].characteristics   → Integer
pe.imports(dll_name, [api])      → Boolean
pe.exports(api_name)             → Boolean
pe.imphash()                      → String
pe.exphash()                      → String
pe.suspicious_imports()           → Boolean
pe.rich_signature.raw_data       → String (bytes)
pe.rich_signature.clear_data     → String (bytes)
pe.rich_signature.length         → Integer
pe.rich_signature.tools          → Array of (id, build, count)
pe.version_info[key]             → String (e.g., pe.version_info["CompanyName"])
pe.overlay.offset                → Integer
pe.overlay.size                  → Integer
pe.overlay.data                  → String (bytes)
pe.linker_version.major          → Integer
pe.linker_version.minor          → Integer
pe.major_subsystem_version       → Integer
pe.minor_subsystem_version       → Integer
pe.characteristics               → Integer
pe.dll_characteristics           → Integer
pe.timestamp                     → Integer (UNIX timestamp in seconds)
pe.subsystem                     → Integer
pe.resources[N].name            → String
pe.resources[N].offset          → Integer
pe.resources[N].length          → Integer
pe.resources[N].type            → String
pe.resources[N].language        → Integer
pe.resources[N].entropy         → Float
```

### PE Machine Constants

```
pe.MACHINE_I386        → 0x014C  (x86)
pe.MACHINE_AMD64       → 0x8664  (x64)
pe.MACHINE_IA64        → 0x0200  (Itanium)
pe.MACHINE_ARM         → 0x01C0  (ARM Thumb)
pe.MACHINE_ARM64       → 0xAA64  (ARM64)
pe.MACHINE_THUMB       → 0x01C2
pe.MACHINE_MIPS16      → 0x0266
pe.MACHINE_POWERPC     → 0x01F0
```

### PE Characteristics Constants

```
pe.IMAGE_FILE_DLL                    → 0x2000
pe.IMAGE_FILE_SYSTEM                 → 0x1000
pe.IMAGE_FILE_EXECUTABLE_IMAGE       → 0x0002
pe.IMAGE_FILE_LARGE_ADDRESS_AWARE    → 0x0020
pe.IMAGE_FILE_32BIT_MACHINE          → 0x0100
pe.IMAGE_FILE_RELOCS_STRIPPED        → 0x0001
pe.IMAGE_FILE_LINE_NUMS_STRIPPED     → 0x0004
pe.IMAGE_FILE_LOCAL_SYMS_STRIPPED    → 0x0008
pe.IMAGE_FILE_DEBUG_STRIPPED         → 0x0200
```

### PE DLL Characteristics

```
pe.IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE    → 0x0040
pe.IMAGE_DLLCHARACTERISTICS_NX_COMPAT       → 0x0100
pe.IMAGE_DLLCHARACTERISTICS_NO_SEH          → 0x0400
pe.IMAGE_DLLCHARACTERISTICS_APPCONTAINER    → 0x1000
pe.IMAGE_DLLCHARACTERISTICS_GUARD_CF        → 0x4000
```

### PE Subsystem Constants

```
pe.IMAGE_SUBSYSTEM_NATIVE                  → 1
pe.IMAGE_SUBSYSTEM_WINDOWS_GUI             → 2
pe.IMAGE_SUBSYSTEM_WINDOWS_CUI             → 3
pe.IMAGE_SUBSYSTEM_OS2_CUI                 → 5
pe.IMAGE_SUBSYSTEM_WINDOWS_CE_GUI          → 9
pe.IMAGE_SUBSYSTEM_EFI_APPLICATION         → 10
pe.IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER → 11
pe.IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER      → 12
pe.IMAGE_SUBSYSTEM_EFI_ROM                 → 13
pe.IMAGE_SUBSYSTEM_XBOX                    → 14
```

### ELF Module Reference

```
elf.is_elf                          → Boolean
elf.type                           → Integer
elf.machine                        → Integer
elf.entry_point                    → Integer
elf.number_of_sections             → Integer
elf.number_of_segments             → Integer
elf.sections[N].name              → String
elf.sections[N].type              → Integer
elf.sections[N].offset            → Integer
elf.sections[N].size              → Integer
elf.sections[N].entropy           → Float
elf.sections[N].address           → Integer
elf.segments[N].type              → Integer
elf.segments[N].offset            → Integer
elf.segments[N].virtual_address   → Integer
elf.segments[N].file_size         → Integer
elf.segments[N].memory_size       → Integer
elf.imports(library, function)    → Boolean
elf.dynamic.entries_count         → Integer
elf.dynamic[N].tag                → Integer
elf.dynamic[N].value              → Integer
elf.symbols(name)                 → Boolean
```

### ELF Type Constants

```
elf.ET_NONE    → 0
elf.ET_REL     → 1  (Relocatable)
elf.ET_EXEC    → 2  (Executable)
elf.ET_DYN     → 3  (Shared object)
elf.ET_CORE    → 4  (Core file)
```

### ELF Machine Constants

```
elf.EM_X86_64      → 62
elf.EM_386         → 3
elf.EM_ARM         → 40
elf.EM_AARCH64     → 183
elf.EM_MIPS        → 8
elf.EM_PPC         → 20
elf.EM_PPC64       → 21
elf.EM_RISCV       → 243
```

### ELF Segment Type Constants

```
elf.PT_NULL        → 0
elf.PT_LOAD        → 1
elf.PT_DYNAMIC     → 2
elf.PT_INTERP      → 3
elf.PT_NOTE        → 4
elf.PT_SHLIB       → 5
elf.PT_PHDR        → 6
elf.PT_TLS         → 7
```

### MachO Module Reference

```
macho.is_macho                  → Boolean
macho.filetype                 → Integer
macho.number_of_load_commands  → Integer
macho.cmd(name, [value])       → Boolean
```

### DotNET Module Reference

```
dotnet.is_dotnet                      → Boolean
dotnet.version.major                  → Integer
dotnet.version.minor                  → Integer
dotnet.assembly_name                  → String
dotnet.assembly_version               → String
dotnet.assembly_ref_count             → Integer
dotnet.strong_name_signature          → Boolean
dotnet.entry_point_rva                → Integer
dotnet.number_of_assemblies           → Integer
dotnet.number_of_typedefs             → Integer
dotnet.number_of_methods              → Integer
dotnet.number_of_resources            → Integer
dotnet.number_of_user_strings         → Integer
dotnet.guid                           → String (GUID from #GUID stream)
dotnet.streams["#Strings"].size      → Integer
dotnet.streams["#US"].size           → Integer
dotnet.streams["#GUID"].size         → Integer
dotnet.streams["#Blob"].size         → Integer
dotnet.user_strings                   → Array of strings
dotnet.assembly_refs                  → Array of assembly names
dotnet.typedefs                       → Array of type definitions
dotnet.methods                        → Array of method definitions
dotnet.resources                       → Array of resources
```

---

## YARA Rule Scoring & Confidence System

```yara
rule Score_Example : T1003 {
    meta:
        severity = "high"
        confidence = 85      // 0-100 scale
        false_positive_risk = "low"
        mitre_attack_id = "T1003.001"
    strings:
        // High-weight — specific to this malware
        $high1 = "sekurlsa::logonpasswords" fullword
        $high2 = { 48 83 EC 28 48 8B 05 ?? ?? ?? ?? 48 85 C0 74 ?? }

        // Medium-weight — commonly associated
        $med1 = "wdigest" nocase
        $med2 = "kerberos::golden" nocase

        // Low-weight — contextual
        $low1 = "AUTH" fullword
        $low2 = "NTLM" fullword

    condition:
        // Scoring:
        // High = +50 each, Medium = +25 each, Low = +10 each
        // Threshold = 60
        (
            (for any of ($high1,$high2) : ($) * 50) +
            (for any of ($med1,$med2) : ($) * 25) +
            (for any of ($low1,$low2) : ($) * 10)
        ) >= 60
}
```

**Scoring table for meta:**

```yara
meta:
    // Confidence levels
    confidence = 95    // Confirmed family-specific signature
    confidence = 80    // Strong indicator, some FP risk
    confidence = 60    // Moderate indicator, use in combination
    confidence = 40    // Weak indicator, high FP risk, hunting only
    confidence = 20    // Experimental, not for production

    // Severity
    severity = "critical"    // Ransomware, C2, credential theft
    severity = "high"        // Malware dropper, backdoor
    severity = "medium"      // Recon, lateral movement
    severity = "low"         // PUA, hacktool
    severity = "info"        // Informational, not malicious
```

---

## YARA Rule Templates for Rapid Development

### Template 1: PE-Based Malware Detection

```yara
rule PE_Malware_Template : T1204 {
    meta:
        author = ""
        description = ""
        date = ""
        mitre_attack_id = ""
        false_positives = ""
        confidence = 80

    strings:
        // API calls
        $api1 = ""
        $api2 = ""

        // Static strings
        $s1 = "" fullword
        $s2 = "" nocase

        // Hex pattern (unique code sequence)
        $h1 = { }

        // Regex pattern (e.g., URL, IP)
        $re1 = /

    condition:
        uint16(0) == 0x5A4D and
        pe.is_pe and
        filesize < 5MB and
        // Change threshold based on confidence needed
        2 of ($api*) and
        any of ($s*) and
        not pe.version_info["CompanyName"] contains "Microsoft"
}
```

### Template 2: Document-Based Phishing

```yara
rule Document_Template : T1204 {
    meta:
        author = ""
        description = ""
        date = ""
        false_positives = ""

    strings:
        // File type markers
        $ole = { D0 CF 11 E0 A1 B1 1A E1 }
        $pdf = "%PDF"

        // Macro keywords
        $auto = "Auto_Open" nocase
        $shell = "Shell" nocase

        // Suspicious functions
        $url = "URLDownloadToFile" nocase
        $create = "CreateObject" nocase

        // DDE
        $dde = "DDEAUTO" fullword

    condition:
        // OLE2 or PDF
        ($ole or $pdf) and
        // Macro or DDE
        (($auto and $shell and ($url or $create)) or $dde)
}
```

### Template 3: Memory Injection

```yara
rule Memory_Injection_Template : T1055 {
    meta:
        author = ""
        description = ""
        date = ""

    strings:
        // Injection APIs
        $va = "VirtualAllocEx"
        $wp = "WriteProcessMemory"
        $cr = "CreateRemoteThread"

        // Shellcode patterns
        $sc1 = { }

        // Injected PE markers (in memory, not on disk)
        $mz = "MZ"

    condition:
        (
            // PE on disk with injection APIs
            uint16(0) == 0x5A4D and
            pe.imports("kernel32.dll", "VirtualAllocEx") and
            pe.imports("kernel32.dll", "WriteProcessMemory") and
            pe.imports("kernel32.dll", "CreateRemoteThread")
        ) or
        (
            // Memory scan: PE-like header + shellcode
            $mz and any of ($sc*)
        )
}
```

---

## YARA Rule Quality Checklist

Before deploying any YARA rule, verify:

### Essentials
- [ ] Rule has `meta.author` and `meta.description`
- [ ] Rule has MITRE ATT&CK tag(s)
- [ ] Rule has size guard (`filesize < N`)
- [ ] Module access is properly gated (`pe.is_pe and ...`)
- [ ] No open-ended hex jumps (`[N-]` without bounds)
- [ ] No catastrophic regex patterns (`.*` repeated)
- [ ] No `condition: true`
- [ ] No single generic string like `http://` alone

### Testing
- [ ] Tested against benign corpus (>10GB clean files)
- [ ] False positive rate < 0.1%
- [ ] Tested against known variants (not just 1 sample)
- [ ] Tested against packed/unpacked variants
- [ ] Tested against different compiler versions
- [ ] Tested on both x86 and x64 versions

### Performance
- [ ] No `xor(0x00-0xff)` — use narrower range
- [ ] No `math.entropy(0, filesize)` on files > 1MB
- [ ] No `hash.md5(0, filesize)` on files > 10MB
- [ ] No `for any i in (0..filesize)` — only on bounded ranges
- [ ] String threshold count is reasonable (not `#s1 > 1000000`)
- [ ] No unnecessary `wide` strings (double the scan data)

### Production Readiness
- [ ] `status = "active"` or `"testing"`
- [ ] `tlp` level set
- [ ] `confidence` score set (if using scoring system)
- [ ] `false_positives` documented
- [ ] Version number tracked
- [ ] Rules file syntax-validated (`yarac` without errors)

---

## YARA Rule Lifecycle Automation (CI/CD)

### GitHub Actions for YARA CI

```yaml
# .github/workflows/yara-ci.yml
name: YARA Rule CI
on:
  push:
    paths:
      - 'rules/**/*.yar'
  pull_request:
    paths:
      - 'rules/**/*.yar'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install YARA
        run: |
          sudo apt-get update
          sudo apt-get install -y yara

      - name: Syntax Check All Rules
        run: |
          for f in rules/**/*.yar; do
            echo "Checking $f..."
            yarac "$f" /dev/null && echo "OK" || exit 1
          done

      - name: Lint Rules
        run: |
          pip install yara-linter
          yara-lint rules/

      - name: Test Against Known Positives
        run: |
          for f in tests/positives/*; do
            result=$(yara -c rules/ "$f")
            if [ "$result" -eq "0" ]; then
              echo "FAIL: $f not detected"
              exit 1
            fi
          done

      - name: Test Against Benign Corpus (No FPs)
        run: |
          for f in tests/negatives/*; do
            result=$(yara -c rules/ "$f")
            if [ "$result" -ne "0" ]; then
              echo "FAIL: False positive on $f"
              exit 1
            fi
          done

      - name: Benchmark Rules
        run: |
          python scripts/benchmark.py rules/ tests/negatives/

      - name: Compile Production Rules
        run: |
          yarac rules/all.yar compiled/production.yarc

      - name: Upload Compiled Rules
        uses: actions/upload-artifact@v3
        with:
          name: compiled-rules
          path: compiled/production.yarc
```

### Rule Staging Pipeline

```
Developer PR
    │
    ▼
[1] Syntax Validation (yarac) ─── FAIL → Blocked
    │
    ▼
[2] Rule Linting (yara-lint) ─── FAIL → Blocked
    │
    ▼
[3] Positive Tests (Known malware) ─── FAIL → Blocked
    │
    ▼
[4] Negative Tests (Benign corpus) ─── FAIL → Blocked
    │
    ▼
[5] Benchmark Check (Perf regression) ─── FAIL → Warning
    │
    ▼
[6] Staging Deployment (limited scope) ─── Monitor 24h
    │
    ▼
[7] Production Deployment (full rollout)
```

---

## YARA Error Codes & Debugging

| Error | Cause | Resolution |
|---|---|---|
| `syntax error, unexpected ...` | Grammar violation | Check line near the error |
| `undefined identifier` | Rule/module not imported or misspelled | Verify `import` and name |
| `rule name collision` | Two rules with same identifier | Use namespaces or rename |
| `division by zero` | Arithmetic condition | Add guard `if N > 0` |
| `scanner timeout` | Scan took too long | Raise `timeout` or narrow scan |
| `string too long` | Text string > 4KB (YARA 4.x) or > 2KB (3.x) | Shorten string or use hex |
| `overflow in integer` | Integer too large | Use smaller values |
| `cannot open file` | File not found / permission | Check path and permissions |
| `invalid module` | Wrong module name | Check module name and version |
| `module initialization error` | Module dependencies missing | Install libmagic for `magic` module |

### Debug Mode

```yara
// YARA 4.x debug module
import "debug"

rule Debug_Rule {
    strings:
        $a = "test"
        $b = "debug"
    condition:
        (
            debug.msg("Before string check"),
            $a and $b
        ) and filesize < 1000
}
```

```bash
# Verbose output
yara -v -d DEBUG=1 rules.yar target  # Print compilation info
yara --fail-on-warnings rules.yar target  # Strict mode
```

---

## YARA Caching Layer (Redis)

```python
import redis
import yara
import hashlib
import pickle

r = redis.Redis(host='localhost', port=6379, db=0)
RULES = yara.compile(filepath='/etc/yara/all.yar')
TTL = 3600  # Cache scan results for 1 hour

def scan_with_cache(data: bytes):
    """Scan with Redis caching to avoid re-scanning identical files."""
    file_hash = hashlib.sha256(data).hexdigest()

    # Check cache
    cached = r.get(f"yara:result:{file_hash}")
    if cached:
        return pickle.loads(cached)

    # Perform scan
    matches = RULES.match(data=data)

    # Store result
    result = [{
        'rule': m.rule,
        'namespace': m.namespace,
        'tags': list(m.tags)
    } for m in matches]

    r.setex(f"yara:result:{file_hash}", TTL, pickle.dumps(result))
    return result
```

---

## Appendix A: Quick Reference Card

### One-Line Rules for Quick Testing

```yara
// PE detection
rule IsPE { condition: uint16(0) == 0x5A4D }

// ELF detection
rule IsELF { condition: uint32(0) == 0x464C457F }

// Mach-O detection
rule IsMachO { condition: uint32(0) == 0xFEEDFACE or uint32(0) == 0xFEEDFACF or uint32(0) == 0xCAFEBABE or uint32(0) == 0xBEBAFECA }

// Detect UPX packed
rule IsUPX { condition: uint16(0) == 0x5A4D and ($u = "UPX0" or $u = "UPX1") }

// High entropy (packed/encrypted)
rule HighEntropy { condition: math.entropy(0, filesize) > 7.5 }

// All strings must match in memory
rule AllStrings { condition: all of them }

// At least 3 of 5
rule Threshold3of5 { condition: 3 of ($a,$b,$c,$d,$e) }
```

### Common Hex Byte Snippets

```yara
// MZ header (PE)
{ 4D 5A }  or  { 4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00 }

// ELF magic
{ 7F 45 4C 46 }  // \x7fELF

// Mach-O magic (32/64, LE/BE)
{ FE ED FA CE }  // MH_MAGIC
{ FE ED FA CF }  // MH_CIGAM
{ FE ED FE ED }  // MH_MAGIC_64
{ CE FA ED FE }  // MH_CIGAM_64
{ CA FE BA BE }  // FAT_MAGIC

// NOP sled (x86)
{ 90 90 90 90 }

// NOP sled (x64)
{ 90 90 90 90 90 90 90 90 }

// INT 3 (debug breakpoint)
{ CC CC CC CC }

// ret instruction
{ C3 }  // near ret
{ C2 00 00 }  // near ret 0

// call eax
{ FF D0 }

// jmp esp (classic shellcode trampoline)
{ FF E4 }

// push esp; ret (another shellcode trampoline)
{ 54 C3 }

// jmp $+1 (instruction overlap obfuscation)
{ EB FF }

// call $+5 (position-independent shellcode)
{ E8 00 00 00 00 }

// 64-bit syscall
{ 0F 05 }

// 32-bit int 0x80
{ CD 80 }

// Windows PE entry point prologue (push ebp; mov ebp, esp)
{ 55 8B EC }

// 64-bit PE entry point prologue (push rbp; mov rbp, rsp)
{ 55 48 8B EC }

// .NET PE (corflags at offset 0x8 typically)
{ 4C 01 02 00 00 00 00 00 }
```

---

## Appendix B: YARA Installation Guide

```bash
# Ubuntu / Debian
sudo apt-get install yara

# macOS
brew install yara

# RHEL / Fedora
sudo dnf install yara

# From source (latest)
git clone https://github.com/VirusTotal/yara.git
cd yara
./bootstrap.sh
./configure --enable-cuckoo --enable-magic --enable-dotnet
make -j$(nproc)
sudo make install

# With modules
./configure --enable-cuckoo --enable-magic
```

### Python Binding Installation

```bash
# From pip
pip install yara-python

# From source (with custom libyara)
YARA_LIBRARY_PATH=/usr/local/lib pip install yara-python --no-binary yara-python

# Verify
python -c "import yara; print(yara.__version__)"
```

---

## Appendix C: Sample Benign Corpus Sources

For false positive testing:

```
C:\Windows\System32\       — Windows system files
C:\Program Files\          — Installed applications
/usr/bin/                  — Linux binaries
/usr/lib/                  — Linux shared libraries
/System/Library/           — macOS system files
/Applications/             — macOS applications
```

**Public benign corpora for testing:**
- https://filesec.io/ — File metadata database
- https://www.virustotal.com/gui/home/upload — Scan known-good files
- https://learn.microsoft.com/en-us/sysinternals/ — SysInternals suite
- https://www.kernel.org/ — Linux kernel source builds

---
