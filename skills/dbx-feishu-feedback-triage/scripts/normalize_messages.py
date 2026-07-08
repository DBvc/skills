#!/usr/bin/env python3
"""Normalize Feishu/Lark message JSON into a small evidence shape.

Input may be a JSON array or an object with messages/items/data.items.
The script does not fetch Feishu data. It only reshapes already-fetched data.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def read_json(path: str | None) -> Any:
    raw = sys.stdin.read() if not path or path == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def pick(d: dict[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        cur: Any = d
        ok = True
        for part in key.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok and cur not in (None, ""):
            return cur
    return default


def extract_messages(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if not isinstance(obj, dict):
        return []
    for key in ("messages", "items"):
        val = obj.get(key)
        if isinstance(val, list):
            return [x for x in val if isinstance(x, dict)]
    data = obj.get("data")
    if isinstance(data, dict):
        for key in ("items", "messages"):
            val = data.get(key)
            if isinstance(val, list):
                return [x for x in val if isinstance(x, dict)]
    return []


def content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        stripped = content.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                return content_to_text(parsed)
            except Exception:
                return stripped
        return stripped
    if isinstance(content, dict):
        parts: list[str] = []
        for key in ("text", "title", "content", "value", "plain_text"):
            val = content.get(key)
            if isinstance(val, str) and val.strip():
                parts.append(val.strip())
        if "elements" in content and isinstance(content["elements"], list):
            for el in content["elements"]:
                txt = content_to_text(el)
                if txt:
                    parts.append(txt)
        return "\n".join(dict.fromkeys(parts))
    if isinstance(content, list):
        return "\n".join(x for x in (content_to_text(x) for x in content) if x)
    return str(content)


def normalize_one(msg: dict[str, Any], max_text_chars: int) -> dict[str, Any]:
    message_id = pick(msg, "message_id", "msg_id", "id", "message.message_id")
    sender = pick(msg, "sender.sender_id.user_id", "sender.sender_id.open_id", "sender.id", "sender.name", "from", default="unknown")
    sender_type = pick(msg, "sender.sender_type", "sender.type", default="unknown")
    create_time = pick(msg, "create_time", "created_at", "timestamp", "send_time", default="")
    chat_id = pick(msg, "chat_id", "chat.id", "conversation_id", default="")
    thread_id = pick(msg, "thread_id", "root_id", "parent_id", "message.thread_id", default="")
    message_type = pick(msg, "message_type", "msg_type", "type", default="unknown")
    text = content_to_text(pick(msg, "text", "content", "body", "message.content", default=""))
    truncated = False
    if max_text_chars > 0 and len(text) > max_text_chars:
        text = text[:max_text_chars] + "..."
        truncated = True
    return {
        "message_id": str(message_id) if message_id else "",
        "sender_label": str(sender),
        "sender_type": str(sender_type),
        "create_time": str(create_time),
        "chat_id": str(chat_id),
        "thread_id": str(thread_id),
        "message_type": str(message_type),
        "text": text,
        "text_truncated": truncated,
        "has_resource": bool(pick(msg, "file_key", "image_key", "resource", "attachments", default=False)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize already-fetched Feishu/Lark message JSON.")
    parser.add_argument("input", nargs="?", default="-", help="JSON file path, or stdin when omitted")
    parser.add_argument("--max-text-chars", type=int, default=1200, help="Truncate message text to this many chars, 0 disables")
    args = parser.parse_args()

    obj = read_json(args.input)
    msgs = extract_messages(obj)
    normalized = [normalize_one(m, args.max_text_chars) for m in msgs]
    warnings = []
    if not normalized:
        warnings.append("no messages found")
    if any(not m["message_id"] for m in normalized):
        warnings.append("some messages have no message_id")

    print(json.dumps({"count": len(normalized), "messages": normalized, "warnings": warnings}, ensure_ascii=False, indent=2))
    return 0 if normalized else 1


if __name__ == "__main__":
    sys.exit(main())
