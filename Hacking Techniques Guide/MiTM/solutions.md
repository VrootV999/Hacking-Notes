# ARP spoofing
## IoC
- `Gratuitous ARP replies`
- `duplicate MAC address`
- `ARP Volatility`
- `static ARP entry overwrites`
- `Asymmetrical ARP Traffic`
- `MAC/IP Mismatch in Logs`

## Defensive Solution
- Enable Dynamic ARP Inspection(DAI)
- Configure static ARP bindings

## Monitoring Solution
- Arpwatch
- IDS/IPS(Snort/Suricata)

## Detection Rules
- SIGMA Rule 
```yaml
title: Potential ARP Spoofing Activity Detected
id: arp-spoofing-detection-01
status: experimental
description: Detects anomalies or high-frequency ARP response patterns indicative of cache poisoning.
author: Security Analyst
date: 2026/09/15
logsource:
    category: network_connection
    product: zeek
detection:
    selection:
        proto: arp
        arp_op_code: "arp-reply"
    condition: selection
falsepositives:
    - Legitimate dynamic IP changes or DHCP re-allocations in large environments.
level: high
```

## Queries
- SPLUNK SPL query
```spl
index=network sourcetype=arp_table 
| stats distinct_count(IP_Address) as IP_Count values(IP_Address) as Associated_IPs by MAC_Address 
| where IP_Count > 1
```

- KQL Query
```kql
DeviceNetworkEvents
| where ActionType == "ArpTableEntryModified"
| summarize TargetCount = dcount(LocalIP) by MacAddress, GatewayIP = RemoteIP
| where TargetCount > 1
```

---
# DNS Spoofing
## IoC
- `Unsolicited DNS respone packets(cache poisoning)`
- `Discrepancies between expected authoritative DNS server IPs and teh actual IP addresses returned in resolution logs.`
- `sudden spikes in failed or anomalous DNS queries toward suspicious local IP endpoints.`

## Defensive Solution
- `Implement DNSSEC(DNS security Extensions) to sign and verify the authenticity of DNS records`
- `Use secure, encrypted DNS protocols like DoH(DNS over HTTPS) or DOT(DNS over TLS) to prevent local tampering`

## Monitoring Solution

- SIGMA Rule
```yaml
title: Potential DNS Spoofing or Cache Poisoning
id: dns-spoofing-detection-01
status: experimental
description: Detects mismatched DNS answers or high volumes of unrequested DNS reply packets.
author: Security Analyst
date: 2026/09/15
logsource:
    category: dns
    product: zeek
detection:
    selection:
        query_status: "SUCCESS"
        answers_count: ">0"
    condition: selection
falsepositives:
    - Legitimate internal DNS forwarders or captive portals.
level: high
```

## Queries
- SPLUNK SPL Query
```spl
index=dns sourcetype=stream:dns 
| stats values(answer) as Resolved_IPs count by query 
| where count > 5 AND mvcount(Resolved_IPs) > 1
```

- KQL Query
```kql
DeviceNetworkEvents
| where ActionType == "DnsQueryResolved"
| summarize UniqueIPs = dcount(RemoteIP) by DomainName
| where UniqueIPs > 2
```

---
