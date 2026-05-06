from pathlib import Path
import olefile
import re
import sys

# ====================== 配置 ======================
MAX_FILE_PATH = "2.max"

# 顶点数限制（100万）三角面范围≈1.5-2倍 根据门槛设置最大顶点数 这个订顶点数是整个文件的
TARGET_VERTICES = 1000000
# ================================================

def check_vertices(file_path):
    try:
        if not olefile.isOleFile(file_path):
            print("拒绝")
            sys.exit(1)

        ole = olefile.OleFileIO(str(file_path))
        data = b''

        for stream in ole.listdir():
            try:
                with ole.openstream(stream) as s:
                    data += s.read()
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

        # 匹配顶点数
        patterns = [
            r'(?:vertices|verts|顶点)[:\s]*[=]?\s*(\d+)',
            r'numverts[:\s]*[=]?\s*(\d+)',
        ]
        
        vertices = None
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                vertices = max(int(m) for m in matches)
                break

        if vertices is None:
            print("通过")  # 无法确定时保守通过
            return "通过"

        status = "通过" if vertices <= TARGET_VERTICES else "拒绝"
        
        print(f"检测到顶点数: {vertices:,}")
        print(status)
        
        if status == "拒绝":
            sys.exit(1)
        return status

    except Exception as e:
        print("拒绝")
        sys.exit(1)


if __name__ == "__main__":
    check_vertices(MAX_FILE_PATH)
