#!/usr/bin/env python3
"""扫描 artifacts 目录，按库名分组创建 GitHub Release。"""
import os
import subprocess
import re
from collections import defaultdict

def group_artifacts(artifacts_dir: str) -> dict:
    """按库名和版本号分组产物文件。"""
    groups = defaultdict(lambda: defaultdict(list))
    for root, dirs, files in os.walk(artifacts_dir):
        for f in files:
            # 文件名格式: library-os-version-filename
            match = re.match(r'(.+?)-(ubuntu|windows|macos)-v([\d.]+)-(.+)', f)
            if match:
                library, os_name, version, rest = match.groups()
                key = f"{library}-v{version}"
                groups[key][library].append(os.path.join(root, f))
    return groups

def create_release(library: str, version: str, files: list):
    tag = f"{library}-v{version}"
    print(f"📦 Creating release {tag} with {len(files)} files...")
    files_args = []
    for f in files:
        files_args.extend(["--upload-file", f])
    subprocess.run(
        ["gh", "release", "create", tag,
         "--title", f"{library.replace('-', ' ').title()} Docs v{version}",
         "--notes", f"Auto-built offline documentation for {library} v{version}.",
         "--latest"] + files_args,
        check=True
    )

if __name__ == "__main__":
    artifacts_dir = "artifacts"
    groups = group_artifacts(artifacts_dir)
    for tag, lib_files in groups.items():
        for library, files in lib_files.items():
            version = tag.split("-v")[1]
            create_release(library, version, files)