#!/usr/bin/env python3
"""Build the ChatGPT (Agent Plugins portable format) package of this plugin.

One repository serves two directories that read different files:

- Claude reads `.claude-plugin/plugin.json` and `.mcp.json`. Its directory
  refuses any field outside its allowed lists (LOCAL_CODE_UNKNOWN_KEY), so
  those two files stay minimal and no OpenAI field may be in the repository
  as a manifest or MCP file.
- ChatGPT reads a root `plugin.json` and a root `mcp.json` in the Agent
  Plugins format, with its sign-in settings under `extensions["com.openai"]`.

This script writes the ChatGPT files from the Claude manifest plus the
overlay below, and zips them with the same skills. The name, version,
description and author come from `.claude-plugin/plugin.json`, so the two
packages cannot drift apart.

    python3 scripts/build_chatgpt_package.py        # writes dist/eudr-chatgpt-<version>.zip
"""
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = "https://eudr.dev/mcp"

# Listing text for ChatGPT. Same words as chatgpt-app-submission.json.
INTERFACE = {
    "displayName": "EUDR compliance",
    "shortDescription": "Deforestation checks and DDS",
    "developerName": "Vortx AI Private Limited",
    "category": "productivity",
    "websiteURL": "https://eudr.dev",
    "privacyPolicyURL": "https://eudr.dev/privacy",
    "termsOfServiceURL": "https://eudr.dev/legal/terms",
    "composerIcon": "./assets/chatgpt-composer-icon-192.png",
    "logo": "./assets/chatgpt-directory-icon-512.png",
}

# Mixed access: the read tools work with no sign-in, eudr_prepare_dds asks for OAuth.
AUTH = {
    "type": "mixed",
    "client": {"mode": "dcr"},
    "authorizationUrl": "https://eudr.dev/oauth/authorize",
    "tokenUrl": "https://eudr.dev/oauth/token",
    "registrationUrl": "https://eudr.dev/oauth/register",
    "authorizationServerBase": "https://eudr.dev",
    "resource": ENDPOINT,
    "baseScopes": ["eudr:read", "eudr:write"],
}


def build():
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    app = json.loads((ROOT / "chatgpt-app-submission.json").read_text())["app_info"]
    claude_mcp = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]
    if list(claude_mcp) != ["eudr"] or claude_mcp["eudr"].get("url") != ENDPOINT:
        sys.exit("the Claude .mcp.json no longer names one server 'eudr' at " + ENDPOINT)

    interface = dict(INTERFACE, longDescription=app["description"])
    plugin = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": claude["name"],
        "version": claude["version"],
        "description": claude["description"],
        "author": claude["author"],
        "homepage": claude["homepage"],
        "repository": claude["repository"],
        "license": claude["license"],
        "keywords": claude["keywords"],
        "extensions": {"com.openai": {"interface": interface}},
    }
    mcp = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {
            "eudr": {
                "type": "streamable-http",
                "url": ENDPOINT,
                "extensions": {"com.openai": {"auth": AUTH}},
            }
        },
    }

    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    target = out / f"eudr-chatgpt-{claude['version']}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("plugin.json", json.dumps(plugin, indent=2) + "\n")
        z.writestr("mcp.json", json.dumps(mcp, indent=2) + "\n")
        for name in ("README.md", "LICENSE"):
            z.write(ROOT / name, name)
        for f in sorted((ROOT / "skills").rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(ROOT).as_posix())
        for f in sorted((ROOT / "submission-assets").glob("chatgpt-*.png")):
            z.write(f, "assets/" + f.name)
        names = z.namelist()
    for path in (interface["composerIcon"], interface["logo"]):
        if path[2:] not in names:
            sys.exit(f"{path} is named in the manifest and is not in the package")
    print(target.relative_to(ROOT), f"{target.stat().st_size} bytes, {len(names)} files")
    return target


if __name__ == "__main__":
    build()
