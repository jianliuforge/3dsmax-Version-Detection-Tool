from pathlib import Path
import olefile
import re
import sys

# ====================== 配置 ======================
MAX_FILE_PATH = r"C:\Users\Administrator\Desktop\新建文件夹 (2)\2021-2019.max"

# 你后续程序支持的最高主版本号
# 23 = 2021    26 = 2024
TARGET_MAJOR = 23
# ================================================

def check_max_version_strict(file_path):
    try:
        if not olefile.isOleFile(file_path):
            print("拒绝")
            sys.exit(1)

        ole = olefile.OleFileIO(str(file_path))
        data = b''

        for stream in ole.listdir():
            try:
                with ole.openstream(stream) as s:
                    data += s.read(65536)
            except:
                continue
        ole.close()

        # 尝试多种编码方式解码
        text = ''
        for encoding in ['utf-8', 'utf-16-le', 'gbk', 'ascii']:
            try:
                text += data.decode(encoding, errors='ignore')
            except:
                continue
        
        text_lower = text.lower()

        # 检测主版本
        main_version_match = re.search(r'3ds Max 版本[:\s]*(\d{2})', text)
        if not main_version_match:
            # 备用方案：查找版本号格式
            main_version_match = re.search(r'(\d{2})\.\d{2}', text_lower)
        
        main_version = int(main_version_match.group(1)) if main_version_match else None
        
        # 检测另存为版本
        saved_as_match = re.search(r'另存为版本[:\s]*(\d{2})', text)
        saved_as_version = int(saved_as_match.group(1)) if saved_as_match else None
        
        # 优先使用另存为版本来判断兼容性，如果没有则使用主版本
        version_to_check = saved_as_version if saved_as_version is not None else main_version

        if version_to_check is None:
            print("通过")   # 无法确定时保守通过
            return "通过"

        status = "通过" if version_to_check <= TARGET_MAJOR else "拒绝"
        
        print(f"检测到主版本: {main_version if main_version else '未知'} | 另存为版本: {saved_as_version if saved_as_version else '未知'} | 判断依据: {version_to_check}")
        print(status)
        
        if status == "拒绝":
            sys.exit(1)
        return status

    except Exception as e:
        print("拒绝")
        sys.exit(1)


if __name__ == "__main__":
    check_max_version_strict(MAX_FILE_PATH)