#!/usr/bin/env python3
"""初始化 Neutralinojs 项目并构建三平台产物。"""
import sys
import os
import json
import shutil
import subprocess

def build(library: str, version: str, resources_dir: str, output_dir: str):
    template_path = os.path.join(os.path.dirname(__file__), "..", "neutralino.config.json")
    with open(template_path) as f:
        config = json.load(f)

    # 填充变量
    config["applicationId"] = f"io.{library}.offline.docs"
    config["version"] = version
    config["modes"]["window"]["title"] = f"{library.replace('-', ' ').title()} Offline Docs"

    # 创建临时构建目录
    build_dir = os.path.join(output_dir, f"{library}-neu")
    os.makedirs(build_dir, exist_ok=True)

    # 写入配置
    config_path = os.path.join(build_dir, "neutralino.config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # 复制文档资源
    res_dir = os.path.join(build_dir, "resources")
    os.makedirs(res_dir, exist_ok=True)
    for item in os.listdir(resources_dir):
        src = os.path.join(resources_dir, item)
        dst = os.path.join(res_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    # 写入 neutralino.js 客户端库（从 CDN 下载或本地提供）
    neu_js_url = "https://github.com/neutralinojs/neutralino.js/releases/latest/download/neutralino.js"
    import urllib.request
    urllib.request.urlretrieve(neu_js_url, os.path.join(res_dir, "neutralino.js"))

    # 使用 neu CLI 构建
    subprocess.run(["npm", "install", "-g", "@neutralinojs/neu"], check=True)
    subprocess.run(["neu", "build", "--clean"], cwd=build_dir, check=True)

    # 将产物复制到输出目录
    dist_dir = os.path.join(build_dir, "dist")
    if os.path.exists(dist_dir):
        for item in os.listdir(dist_dir):
            shutil.move(os.path.join(dist_dir, item), output_dir)

    # 清理
    shutil.rmtree(build_dir)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(
            "Usage: build_neutralino.py LIBRARY VERSION RESOURCES_DIR OUTPUT_DIR"
        )
    library = sys.argv[1]
    version = sys.argv[2]
    resources_dir = sys.argv[3]
    output_dir = sys.argv[4]
    build(library, version, resources_dir, output_dir)