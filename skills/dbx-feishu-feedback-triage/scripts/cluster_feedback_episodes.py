#!/usr/bin/env python3
"""Create rough feedback episode groups from normalized messages.

This is a helper, not a judge. It groups by thread/root id first and otherwise
keeps a conservative per-message episode so the model can merge with domain context.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

FEEDBACK_HINT_RE = re.compile(
    r"(报错|错误|失败|打不开|看不到|不展示|不能|无法|异常|bug|需求|希望|能不能|怎么|如何|权限|配置|500|403|超时|导出|同步)",
    re.I,
)


def read_json(path: str | None) -> Any:
    raw = sys.stdin.read() if not path or path == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def get_messages(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict) and isinstance(obj.get("messages"), list):
        return [x for x in obj["messages"] if isinstance(x, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Cluster normalized Feishu messages into rough episodes.")
    parser.add_argument("input", nargs="?", default="-", help="Normalized JSON file path, or stdin")
    parser.add_argument("--include-non-feedback", action="store_true", help="Keep messages without simple feedback keywords")
    args = parser.parse_args()

    msgs = get_messages(read_json(args.input))
    # First pass: decide which threaded groups contain at least one feedback-like message.
    group_has_feedback: dict[str, bool] = {}
    group_order: list[str] = []
    message_groups: list[tuple[str, int, dict[str, Any]]] = []

    for idx, msg in enumerate(msgs, start=1):
        text = str(msg.get("text", ""))
        thread_id = str(msg.get("thread_id") or "")
        if thread_id:
            key = f"thread:{thread_id}"
        else:
            mid = str(msg.get("message_id") or idx)
            key = f"message:{mid}"
        if key not in group_has_feedback:
            group_has_feedback[key] = False
            group_order.append(key)
        if FEEDBACK_HINT_RE.search(text):
            group_has_feedback[key] = True
        message_groups.append((key, idx, msg))

    episodes: "OrderedDict[str, dict[str, Any]]" = OrderedDict()
    for key in group_order:
        if args.include_non_feedback or group_has_feedback.get(key):
            episodes[key] = {"episode_id": key, "message_ids": [], "thread_ids": [], "messages": []}

    for key, idx, msg in message_groups:
        if key not in episodes:
            continue
        text = str(msg.get("text", ""))
        thread_id = str(msg.get("thread_id") or "")
        ep = episodes[key]
        mid = str(msg.get("message_id") or "")
        if mid:
            ep["message_ids"].append(mid)
        if thread_id and thread_id not in ep["thread_ids"]:
            ep["thread_ids"].append(thread_id)
        ep["messages"].append({
            "message_id": mid,
            "sender_label": msg.get("sender_label", "unknown"),
            "create_time": msg.get("create_time", ""),
            "text": text,
        })

    result = {"count": len(episodes), "episodes": list(episodes.values())}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
