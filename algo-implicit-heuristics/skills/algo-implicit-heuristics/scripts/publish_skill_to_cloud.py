# -*- coding: utf-8 -*-
"""把 skills/<name>/ 打包上传到 WorkBuddy 云端个人技能库。

用途
----
客户端 `~/.workbuddy/skills/` 里的技能是**本地个人库**，Web 端 / 云端任务看不到
（官方说明：Web 端与客户端的个人 Skill 库互不相通；云上任务只能选云上个人库里的 Skill）。
本脚本走客户端主进程暴露的 WBIPC `wb.request/http.fetch` 通道（自动带登录态），
把技能包 POST 到 `/v2/user-asset/custom-skills`，使其在云端可用。

用法
----
    python scripts/publish_skill_to_cloud.py algo-implicit-heuristics
    python scripts/publish_skill_to_cloud.py algo-implicit-heuristics --version 2.9.0

前置条件
--------
1. 客户端已登录（云端接口需要 Bearer token，由宿主注入）。
2. `skills/<name>/SKILL.md` 存在，且 frontmatter 至少含 `name` 与 `description`
   （服务端会解析 frontmatter，YAML 非法会直接判 invalid）。

幂等性
------
同名重复上传会在云端产生新的 skillUid（多版本并存），不会覆盖旧版本。
重复发布前请确认版本号已递增。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import uuid
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_PATH = "/v2/user-asset/custom-skills"
LIST_PATH = "/v2/user-asset/skill/get-list"
TERMINAL_STATUS = ("ready", "invalid", "failed")


def find_wbipc_module():
    """定位内置 workbuddy_ipc 客户端（library skill 携带，纯标准库实现）。"""
    candidates = []
    for base in (
        os.path.join(os.path.expanduser("~"), "Desktop", "文件", "WorkBuddy", "resources",
                     "app.asar.unpacked", "resources", "plugins", "workbuddy-builtin", "skills", "library"),
        os.path.join(os.path.expanduser("~"), "Desktop", "文件", "WorkBuddy", "resources",
                     "app.asar.unpacked", "resources", "plugins", "workbuddy-builtin", "builtin-plugins",
                     "tencent-docs-plugin", "skills", "tencent-saas-docs"),
    ):
        candidates.append(base)
    plugins_root = os.path.join(os.path.expanduser("~"), ".workbuddy", "plugins", "cache",
                                "workbuddy-builtin", "skill-library")
    if os.path.isdir(plugins_root):
        for entry in sorted(os.listdir(plugins_root), reverse=True):
            candidates.append(os.path.join(plugins_root, entry))
    for path in candidates:
        if os.path.isfile(os.path.join(path, "workbuddy_ipc", "__init__.py")):
            return path
    raise SystemExit("未找到 workbuddy_ipc 模块，请确认 WorkBuddy 客户端已安装")


def read_frontmatter(skill_md_path):
    text = open(skill_md_path, encoding="utf-8").read()
    match = re.match(r"^---\s*\r?\n([\s\S]*?)\r?\n---", text)
    if not match:
        raise SystemExit(f"{skill_md_path} 缺少 YAML frontmatter，无法上传")
    meta = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    if not meta.get("name") or not meta.get("description"):
        raise SystemExit("frontmatter 缺少 name 或 description，服务端会判 invalid")
    return meta


def build_zip(skill_dir):
    buffer = __import__("io").BytesIO()
    skill_name = os.path.basename(skill_dir.rstrip(os.sep))
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(skill_dir):
            for name in files:
                if name.startswith(".") or name.endswith(".pyc"):
                    continue
                full = os.path.join(root, name)
                arc = os.path.join(skill_name, os.path.relpath(full, skill_dir)).replace("\\", "/")
                zf.write(full, arc)
    return buffer.getvalue()


def multipart_body(fields, filename, blob, boundary):
    chunks = []
    for key, value in fields.items():
        chunks.append(
            (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n")
            .encode("utf-8")
        )
    chunks.append(
        (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
         "Content-Type: application/zip\r\n\r\n").encode("utf-8") + blob + b"\r\n"
    )
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", help="skills/ 下的技能目录名")
    parser.add_argument("--version", help="覆盖 frontmatter 里的 version")
    parser.add_argument("--wait", type=int, default=60, help="等待审核就绪的秒数")
    args = parser.parse_args()

    skill_dir = os.path.join(REPO_ROOT, "skills", args.skill)
    if not os.path.isdir(skill_dir):
        raise SystemExit(f"找不到技能目录 {skill_dir}")
    skill_md = os.path.join(skill_dir, "SKILL.md")
    meta = read_frontmatter(skill_md)
    version = args.version or meta.get("version") or "1.0.0"

    blob = build_zip(skill_dir)
    boundary = "----WBSkill" + uuid.uuid4().hex
    body = multipart_body(
        {
            "name": meta["name"],
            "title": meta.get("display_name") or meta["name"],
            "description": meta["description"],
            "version": version,
        },
        f"{meta['name']}.zip",
        blob,
        boundary,
    )

    sys.path.insert(0, find_wbipc_module())
    from workbuddy_ipc import connect  # noqa: E402

    def fetch(method, path, query=None, body_b64=None, content_type=None):
        with connect(client_id="skill-publisher", client_kind="skill") as wb:
            pipe = wb.get_pipe("wb.request")
            req = {"method": method, "path": path, "headers": {"accept": "application/json"}}
            if query:
                req["query"] = {k: str(v) for k, v in query.items()}
            if body_b64 is not None:
                req["body_b64"] = body_b64
                req["headers"]["content-type"] = content_type
            resp = pipe.invoke("http.fetch", req)
            return resp["status"], json.loads(base64.b64decode(resp["body_b64"]).decode("utf-8"))

    status, payload = fetch(
        "POST", UPLOAD_PATH,
        body_b64=base64.b64encode(body).decode(),
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    if payload.get("code") != 0:
        raise SystemExit(f"上传失败: {payload}")
    uid = payload["data"]["skillUid"]
    print(f"已上传 skillUid={uid} version={version} status={payload['data'].get('status')}")

    deadline = time.time() + args.wait
    while time.time() < deadline:
        _, detail = fetch("GET", f"{UPLOAD_PATH}/{uid}")
        state = (detail.get("data") or {}).get("status")
        if state in TERMINAL_STATUS:
            print(f"最终状态: {state}")
            if state != "ready":
                raise SystemExit(f"云端校验未通过: {detail}")
            break
        time.sleep(3)
    else:
        print("等待超时，可稍后手动确认状态。")

    _, listing = fetch("GET", LIST_PATH, query={"source": "custom", "page_no": 1, "page_size": 50})
    items = (listing.get("data") or {}).get("items") or []
    print(f"云端个人技能库现有 {len(items)} 项: " + ", ".join(i.get("name", "?") for i in items))


if __name__ == "__main__":
    main()
