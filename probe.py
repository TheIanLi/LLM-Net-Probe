#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import requests

PROXY_PORT = 7897
# 换成了 Groq 的 API 和 Llama3 模型
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"
REQUEST_TIMEOUT = 15

def get_os_and_host_ip() -> tuple:
    current_platform = sys.platform
    if current_platform == "win32":
        return "Windows", "127.0.0.1"
    elif current_platform.startswith("linux"):
        cmd = "ip route | grep default | awk '{print $3}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return "WSL2", result.stdout.split('\n')[0].strip()
    sys.exit(1)

def setup_proxy(host_ip: str, port: int):
    proxy_url = f"http://{host_ip}:{port}"
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    os.environ['http_proxy'] = proxy_url
    os.environ['https_proxy'] = proxy_url
    print(f"[INFO] 代理已注入: {proxy_url}")

def test_groq_api():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n[ERROR] 缺少环境变量 GROQ_API_KEY")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": "我正在进行全平台网络诊断，请只回复'网络畅通'四个字。"}],
        "temperature": 0.0
    }

    print(f"\n[INFO] 开始请求 Groq API ({GROQ_MODEL})...")
    start_time = time.time()
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        reply_content = response.json()["choices"][0]["message"]["content"].strip()
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        print("\n================ 测试结果 ================")
        print("[SUCCESS] API 请求成功！您的节点完美支持海外高频调用。")
        print(f"[INFO] 接口耗时: {elapsed_ms} ms (不愧是地表最快 Groq!)")
        print(f"[INFO] 模型回复: {reply_content}")
        print("==========================================")

    except requests.exceptions.HTTPError as e:
        print(f"\n[ERROR] HTTP 错误: 状态码 {response.status_code}")
        print(f"-> 真实报错内容: {response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 发生异常: {e}")
        sys.exit(1)

def main():
    print(">>> 开始执行跨平台 AI 环境网络连通性检测 (Groq / Llama3 版) <<<")
    os_type, host_ip = get_os_and_host_ip()
    setup_proxy(host_ip, PROXY_PORT)
    test_groq_api()

if __name__ == "__main__":
    main()
