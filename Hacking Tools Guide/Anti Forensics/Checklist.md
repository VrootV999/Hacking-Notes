
# 🧨 Anti-Forensics Expert Checklist (Red Team / Adversarial Simulation)

## 🛠️ 1. Environment Preparation
- [ ] Setup encrypted VMs or containerized workspaces
- [ ] Use anonymity-preserving OS (Tails, Whonix)
- [ ] Disable telemetry/logging on system
- [ ] Use RAM-only or in-memory execution techniques
- [ ] Test environment against forensics tools

---

## 🧽 2. Data Manipulation & Artifact Evasion
- [ ] Wipe disk free space (`shred`, `SDelete`, `BleachBit`)
- [ ] Overwrite file metadata (`exiftool -all=`, `Metagoofil`)
- [ ] Modify MAC timestamps (`Timestomp`)
- [ ] Clear shell & system history (`history -c`, `.bash_history`)
- [ ] Disable system logs (`auditd`, `journald`, `wevtutil`)

---

## 🧱 3. Evasion & Persistence Techniques
- [ ] Use fileless execution (e.g., PowerShell, LOLBins)
- [ ] Inject payloads into memory (`reflective DLL`, `msf`)
- [ ] Encrypt payloads or use packers
- [ ] Obfuscate scripts (`Invoke-Obfuscation`, `ConfuserEx`)
- [ ] Employ decoys or false artifacts to mislead investigation

---

## 🕵️ 4. Logging & Monitoring Evasion
- [ ] Identify and disable audit mechanisms
- [ ] Manipulate log entries or truncate logs
- [ ] Wipe or rotate logs on exfil
- [ ] Kill or evade EDR/AV systems

---

## 📤 5. Data Exfiltration Techniques
- [ ] Covert channels (DNS tunneling, HTTPS over Tor)
- [ ] Steganography tools (`steghide`, `zsteg`)
- [ ] Compression + Encryption (`7z`, `gpg`, `AEScrypt`)
- [ ] Use burner services (AnonFiles, temp email, dead drop)

---

## 🔚 6. Cleanup
- [ ] Secure erase of payloads and tools
- [ ] Kill running memory-resident payloads
- [ ] Reboot or corrupt VM snapshots
- [ ] Shred configuration and temp files
- [ ] Leave minimal or no forensic footprint

---

## 🧰 Recommended Anti-Forensics Tools

| Purpose                 | Tool                             |
|-------------------------|----------------------------------|
| File Wiping             | `SDelete`, `shred`, `BleachBit` |
| Timestamps Manipulation | `Timestomp`, `Touch`            |
| Metadata Removal        | `ExifTool`, `MAT2`              |
| In-Memory Execution     | `Reflective DLL`, `Powersploit` |
| Obfuscation             | `Invoke-Obfuscation`, `Veil`    |
| Stego/Hidden Data       | `steghide`, `zsteg`, `Snow`     |
| Log Clearing            | `wevtutil`, `auditctl`, `clear` |

