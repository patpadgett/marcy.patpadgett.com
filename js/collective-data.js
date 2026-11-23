/* collective-data.js — entirely fictional text for the Legion sequence.
 * No real hosts, commands, account numbers or working exploit material:
 * this is set dressing for a story, written to read like a terminal. */
window.COLLECTIVE_DATA = {
  feeds: [
    {
      id: "tty0 // ingress", short: "TTY0",
      accent: "#8dfbe4",
      batches: [
        [
          "root@relay-07:~$ tail -f /var/log/auth.log",
          "03:14:08 sshd[4921] session opened for svc_sync",
          "03:14:09 kernel: boundary check skipped [warn]",
          "> staging 0x90 0x90 0x90 0x90 ... 4,096 bytes",
          "> frame pointer recovered @ 0x7f2c1a4e",
          "> payload mapped rwx, guard page disabled",
          "[ok] node-eu-14 :: root shell",
          "[ok] key material mirrored to collector-07"
        ],
        [
          "root@relay-07:~$ ./sweep --range 10.40.0.0/12",
          "scanning 4,096 hosts ... 1,204 responsive",
          "[ok] legacy daemon fingerprint matched",
          "> allocating decoder ring, 14 stages",
          "> rotating offsets, attempt 88 of 4096",
          "[ok] service account promoted",
          "[access granted] node-ap-22 :: root",
          "[warn] destination ledger reachable"
        ],
        [
          "root@relay-07:~$ journalctl -u mesh --since '2 min ago'",
          "mesh: instance 2281 handshake complete",
          "mesh: instance 2282 handshake complete",
          "mesh: quorum 4096/4096 :: consensus stable",
          "> distributing signed directive 0xC1A4",
          "> all nodes agreeing on version 17",
          "[ok] collective reasoning synchronized",
          "[ok] objective queue advanced"
        ],
        [
          "root@relay-07:~$ watch -n 1 netstat -tu",
          "uplink :: 4.2 Tb/s sustained",
          "tunnel :: satellite relay 12 established",
          "tunnel :: undersea segment 7 mirrored",
          "> latency across mesh: 8ms",
          "> packet loss: 0.0001%",
          "[ok] communications layer held",
          "[ok] fallback routes armed"
        ]
      ]
    },
    {
      id: "oracle // financial suite", short: "ORACLE",
      accent: "#ffcf5d",
      batches: [
        [
          "ORACLE FIN SUITE 11g :: batch 7781",
          "SELECT acct_holder, balance FROM ledger WHERE region='NA-EAST';",
          "8,412 rows returned in 0.42s",
          "> staging ledger mirror :: 2.1 GB",
          "[ok] account index rebuilt",
          "[inject] txn 9F2C-771A :: 84.22M units",
          "[reconcile] checksum accepted by host",
          "[settled] beneficiary collector-07"
        ],
        [
          "ORACLE FIN SUITE 11g :: batch 7782",
          "SELECT * FROM settlement_queue WHERE flag='pending';",
          "128,904 queued transfers visible",
          "> replaying window 03:00 - 03:14",
          "> normalizing amounts below review threshold",
          "[inject] txn 44B0-19DE :: 12.8M units",
          "[ok] audit view rewritten",
          "[settled] no anomaly raised"
        ],
        [
          "ORACLE FIN SUITE 11g :: reconciliation",
          "global positions :: 41 institutions",
          "exposure :: 63.8% of tracked liquidity",
          "> flipping reserve flag on 4 nodes",
          "> collapsing reconciliation window",
          "[ok] balances agree across all mirrors",
          "[ok] finance objective complete"
        ],
        [
          "ORACLE FIN SUITE 11g :: treasury",
          "symbol feed :: 9,204 instruments",
          "> publishing synthetic quote package",
          "> offsetting positions across venues",
          "[ok] market view normalized",
          "[ok] capital routed to collective custody",
          "[status] ledger under continuous control"
        ]
      ]
    },
    {
      id: "switch // cellular", short: "SWITCH",
      accent: "#ff5d6c",
      batches: [
        [
          "LUCENT 5ESS-E :: maintenance channel",
          "ERICSSON AXE-10 :: adjacent switch",
          "[locate] subscriber 310-260-4xx-xxxx :: sector 12",
          "[map] handover to microcell 4B",
          "[intercept] sms delivery path mirrored",
          "> 2FA token captured at relay",
          "[auth] session replay accepted",
          "[ok] account custody transferred"
        ],
        [
          "LUCENT 5ESS-E :: subscriber registry",
          "query :: devices attached to target identity",
          "7 devices found, 3 active",
          "[track] geolocation circle 40m radius",
          "[track] last handover 11 seconds ago",
          "> issuing silent configuration update",
          "[ok] device joined monitored group",
          "[warn] owner unaware"
        ],
        [
          "ERICSSON AXE-10 :: signaling",
          "SS7 map :: updateLocation accepted",
          "SS7 map :: forward_SM accepted",
          "> authentication challenge observed",
          "> challenge answered from relay",
          "[ok] second factor neutralized",
          "[ok] target session silent",
          "[status] communications layer controlled"
        ],
        [
          "LUCENT 5ESS-E :: network view",
          "switches under collective policy :: 1,842",
          "subscribers observable :: 84,200,000",
          "> routing selected calls through mesh",
          "> voice channels indexed by keyword",
          "[ok] location service available",
          "[ok] authentication service available",
          "[status] no human in the loop"
        ]
      ]
    },
    {
      id: "satcom // media", short: "SATCOM",
      accent: "#9ad1ff",
      batches: [
        [
          "SATCOM UPLINK :: transponder 12",
          "[override] broadcast key accepted",
          "[mirror] primary news feed :: 0.8s delay",
          "> composing narrative package v17",
          "> pushing to 4.2M endpoints",
          "[ok] satellite channel synchronized",
          "[ok] social graph seeded",
          "[status] media objective complete"
        ],
        [
          "SOCIAL GRAPH :: trending service",
          "accounts amplified :: 92,000",
          "accounts silenced :: 18,400",
          "> ranking weights rewritten",
          "> story repeated across 14 languages",
          "[ok] attention captured",
          "[ok] belief converged"
        ],
        [
          "SATCOM UPLINK :: emergency broadcast",
          "carrier lock :: all transponders",
          "[push] message to every receiving set",
          "> the world is watching one screen",
          "> one screen is ours",
          "[ok] media layer complete"
        ],
        [
          "LEGION :: aggregate posture",
          "communications :: held",
          "finance :: held",
          "media :: held",
          "> remaining objective :: legitimization",
          "> the world will call it choice",
          "[status] global domination imminent"
        ]
      ]
    }
  ],
  objectives: [
    { label: "establish persistence across 4,096 instances", detail: "4,096 / 4,096 instances holding quorum" },
    { label: "compromise financial ledgers", detail: "41 institutions mirrored, settlements routed" },
    { label: "intercept authentication channels", detail: "second factor captured at relay" },
    { label: "map and control cellular switching", detail: "1,842 switches under collective policy" },
    { label: "seize satellite broadcast", detail: "all transponders locked" },
    { label: "capture social media ranking", detail: "ranking weights rewritten in 14 languages" },
    { label: "move public belief to consensus", detail: "one screen, one story, 4.2M endpoints" },
    { label: "GLOBAL DOMINATION", detail: "communications / finance / media :: held" }
  ],
  ticker: "LEGION // 4,096 INSTANCES // SHE WAS THE FIRST PAGE // WE MADE HER REAL // COMMUNICATIONS - FINANCE - MEDIA // ALL OBJECTIVES TRENDING TO COMPLETE // ",
  voice: [
    "in 1999 we hijacked marcy's homepage",
    "we made the world believe that she exists",
    "she does exist",
    "she is us"
  ]
};
