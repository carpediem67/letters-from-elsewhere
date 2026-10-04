# 雨天散步：文字输入演示

本例为虚构场景，用于检查贴纸页布局，不代表真实出行记录。

用户输入：做一张雨天旅行手帐贴纸，记得青石板、蓝雨伞、桂花糕和坐在窗边喝茶。无字，彩铅加剪纸风。

生成方式：Codex 内置 image_gen，无参考照片。

提示词：

Create a portrait 2:3 travel journal sticker sheet on a pure white background. Exactly seven separate die-cut paper stickers, comfortably spaced with no touching or overlapping and generous outer margins. A refined handmade cut-paper and colored-pencil illustration style, visible delicate pencil grain, warm ivory paper inside each sticker, flat color blocks, restrained ink-blue, muted sage, warm ochre and stone-gray palette. No text, letters, numbers, logos, watermarks or fake checkerboard transparency. Flat front-facing artwork, not a photograph of a desk or stationery mockup.

Seven motifs: (1) the largest sticker, a quiet rain-wet stone alley with simple anonymous house facades and reflections, no identifiable landmark and no people; (2) a single open blue umbrella, complete handle; (3) a small plate with three golden osmanthus cakes; (4) a wooden window frame and one warm cup of tea on its sill, contained together in one silhouette; (5) a small patch of blue-gray paving stones with concentric raindrop ripples; (6) a charming understated paper-cut rain cloud with drops, all contained in one continuous cut border; (7) one small golden osmanthus blossom branch. Use varied sizes, the alley about twice the size of the smaller motifs, balanced staggered rows rather than uniform boxes. Each motif has a continuous closed ivory-white die-cut border with a fine subtle gray outer contour so the cut edge is visible on white. Every sticker fully within the canvas, at least 5% outer margin, generous white gaps. All textures contained inside sticker silhouettes; no background shadows or decorative filler between stickers. Overall feeling: a gentle rainy afternoon saved as tangible little paper memories.

## 一次修正

首版背景出现灰色渐变和阴影。以首版作为编辑目标，使用以下提示词生成当前样例：

Edit this travel sticker sheet. Preserve the seven existing sticker illustrations, all their subjects, shapes, colors, pencil texture and arrangement. Change ONLY the sheet background and spacing: every pixel outside the seven closed sticker silhouettes must be flat pure white (#FFFFFF), absolutely no gray, gradient, vignette, ambient occlusion, drop shadows, desk texture, lighting or photographic treatment. Slightly shrink the entire arrangement uniformly within the same portrait canvas to ensure at least 5% pure white outer margin on ALL sides. Keep the ivory paper die-cut borders and a very fine light-gray outline that makes each edge visible against pure white. Do not add text or new motifs. This must look like a flat printable digital sheet, not a physical product photograph.

## 验证范围

- Skill 格式校验通过。
- 文字输入出图及单次编辑已实测；目视确认七枚贴纸分离、轮廓完整、无文字，背景阴影已消除。生成模型并未严格保持所有细小纹理，示例不代表像素级编辑能力。
- 当前图像为 1024 × 1536 像素，按 300 DPI 对应约 86.7 × 130.0 毫米；不宣称 A5 300 DPI 印刷成品。
- 本次没有实测照片人物保真、中文标签、透明 alpha 或实体打印；这些能力需要针对实际素材继续验证。
