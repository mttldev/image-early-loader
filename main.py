import os
import yaml

class Config:
    basedir: str
    files: dict[str, list[str]]

    def __init__(self, basedir: str, files: dict[str, list[str]], **kwargs):
        self.basedir = basedir
        self.files = files

def parse(text: str) -> tuple[bool, str]:
    """
    入力されたテキストが画像表示のコマンドであるかを判定し、
    画像表示のコマンドであれば`(True, Expression)`を返す。
    画像表示のコマンドでなければ`(False, "")`を返す。
    """
    text = text.strip()
    text = text.replace('\n', '')
    if text.startswith("scene ") or text.startswith("show "):
        image_name = []
        splited_text = text.split(" ")[1:]
        if splited_text[0] == "expression":
            image_name.extend([splited_text[0], splited_text[1]])
        else:
            for t in splited_text:
                if t in ["with", "at", "as", "behind", "onlayer", "zorder"]:
                    break
                image_name.append(t)
        if image_name[-1][-1] == ":":
            image_name[-1] = image_name[-1][:-1]
        return (True, " ".join(image_name))
    else:
        return (False, "")

def load_config() -> Config:
    if os.path.isfile("config.yml"):
        with open("config.yml", "r", encoding="utf-8") as f:
            return Config(**yaml.safe_load(f))
    elif os.path.isfile("config.yaml"):
        with open("config.yaml", "r", encoding="utf-8") as f:
            return Config(**yaml.safe_load(f))
    else:
        raise FileNotFoundError("config.yml or config.yaml not found.")

def main():
    # 設定の読み込み
    config = load_config()
    # 使用画像の抽出
    result: dict[str, list[str]] = {}
    for name, files in config.files.items():
        result[name] = []
        for file in files:
            with open(os.path.join(config.basedir, file), "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                is_image_command, image_command = parse(line)
                if is_image_command:
                    if image_command not in result[name]:
                        result[name].append(image_command)
    # 結果の保存
    with open("result.yml", "w", encoding="utf-8") as f:
        yaml.dump(result, f)

if __name__ == "__main__":
    main()
