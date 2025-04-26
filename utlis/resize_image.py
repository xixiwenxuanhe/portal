import sys
from PIL import Image
import os

def resize_image(input_path, size):
    try:
        size = int(size)
        assert size in (100, 400)
    except:
        print("目标尺寸只能为100或400")
        return

    if not os.path.isfile(input_path):
        print(f"文件不存在: {input_path}")
        return

    try:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_{size}x{size}{ext}"
        
        # 检查是否为GIF文件
        if ext.lower() == '.gif':
            # 处理GIF文件
            with Image.open(input_path) as img:
                # 保存原始GIF参数
                frames = []
                durations = []
                
                # 遍历所有帧
                try:
                    for frame_num in range(0, img.n_frames):
                        img.seek(frame_num)
                        # 调整帧大小
                        new_frame = img.copy()
                        new_frame = new_frame.resize((size, size), Image.Resampling.LANCZOS)
                        frames.append(new_frame)
                        # 获取帧延迟时间
                        durations.append(img.info.get('duration', 100))
                    
                    # 保存第一帧
                    frames[0].save(
                        output_path,
                        save_all=True,
                        append_images=frames[1:],
                        duration=durations,
                        loop=img.info.get('loop', 0),
                        disposal=img.info.get('disposal', 2),
                        optimize=False
                    )
                    print(f"已保存GIF为: {output_path}")
                except Exception as e:
                    print(f"处理GIF失败: {e}")
        else:
            # 处理普通图像
            img = Image.open(input_path)
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            img.save(output_path)
            print(f"已保存为: {output_path}")
    except Exception as e:
        print(f"处理失败: {e}")

if __name__ == "__main__":
    # 自动处理imgs/01.jpg为100x100，imgs/02.jpg为400x400
    tasks = [
        # ("imgs/01.png", 100),
        # ("imgs/02.png", 400)
        ("imgs/05.jpg", 100)

    ]
    for path, size in tasks:
        print(f"处理图片: {path}，目标尺寸: {size}x{size}")
        resize_image(path, size) 