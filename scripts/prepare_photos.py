#!/usr/bin/env python3
"""Create read-only-source photo inventory and numbered contact sheets. Requires Pillow."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif', '.avif', '.bmp'}


def prepare(source, output):
    source, output = source.resolve(), output.resolve()
    if not source.is_dir():
        raise ValueError('照片目录不存在')
    if output == source or source in output.parents:
        raise ValueError('输出目录必须位于照片目录之外')
    if output.exists():
        raise ValueError('输出目录已存在，请使用新的目录，避免覆盖')
    files = sorted(p for p in source.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONS)
    if not files:
        raise ValueError('没有找到支持的照片文件')
    (output / 'photos').mkdir(parents=True)
    (output / 'contacts').mkdir()
    records, seen = [], {}
    for index, path in enumerate(files, 1):
        record = {'id': f'P{index:04}', 'source': str(path), 'status': 'error'}
        try:
            with path.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            record['sha256'] = digest
            if digest in seen:
                original = seen[digest]
                record.update(status='duplicate', duplicate_of=original['id'],
                              photo=original['photo'], captured_at=original['captured_at'],
                              width=original['width'], height=original['height'])
            else:
                with Image.open(path) as raw:
                    exif = raw.getexif()
                    try:
                        captured = exif.get_ifd(34665).get(36867) or exif.get(36867)
                    except (KeyError, TypeError, ValueError):
                        captured = exif.get(36867)
                    picture = ImageOps.exif_transpose(raw)
                    width, height = picture.size
                    picture.thumbnail((2000, 2000))
                    rgba = picture.convert('RGBA')
                    flat = Image.new('RGB', rgba.size, 'white')
                    flat.paste(rgba, mask=rgba.getchannel('A'))
                    relative = f"photos/{record['id']}.jpg"
                    flat.save(output / relative, quality=88)
                record.update(status='ready', photo=relative, width=width, height=height,
                              captured_at=str(captured) if captured else None)
                seen[digest] = record
        except (OSError, ValueError, Image.DecompressionBombError) as exc:
            record['error'] = str(exc)
        records.append(record)
    usable = [r for r in records if r['status'] != 'error']
    contacts = []
    for start in range(0, len(usable), 20):
        batch = usable[start:start + 20]
        sheet = Image.new('RGB', (1200, ((len(batch) + 3) // 4) * 240), '#f5f2e9')
        draw = ImageDraw.Draw(sheet)
        for i, record in enumerate(batch):
            x, y = (i % 4) * 300, (i // 4) * 240
            with Image.open(output / record['photo']) as picture:
                picture.thumbnail((280, 200))
                sheet.paste(picture, (x + (300 - picture.width) // 2, y + 8))
            label = record['id']
            if record['status'] == 'duplicate':
                label += f" = {record['duplicate_of']}"
            draw.text((x + 12, y + 215), label, fill='#183b50')
        name = f'contacts/sheet-{start // 20 + 1:02}.jpg'
        sheet.save(output / name, quality=90)
        contacts.append(name)
    summary = {state: sum(r['status'] == state for r in records)
               for state in ('ready', 'duplicate', 'error')}
    manifest = {'version': 1, 'total': len(records), 'summary': summary,
                'contacts': contacts, 'photos': records}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(output), 'total': len(records), **summary}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    prepare(args.source, args.output)
