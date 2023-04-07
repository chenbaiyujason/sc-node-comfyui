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

    CATEGORY = "SC/GPT"

    def text_string(self, text,key,role):
        openai.api_key = key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": role, "content": text}
            ]
        )
        return (completion.choices[0].message,)


class MultiplePostGPT:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": ("ASCII", {"multiline": False}),
                "Messages": ("ASCII", {"multiline": False}),

            }
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_string"

    CATEGORY = "SC/GPT"

    def text_string(self, key,Messages):
        openai.api_key = key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=Messages,
        )
        return (completion.choices[0].message,)




class OneGPTBuilder:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "role": ("ASCII", {"multiline": False}),
                "text": ("ASCII", ),
            }
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_string"

    CATEGORY = "SC/GPT"

    def text_string(self, text,role):
        message= {"role": role, "content": text}
        return (message,)


class CombineGPTBuilder:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "PromptA": ("ASCII",),
                "PromptB": ("ASCII", ),
            }
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_string"

    CATEGORY = "SC/GPT"

    def text_string(self, PromptA,PromptB):
        messages=[PromptA,PromptB]
        return (messages,)


# Prompt Preview
class PromptPreview:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("ASCII",),}
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "display"

    CATEGORY = "SC/Text"

    def display(self, text):
        text = str(text)
        text1 = text.split("\": \"")[1:]
        text2 = ''.join(str(t) for t in text1).split("\",")[:-1]
        result = ''.join(str(t) for t in text2).encode().decode('unicode_escape')
        print(f"GPT返回预览：\n{result}")
        return (result,)


class String_TO_ASCII:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING",),}
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "S2A"

    CATEGORY = "SC/Text"

    def S2A(self, text):
        return (text,)


class SCCLIPTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("ASCII",), "clip": ("CLIP", )}}
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "SC/Img"

    def encode(self, clip, text):
        return ([[clip.encode(text), {}]], )




# Multiple Text String Node

class Multiple_Text_String:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": True}),
            }
        }
    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_string"

    CATEGORY = "SC/Text"

    def text_string(self, text):
        return (text, )

# Text String Node

class Single_Text_String:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": False}),
            }
        }
    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_string"

    CATEGORY = "SC/Text"

    def text_string(self, text):
        return (text, )

# Text Combine

class Combine_Text_String:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text1": ("ASCII", {"default": '', "multiline": False}),
                "text2": ("ASCII", {"default": '', "multiline": False}),
            }
        }
    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_combine"

    CATEGORY = "SC/Text"

    def text_combine(self, text1,text2):
        return (text1+text2, )


class Builder_Text_String:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("ASCII",),
                "prefix": ("STRING", {"default": '', "multiline": False}),
                "suffix": ("STRING", {"default": '', "multiline": False}),
            }
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_to_console"

    CATEGORY = "SC/Text"

    def text_to_console(self, text, prefix,suffix):
        t = prefix+text+suffix
        return (t, )


# Text Search

class SC_Search_and_Replace:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("ASCII",),
                "find": ("STRING", {"default": '', "multiline": False}),
                "replace": ("STRING", {"default": '', "multiline": False}),
            }
        }

    RETURN_TYPES = ("ASCII",)
    FUNCTION = "text_search_and_replace"

    CATEGORY = "SC/Text"

    def text_search_and_replace(self, text, find, replace):
        return (self.replace_substring(text, find, replace), )

    def replace_substring(self, text, find, replace):
        import re
        text = re.sub(find, replace, text)
        return text


class SC_Text_to_Console:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("ASCII",),
                "label": ("STRING", {"default": f'Text Output', "multiline": False}),
            }
        }

    RETURN_TYPES = ("ASCII",)
    OUTPUT_NODE = True
    FUNCTION = "text_to_console"

    CATEGORY = "SC/Text"

    def text_to_console(self, text, label):
        print (f"\033[34m{label}\n\033[33m{text}")
        return (text, )



NODE_CLASS_MAPPINGS = {
    "One Post to GPT": OnePostGPT,
    "One GPT Builder": OneGPTBuilder,
    "Combine GPT Prompt": CombineGPTBuilder,
    "Multiple Post to GPT": MultiplePostGPT,
    "Prompt Preview": PromptPreview,
    "String to ASCII": String_TO_ASCII,
    "SCSCCLIPTextEncode": SCCLIPTextEncode,
    "Multiple Text String": Multiple_Text_String,
    "Single Text String": Single_Text_String,
    "Combine Text String": Combine_Text_String,
    "Builder Text String": Builder_Text_String,
    "SCSearch and Replace": SC_Search_and_Replace,
    "SCText to Console": SC_Text_to_Console,
}
