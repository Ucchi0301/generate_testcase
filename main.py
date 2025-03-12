import json
import uuid
import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class AIClient:
    @staticmethod
    def generate_list(prompt, count):
        formatted_prompt = f"""
        次の内容のリストを {count} 個生成し、**余計な説明を一切せず**、**そのままの リスト形式で** 出力してください。
        出力形式は **["データ1", "データ2", ...] のみ** にしてください。それ以外のテキストは不要です。
        {prompt}
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": formatted_prompt}]
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            return []

class JSONGenerator:
    def __init__(self, config):
        self.config = config
        self.count = config["count"]
        self.fields = config["fields"]
        self.ai_data = self.prepare_ai_data()

    def collect_ai_prompts(self, fields, parent_key=""):
        ai_prompts = {}
        for key, settings in fields.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            if settings["source"] == "ai":
                ai_prompts[current_key] = settings["prompt"]
            elif settings["source"] == "object":
                ai_prompts.update(self.collect_ai_prompts(settings["fields"], current_key))
        return ai_prompts

    def prepare_ai_data(self):
        ai_prompts = self.collect_ai_prompts(self.fields)
        return {key: AIClient.generate_list(prompt, self.count) for key, prompt in ai_prompts.items()}

    def generate_nested(self, fields, index, parent_key=""):
        result = {}
        for key, settings in fields.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            result[key] = self.generate_value(current_key, settings, index)
        return result

    def generate_value(self, full_key, settings, index):
        source = settings["source"]

        if source == "ai":
            return self.ai_data[full_key][index]
        elif source == "object":
            return self.generate_nested(settings["fields"], index, full_key)
        elif source == "random":
            if settings["type"] == "uuid":
                return str(uuid.uuid4())
            elif settings["type"] == "num" and "range" in settings:
                return random.randint(settings["range"][0], settings["range"][1])
            elif settings["type"] == "bool":
                return random.choice([True, False])
        elif source == "static":
            return settings["value"]

        raise ValueError(f"Unknown source type: {source}")

    def generate(self):
        return [self.generate_nested(self.fields, i) for i in range(self.count)]

def main():
    with open("input.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    generator = JSONGenerator(config)
    output = generator.generate()

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("output.json にデータを書き出しました。")

if __name__ == "__main__":
    main()