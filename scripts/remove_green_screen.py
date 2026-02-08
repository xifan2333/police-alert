#!/usr/bin/env python3
"""
绿幕抠图脚本 - 使用 Pillow，多次边缘处理
"""

from PIL import Image, ImageFilter
import numpy as np
from pathlib import Path


def remove_green_screen(input_path: str, output_path: str = None, iterations: int = 5):
    """
    移除绿幕背景，多次处理边缘
    """
    # 读取图片
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)

    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    print(f"图片尺寸: {img.size}")
    print(f"处理迭代次数: {iterations}")

    # === 多次迭代处理 ===
    # 创建累积遮罩
    total_mask = np.zeros(r.shape, dtype=bool)

    for i in range(iterations):
        print(f"迭代 {i + 1}/{iterations}...")

        # 逐渐收紧绿色检测阈值
        # 第一次宽松，后续逐渐严格
        green_threshold = 1.1 + i * 0.1  # 1.1, 1.2, 1.3, 1.4, 1.5
        min_green = 80 - i * 10  # 80, 70, 60, 50, 40
        max_rb_ratio = 0.9 - i * 0.05  # 0.9, 0.85, 0.8, 0.75, 0.7

        # 检测绿色像素
        # 条件1: 绿色通道明显高于红蓝
        is_green_dominant = (g > r * green_threshold) & (g > b * green_threshold)

        # 条件2: 绿色值足够高
        is_green_bright = g > min_green

        # 条件3: 红蓝通道相对较低
        rb_avg = (r.astype(np.float32) + b.astype(np.float32)) / 2
        is_rb_low = rb_avg < g * max_rb_ratio

        # 组合条件
        green_mask = is_green_dominant & is_green_bright & is_rb_low

        total_mask = total_mask | green_mask

    # === 边缘处理 ===
    print("处理边缘...")

    # 转换为 PIL Image 进行形态学操作
    mask_img = Image.fromarray((~total_mask * 255).astype(np.uint8))

    # 多次边缘处理
    for i in range(3):
        # 轻微模糊以平滑边缘
        mask_img = mask_img.filter(ImageFilter.MedianFilter(3))

    # 边缘锐化
    mask_img = mask_img.filter(ImageFilter.SMOOTH)

    # === 绿色溢出修复 ===
    print("修复绿色溢出...")

    result = data.copy()
    mask_array = np.array(mask_img)

    # 找到边缘区域（半透明区域）
    edge_region = (mask_array > 20) & (mask_array < 235)

    # 在边缘区域降低绿色通道
    green_excess = np.maximum(0, g.astype(np.int16) - np.maximum(r, b).astype(np.int16))

    # 修正绿色溢出
    result[:, :, 1] = np.where(
        edge_region,
        np.clip(g.astype(np.int16) - green_excess * 0.7, 0, 255).astype(np.uint8),
        g
    )

    # 应用透明度
    result[:, :, 3] = mask_array

    # 完全透明区域设为黑色
    transparent = mask_array < 10
    result[transparent, 0] = 0
    result[transparent, 1] = 0
    result[transparent, 2] = 0

    # === 保存结果 ===
    if output_path is None:
        input_p = Path(input_path)
        output_path = input_p.parent / f"{input_p.stem}_no_green.png"

    result_img = Image.fromarray(result)
    result_img.save(output_path, "PNG")
    print(f"\n完成！输出: {output_path}")

    return str(output_path)


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "frontend/public/a11.jpeg"
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    remove_green_screen(input_file, iterations=iterations)
