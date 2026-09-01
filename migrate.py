"""محرك ترحيل الـ imports من pyrogram إلى compat.

يحافظ على كل الكود ما عدا سطور الاستيراد. يُستخدم مرة واحدة على
نسخة العمل (bot_migrated/plugins)."""

import os
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "."
DRY = "--dry" in sys.argv


IMPORT_REPLACEMENTS = [
    (r"^from pyrogram\.raw\.functions\.users import GetFullUser\s*$",
     "from compat import GetFullUser  # MTProto stub (raises NotImplementedError)"),
    (r"^from pyrogram\.raw\.functions\.channels import GetFullChannel\s*$",
     "from compat import GetFullChannel  # MTProto stub"),
    (r"^from pyrogram\.raw\.functions\.messages import GetStickerSet\s*$",
     "from compat import GetStickerSet  # MTProto stub (use bot.get_sticker_set)"),
    (r"^from pyrogram\.raw\.functions\.stickers import CreateStickerSet\s*$",
     "from compat import CreateStickerSet  # MTProto stub (use bot.create_new_sticker_set)"),
    (r"^from pyrogram\.file_id import FileId, FileType, ThumbnailSource\s*$",
     "from compat import FileId, FileType, ThumbnailSource  # MTProto stubs"),
    (r"^from pyrogram\.errors import \*\s*$",
     "from compat import *"),
    (r"^from pyrogram\.errors import (.+)\s*$",
     lambda m: "from compat import " + m.group(1)),
    (r"^from pyrogram\.enums import \*\s*$",
     "from compat import *"),
    (r"^from pyrogram\.enums import (.+)\s*$",
     lambda m: "from compat import " + m.group(1)),
    (r"^from pyrogram\.types import \*\s*$",
     "from compat import *"),
    (r"^from pyrogram\.types import (.+)\s*$",
     lambda m: "from compat import " + m.group(1)),
    (r"^from pyrogram\.handlers import (.+)\s*$",
     lambda m: "from compat import " + m.group(1)),
    (r"^from pyrogram import \*\s*$",
     "from compat import *"),
    (r"^from pyrogram import (.+)\s*$",
     lambda m: "from compat import " + m.group(1)),
    (r"^import pyrogram\.raw\.types\s*$",
     "from compat import raw  # MTProto stub"),
    (r"^import pyrogram\s*$",
     "import compat as pyrogram  # compat shim"),
]

RAW_TYPES_IMPORT_START = re.compile(r"^from pyrogram\.raw\.types import \(\s*$")


def transform_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return line
    for pattern, repl in IMPORT_REPLACEMENTS:
        if isinstance(repl, str):
            if re.match(pattern, line):
                return repl + "\n"
        else:
            m = re.match(pattern, line)
            if m:
                return repl(m) + "\n"
    return line


def transform_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    changed = False
    out = []
    i = 0
    in_raw_types_block = False
    while i < len(lines):
        line = lines[i]

        if RAW_TYPES_IMPORT_START.match(line.strip()):
            in_raw_types_block = True
            changed = True
            while i < len(lines):
                if ")" in lines[i]:
                    i += 1
                    break
                i += 1
            out.append("from compat import raw  # MTProto types stub (raw.types.*)\n")
            continue

        new_line = transform_line(line)
        if new_line != line:
            changed = True
        out.append(new_line)
        i += 1

    if changed and not DRY:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
    return changed


def main():
    total = 0
    changed_files = []
    for root, dirs, files in os.walk(SRC):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)
            try:
                if transform_file(path):
                    total += 1
                    changed_files.append(path)
            except Exception as e:
                print(f"ERROR {path}: {e}")
    print(f"\n[+] Files changed: {total}")
    for p in changed_files:
        print(f"    - {p}")
    if DRY:
        print("\n[DRY RUN — لم يتم تعديل أي ملف]")


if __name__ == "__main__":
    main()
