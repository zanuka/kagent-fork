#!/usr/bin/env python3

import sys
import pkg_resources
import os

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Python path:", sys.path)
print("Environment variables:")
for key, value in os.environ.items():
    print(f"{key}={value}")

print("\nInstalled packages:")
for package in pkg_resources.working_set:
    print(f"{package.key}=={package.version}")

try:
    import openai
    print("\nOpenAI package successfully imported")
    print("OpenAI version:", openai.__version__)
    print("OpenAI path:", openai.__file__)
    print("OpenAI dir:", dir(openai))
    
    print("\nChecking for openai.types.chat module...")
    try:
        from openai.types import chat
        print("Successfully imported 'openai.types.chat'")
        print("Chat module dir:", dir(chat))
    except ImportError as e:
        print(f"Error importing openai.types.chat: {e}")
    
    print("\nChecking for autogen_ext.models.openai...")
    try:
        import autogen_ext.models.openai
        print("Successfully imported 'autogen_ext.models.openai'")
        print("Module dir:", dir(autogen_ext.models.openai))
    except ImportError as e:
        print(f"Error importing autogen_ext.models.openai: {e}")
        
    print("\nChecking the problematic import directly...")
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        print("Successfully imported OpenAIChatCompletionClient")
    except ImportError as e:
        print(f"Error importing OpenAIChatCompletionClient: {e}")
        import traceback
        traceback.print_exc()
except ImportError as e:
    print(f"\nError importing openai: {e}") 
