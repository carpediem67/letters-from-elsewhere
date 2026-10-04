#!/usr/bin/env python3
"""Build an offline photo journal from a reviewed editorial plan. Standard library only."""
import argparse
import base64
import html
import json
from pathlib import Path

CSS = '''
button,.download{font:inherit;border:1px solid #879e9b;background:#fbf8ee;color:#283e46;border-radius:8px;padding:10px 16px;cursor:pointer;text-decoration:none}.actions{max-width:880px;margin:20px auto;padding:16px;display:flex;gap:10px;flex-wrap:wrap}.status{width:100%;font-size:14px;white-space:pre-wrap}.exports{max-width:880px;margin:auto;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.export-card{padding:16px;background:#fbf8ee}.export-card img{height:auto}.download{display:inline-block;margin-top:10px}
*{box-sizing:border-box}body{margin:0;background:#dfded5;color:#283e46;font-family:system-ui,"PingFang SC","Microsoft YaHei",sans-serif}
nav{max-width:880px;margin:20px auto;padding:16px;display:flex;gap:14px;flex-wrap:wrap}a{color:inherit}
.page{max-width:880px;min-height:980px;margin:24px auto;padding:60px;background:#fbf8ee;box-shadow:0 8px 28px #1b303518;border-top:6px solid #879e9b;scroll-margin-top:16px}
.eyebrow,footer{font-size:12px;letter-spacing:2px;color:#657b7a}h1{font-size:48px;line-height:1.2;margin:24px 0}h2{font-size:32px;margin:18px 0}p{white-space:pre-wrap;line-height:1.85;overflow-wrap:anywhere}.intro{max-width:42em;margin-bottom:32px}
.photos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;align-items:start}.photos.count-1{grid-template-columns:1fr}.count-3 figure:first-child{grid-column:1/-1}
figure{margin:0;background:white;padding:12px 12px 16px;box-shadow:0 3px 10px #30404914;position:relative;break-inside:avoid}figure:before{content:"";position:absolute;top:-8px;left:40%;width:20%;height:18px;background:#d9bc7790}
img{width:100%;height:250px;object-fit:contain;display:block;background:#f6f5ee}.count-1 img{height:570px}.count-3 figure:first-child img{height:320px}figcaption{font-size:14px;margin-top:12px;line-height:1.6;overflow-wrap:anywhere;white-space:pre-wrap}.cover img{height:530px}.cover figure{margin-top:36px}footer{margin-top:36px;border-top:1px solid #d8dfd9;padding-top:16px}.end{min-height:360px}
@media(max-width:600px){.page{margin:12px;min-height:0;padding:26px 20px}h1{font-size:36px}h2{font-size:26px}.photos{grid-template-columns:1fr}.count-3 figure:first-child{grid-column:auto}img,.count-1 img,.count-3 figure:first-child img,.cover img{height:auto;max-height:600px}nav{margin:8px}.eyebrow{font-size:11px}}
@page{size:A4;margin:12mm}@media print{body{background:white}nav,.actions,.exports{display:none}.page{max-width:none;min-height:0;margin:0;padding:14mm 8mm;box-shadow:none;break-before:page}.page:first-of-type{break-before:auto}h1{font-size:32px}h2{font-size:24px}.intro{margin-bottom:20px}img{height:52mm}.count-1 img,.cover img{height:145mm}.count-3 figure:first-child img{height:70mm}footer{margin-top:20px}.photos{gap:18px}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''

SCRIPT = r'''
const status = document.querySelector('.status');
document.querySelector('#share').onclick = async () => {
  const url = new URL(location.href); url.hash = '';
  if (!/^https?:$/.test(url.protocol) || ['localhost','127.0.0.1','[::1]'].includes(url.hostname)) {
    status.textContent = '这是本地预览。将手帐发布到你选择的静态网站后，才能分享在线链接；现在可以导出图片分享。'; return;
  }
  try {
    if (navigator.share) await navigator.share({title:document.title,url:url.href});
    else if (navigator.clipboard) {await navigator.clipboard.writeText(url.href); status.textContent='链接已复制，可以粘贴给朋友。';}
    else status.textContent='复制此链接分享：'+url.href;
  } catch(e) {status.textContent=e.name==='AbortError'?'已取消分享。':'请手动复制链接：'+url.href;}
};
function lines(ctx,text,x,y,width,lineHeight,maxLines) {
  let line='', rows=[];
  for(const char of text) {
    if(char==='\n') {rows.push(line);line='';continue;}
    if(ctx.measureText(line+char).width>width) {rows.push(line);line=char;} else line+=char;
  }
  if(line)rows.push(line);
  if(rows.length>maxLines)throw Error('文字过长，请缩短标题、正文或图注后再导出，避免内容被裁切。');
  rows.forEach((row,i)=>ctx.fillText(row,x,y+i*lineHeight));
}
async function card(section,index) {
  await document.fonts.ready;
  const canvas=document.createElement('canvas');canvas.width=1080;canvas.height=1440;
  const ctx=canvas.getContext('2d');
  ctx.fillStyle='#fbf8ee';ctx.fillRect(0,0,1080,1440);
  ctx.fillStyle='#879e9b';ctx.fillRect(64,66,64,6);
  ctx.fillStyle='#657b7a';ctx.font='22px sans-serif';ctx.fillText('旅 行 手 帐',64,114);
  ctx.fillStyle='#283e46';ctx.font='bold 48px sans-serif';
  lines(ctx,section.querySelector('h1,h2').textContent,64,195,952,60,2);
  ctx.font='26px sans-serif';
  lines(ctx,section.querySelector('p')?.textContent||'',64,328,952,40,4);
  const figures=[...section.querySelectorAll('figure')];
  const count=figures.length;
  for(let i=0;i<count;i++) {
    const source=figures[i].querySelector('img'); await source.decode();
    const cols=count===1?1:2, rows=Math.ceil(count/cols);
    const w=(952-(cols-1)*24)/cols,h=(794-(rows-1)*26)/rows;
    const x=64+(i%cols)*(w+24),y=510+Math.floor(i/cols)*(h+26);
    ctx.fillStyle='#ffffff';ctx.fillRect(x,y,w,h);
    const caption=figures[i].querySelector('figcaption').textContent;
    const available=h-(caption?94:32), scale=Math.min((w-24)/source.naturalWidth,available/source.naturalHeight);
    const dw=source.naturalWidth*scale,dh=source.naturalHeight*scale;
    ctx.drawImage(source,x+(w-dw)/2,y+12+(available-dh)/2,dw,dh);
    ctx.fillStyle='#283e46';ctx.font='22px sans-serif';
    if(caption)lines(ctx,caption,x+16,y+h-58,w-32,28,2);
  }
  ctx.fillStyle='#657b7a';ctx.font='20px sans-serif';ctx.fillText(String(index+1).padStart(2,'0'),64,1380);
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));
  if(!blob)throw Error('浏览器未能生成图片，请换用系统浏览器重试。');
  return {blob,name:`travel-journal-${String(index+1).padStart(2,'0')}.png`};
}
let exportUrls=[];
async function zipCards(files) {
  const encoder=new TextEncoder(),chunks=[],central=[];let offset=0;
  const table=Uint32Array.from({length:256},(_,n)=>{let c=n;for(let k=0;k<8;k++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;return c>>>0;});
  const u16=(v,o,n)=>v.setUint16(o,n,true),u32=(v,o,n)=>v.setUint32(o,n,true);
  for(const file of files){
    const bytes=new Uint8Array(await file.blob.arrayBuffer()),name=encoder.encode(file.name);
    let crc=0xffffffff;for(const b of bytes)crc=table[(crc^b)&255]^(crc>>>8);crc=(crc^0xffffffff)>>>0;
    const head=new Uint8Array(30+name.length),h=new DataView(head.buffer);
    u32(h,0,0x04034b50);u16(h,4,20);u16(h,6,0x800);u16(h,12,33);u32(h,14,crc);u32(h,18,bytes.length);u32(h,22,bytes.length);u16(h,26,name.length);head.set(name,30);
    const dir=new Uint8Array(46+name.length),d=new DataView(dir.buffer);
    u32(d,0,0x02014b50);u16(d,4,20);u16(d,6,20);u16(d,8,0x800);u16(d,14,33);u32(d,16,crc);u32(d,20,bytes.length);u32(d,24,bytes.length);u16(d,28,name.length);u32(d,42,offset);dir.set(name,46);
    chunks.push(head,bytes);central.push(dir);offset+=head.length+bytes.length;
  }
  const length=central.reduce((sum,c)=>sum+c.length,0),end=new Uint8Array(22),v=new DataView(end.buffer);
  u32(v,0,0x06054b50);u16(v,8,files.length);u16(v,10,files.length);u32(v,12,length);u32(v,16,offset);
  return new Blob([...chunks,...central,end],{type:'application/zip'});
}
async function exportCards(mode) {
  const button=document.querySelector(mode==='cover'?'#export-cover':'#export-all');button.disabled=true;
  try {
    const sections=[...document.querySelectorAll('.page:not(.end)')];
    const selected=mode==='cover'?sections.slice(0,1):sections;
    status.textContent='正在生成 1080 × 1440 图片…';
    const results=[];
    for(let i=0;i<selected.length;i++)results.push(await card(selected[i],i));
    exportUrls.forEach(URL.revokeObjectURL);exportUrls=[];
    const gallery=document.querySelector('.exports');gallery.replaceChildren();
    if(results.length>1){
      const zip=await zipCards(results),url=URL.createObjectURL(zip);exportUrls.push(url);
      const bundle=document.createElement('a');bundle.id='download-bundle';bundle.className='download';
      bundle.style.gridColumn='1 / -1';bundle.style.textAlign='center';bundle.href=url;bundle.download='travel-journal-images.zip';
      bundle.textContent=`下载整套 ZIP（${results.length} 张图片）`;gallery.append(bundle);
    }
    for(const result of results) {
      const url=URL.createObjectURL(result.blob);exportUrls.push(url);
      const item=document.createElement('div');item.className='export-card';
      const img=new Image();img.src=url;img.alt=result.name;
      const link=document.createElement('a');link.href=url;link.download=result.name;link.className='download';link.textContent='保存 '+result.name;
      item.append(img,link);gallery.append(item);
    }
    status.textContent=`已生成 ${results.length} 张 3:4 图片。可整套下载 ZIP、逐张保存，或在手机上长按图片保存，再发微信或小红书。若内置浏览器不支持保存，请用系统浏览器打开。`;
    gallery.scrollIntoView({behavior:'smooth'});
  } catch(e) {status.textContent='导出未完成：'+e.message;}
  finally {button.disabled=false;}
}
document.querySelector('#export-cover').onclick=()=>exportCards('cover');
document.querySelector('#export-all').onclick=()=>exportCards('all');
'''


def build(manifest_path, plan_path, output):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    if output.exists():
        raise ValueError('输出文件已存在，请指定新文件名')
    records = {p['id']: p for p in manifest['photos']}
    root = manifest_path.resolve().parent
    escape = lambda value: html.escape(str(value), quote=True)
    used = set()

    def figure(photo_id, caption=''):
        record = records.get(photo_id)
        if not record or record['status'] == 'error':
            raise ValueError(f'照片不可用: {photo_id}')
        photo = (root / record['photo']).resolve()
        if root not in photo.parents or photo.suffix.lower() != '.jpg':
            raise ValueError('照片必须是清单目录内的 JPEG 阅读副本')
        encoded = base64.b64encode(photo.read_bytes()).decode('ascii')
        used.add(photo_id)
        return (f'<figure><img src="data:image/jpeg;base64,{encoded}" alt="{escape(caption or photo_id)}">'
                f'<figcaption>{escape(caption)}</figcaption></figure>')

    pages = plan.get('pages', [])
    if not pages or not str(plan.get('title', '')).strip():
        raise ValueError('需要手帐标题和至少一个内容页')
    cover = figure(plan['cover_photo_id']) if plan.get('cover_photo_id') else ''
    sections = [f'<section class="page cover" id="cover"><div class="eyebrow">旅行手帐</div>'
                f'<h1>{escape(plan["title"])}</h1><p>{escape(plan.get("subtitle", ""))}</p>{cover}</section>']
    navigation = ['<a href="#cover">封面</a>']
    for index, page in enumerate(pages, 1):
        photos = page.get('photos', [])
        if not 1 <= len(photos) <= 4:
            raise ValueError(f'第 {index} 页应包含 1–4 张照片')
        title = escape(page.get('title', f'旅途片刻 {index}'))
        figures = ''.join(figure(p['id'], p.get('caption', '')) for p in photos)
        sections.append(f'<section class="page" id="page-{index}"><div class="eyebrow">沿途记录 · {index:02}</div>'
                        f'<h2>{title}</h2><p class="intro">{escape(page.get("text", ""))}</p>'
                        f'<div class="photos count-{len(photos)}">{figures}</div>'
                        f'<footer>{index:02} / {len(pages):02}</footer></section>')
        navigation.append(f'<a href="#page-{index}">{index:02} {title}</a>')
    sections.append('<section class="page end"><div class="eyebrow">留在纸上的旅程</div>'
                    '<h2>把这些片刻收好</h2><p>留一点空白，给下一次出发。</p></section>')
    actions = ('<div class="actions"><button id="share">分享整本手帐</button>'
               '<button id="export-cover">生成分享封面</button><button id="export-all">生成整套分享图片</button>'
               '<div class="status" role="status" aria-live="polite">把旅途做成一本，也把喜欢的几页分享出去。</div></div><div class="exports"></div>')
    document = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>{escape(plan["title"])}</title><style>{CSS}</style></head><body>'
                f'{actions}<nav aria-label="手帐目录">{"".join(navigation)}</nav>{"".join(sections)}'
                f'<script>{SCRIPT}</script></body></html>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding='utf-8')
    print(json.dumps({'output': str(output), 'content_pages': len(pages), 'sections': len(sections),
                      'selected_photo_ids': len(used), 'bytes': output.stat().st_size}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('plan', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    build(args.manifest, args.plan, args.output)
