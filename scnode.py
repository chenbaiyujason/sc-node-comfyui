import torch
import numpy as np
from PIL import Image, ImageEnhance
import os
import openai
import re


class OnePostGPT:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": ("ASCII", {"multiline": False}),
                "role": ("ASCII", {"multiline": False}),
                "text": ("ASCII", ),
            }
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_string"

    CATEGORY = "SC"

    def text_string(self, text,key,role):
        openai.api_key = key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": role, "content": text}
            ]
        )
        return (completion.choices[0].message,)


class PromptPreview:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("ASCII",),}
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "display"

    CATEGORY = "SC"

    def display(self, text):
        text = str(text)
        text1 = text.split("\": \"")[1:]
        text2 = ''.join(str(t) for t in text1).split("\",")[:-1]
        print(text1,text2)
        result = ''.join(str(t) for t in text2).encode().decode('unicode_escape')
        print(result)
        return (result,)


class String_TO_ASCII:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING",),}
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "S2A"

    CATEGORY = "SC"

    def S2A(self, text):
        return (text,)


class SCCLIPTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("ASCII",), "clip": ("CLIP", )}}
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "SC"

    def encode(self, clip, text):
        return ([[clip.encode(text), {}]], )


NODE_CLASS_MAPPINGS = {
    "One Post to GPT": OnePostGPT,
    "String Preview": PromptPreview,
    "String to ASCII": String_TO_ASCII,
    "SCSCCLIPTextEncode": SCCLIPTextEncode
}
