#!/usr/bin/env python3
"""从已审阅的整页 PNG 构建纸本翻阅器；阅读与下载使用相同字节。"""
import argparse
import base64
import html
import json
import zipfile
from pathlib import Path

TEMPLATE = r'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title><style>
*{box-sizing:border-box}body{margin:0;color:#f1eadb;background:radial-gradient(ellipse at 50% 28%,#48506a,#202737 80%);font:14px -apple-system,BlinkMacSystemFont,sans-serif;min-height:100svh}header{display:flex;justify-content:space-between;align-items:center;max-width:1300px;margin:auto;padding:22px 28px}h1{font-size:18px;font-weight:500;letter-spacing:3px;margin:0}header small{color:#bbbfc8}.stage{display:flex;align-items:center;justify-content:center;padding:18px 25px 24px;min-height:65vh}.book{position:relative;display:flex;box-shadow:0 20px 55px #050b2280;max-width:100%;border-radius:8px;background:#c3b69e;isolation:isolate}.book:before,.book:after{content:'';position:absolute;inset:6px -8px -5px;background:#d7cbb7;border-radius:8px;z-index:-1;transform:rotate(-1deg)}.book:after{inset:11px -14px -9px;background:#998d79;transform:rotate(1deg);z-index:-2}.leaf{display:block;width:min(42vw,calc((100svh - 230px)*.75));aspect-ratio:3/4;object-fit:contain;background:#e6dcc5}.left{border-radius:7px 0 0 7px}.right{border-radius:0 7px 7px 0}.book.single .right,.book.single .seam{display:none}.book.single .left{border-radius:7px}.seam{position:absolute;left:50%;top:0;bottom:0;width:22px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,#342b2629,transparent);pointer-events:none}nav,.actions{display:flex;gap:15px;justify-content:center;align-items:center;margin:8px auto 20px}button,a{font:inherit;cursor:pointer;color:inherit;background:#ffffff0c;border:1px solid #ffffff32;border-radius:25px;padding:11px 19px;text-decoration:none}button:hover,a:hover{background:#ffffff1c}button:disabled{opacity:.3;cursor:default}#status{min-width:90px;text-align:center;color:#d6d6de}footer{text-align:center;color:#b6bac6;font-size:12px;padding:0 20px 24px}#message{min-height:18px;text-align:center;color:#edd5a3;font-size:13px}.actions{flex-wrap:wrap;margin-bottom:12px}@media(max-width:640px){header{padding:22px 20px}header small{display:none}.stage{padding:12px 22px 20px;min-height:0}.leaf{width:min(calc(100vw - 44px),calc((100svh - 235px)*.75));border-radius:5px}.right,.seam{display:none}.actions{gap:8px}button,a{padding:10px 13px;font-size:13px}h1{font-size:16px}}
</style><body><header><h1>__TITLE__</h1><small>一段旅程 · 几页小纸片</small></header><main><section class="stage" aria-label="手帐翻阅"><div class="book"><img class="leaf left" id="left"><img class="leaf right" id="right"><div class="seam"></div></div></section><nav><button id="prev" aria-label="上一页">← 前页</button><span id="status" aria-live="polite"></span><button id="next" aria-label="下一页">后页 →</button></nav><div class="actions"><a id="save" download>保存当前页</a><a id="all" download="__ZIP_NAME__" href="__ZIP_FALLBACK__">下载整本图片</a><button id="share">分享这本手帐</button></div><p id="message" aria-live="polite"></p></main><footer>左右滑动或使用方向键翻阅 · 手机可长按图片保存</footer><script>
const pages=__PAGES__;let index=0;const $=id=>document.getElementById(id);const mobile=()=>matchMedia('(max-width:640px)').matches;const step=()=>mobile()?1:2;
function render(){if(!mobile())index-=index%2;const a=pages[index],b=pages[index+1];$('left').src=a.src;$('left').alt='第 '+(index+1)+' 页手帐';$('right').src=(b||a).src;$('right').alt=b?'第 '+(index+2)+' 页手帐':'';$('right').style.visibility=b?'visible':'hidden';document.querySelector('.book').classList.toggle('single',!b);$('status').textContent=(index+1)+(!mobile()&&b?'–'+(index+2):'')+' / '+pages.length;$('prev').disabled=index===0;$('next').disabled=index+step()>=pages.length;$('save').href=a.src;$('save').download=a.name;$('save').textContent='保存第 '+(index+1)+' 页';}
function turn(d){index=Math.max(0,Math.min(pages.length-1,index+d*step()));render()}
$('prev').onclick=()=>turn(-1);$('next').onclick=()=>turn(1);addEventListener('keydown',e=>{if(e.key==='ArrowRight')turn(1);if(e.key==='ArrowLeft')turn(-1)});addEventListener('resize',render);let sx;document.querySelector('.book').addEventListener('touchstart',e=>sx=e.changedTouches[0].clientX,{passive:true});document.querySelector('.book').addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>45)turn(dx<0?1:-1)},{passive:true});$('share').onclick=async()=>{if(location.protocol==='file:'||['localhost','127.0.0.1','::1'].includes(location.hostname)){$('message').textContent='当前是本地预览。公开部署此 HTML 后即可分享网址；现在可下载图片分享。';return}try{if(navigator.share)await navigator.share({title:document.title,url:location.href});else{await navigator.clipboard.writeText(location.href);$('message').textContent='手帐网址已复制'}}catch(e){if(e.name!=='AbortError')$('message').textContent='请复制浏览器地址分享'}};render();

// ZIP_STORED：直接使用阅读中的 PNG 字节，没有重新绘制或降低画质。
const bookCrcTable=new Uint32Array(256);
for(let i=0;i<256;i++){let c=i;for(let j=0;j<8;j++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;bookCrcTable[i]=c>>>0;}
function bookCrc(bytes){let c=0xffffffff;for(const b of bytes)c=bookCrcTable[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
async function bookZip(){
 const entries=await Promise.all(pages.map(async p=>{
  let bytes;
  if(p.src.startsWith('data:')){const raw=atob(p.src.split(',')[1]);bytes=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);}
  else{const response=await fetch(p.src);if(!response.ok)throw new Error('Page download failed');bytes=new Uint8Array(await response.arrayBuffer());}
  return {name:new TextEncoder().encode(p.name),bytes,crc:bookCrc(bytes)};
 }));
 let offset=0;const local=[],central=[];
 for(const e of entries){
  const flags=e.name.some(b=>b>127)?0x800:0;
  const h=new Uint8Array(30+e.name.length),v=new DataView(h.buffer);
  v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,flags,true);v.setUint16(12,33,true);v.setUint32(14,e.crc,true);v.setUint32(18,e.bytes.length,true);v.setUint32(22,e.bytes.length,true);v.setUint16(26,e.name.length,true);h.set(e.name,30);
  const c=new Uint8Array(46+e.name.length),d=new DataView(c.buffer);
  d.setUint32(0,0x02014b50,true);d.setUint16(4,788,true);d.setUint16(6,20,true);d.setUint16(8,flags,true);d.setUint16(14,33,true);d.setUint32(16,e.crc,true);d.setUint32(20,e.bytes.length,true);d.setUint32(24,e.bytes.length,true);d.setUint16(28,e.name.length,true);d.setUint32(38,0x1800000,true);d.setUint32(42,offset,true);c.set(e.name,46);
  local.push(h,e.bytes);central.push(c);offset+=h.length+e.bytes.length;
 }
 const end=new Uint8Array(22),v=new DataView(end.buffer),size=central.reduce((n,c)=>n+c.length,0);
 v.setUint32(0,0x06054b50,true);v.setUint16(8,entries.length,true);v.setUint16(10,entries.length,true);v.setUint32(12,size,true);v.setUint32(16,offset,true);
 return new Blob([...local,...central,end],{type:'application/zip'});
}
$('all').onclick=async e=>{e.preventDefault();const link=$('all');link.textContent='正在打包…';try{await new Promise(resolve=>requestAnimationFrame(resolve));const url=URL.createObjectURL(await bookZip()),a=document.createElement('a');a.href=url;a.download=link.download;a.click();setTimeout(()=>URL.revokeObjectURL(url),60000);}catch(err){$('message').textContent='打包失败，请逐页保存图片。';}finally{link.textContent='下载整本图片';}};
</script></body></html>'''

CREDITS_CSS = '.credits{max-width:750px;margin:0 auto;padding:0 24px 32px;color:#b6bac6;font-size:12px;line-height:1.8}.credits>span{display:block;text-align:center;letter-spacing:1px}.credits details{margin:12px auto 0}.credits summary{cursor:pointer;text-align:center}.credits a{padding:0;border:0;border-radius:0;background:none;text-decoration:underline;text-underline-offset:3px}.credits a:hover{background:none;color:#f1eadb}.credits ol{padding-left:23px}.credits li{margin:5px 0}button:focus-visible,a:focus-visible,summary:focus-visible{outline:2px solid #e4d1a1;outline-offset:4px}'

def credits_markup(path):
    if path is None:
        return ""
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for record in data.get("photos", []):
        url = record["source"]
        if not url.startswith("https://"):
            raise ValueError("素材来源必须是 HTTPS 详情页")
        rows.append('<li><a href="' + html.escape(url, quote=True) +
                    '" target="_blank" rel="noopener noreferrer">' +
                    html.escape(record["title"]) + '</a> · ' +
                    html.escape(record["author"]) + '</li>')
    return ('<div class="credits"><span>旅行手帐·Letters from Elsewhere</span>'
            '<details><summary>素材来源与说明</summary><p>' +
            html.escape(data.get("summary", "")) + '</p><p>' +
            html.escape(data.get("font_note", "")) +
            '</p><p>素材许可见本示例的来源说明，与项目代码 MIT License 分开适用。</p><ol>' +
            ''.join(rows) + '</ol></details></div>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", type=Path, help="按页序命名的 PNG 文件夹，例如 01.png")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title", default="旅途剪贴簿")
    parser.add_argument("--linked-pages", help="静态网站页图的相对路径；默认内嵌全部 PNG")
    parser.add_argument("--zip-name", help="整本下载的文件名")
    parser.add_argument("--credits", type=Path, help="可选的公开素材说明 JSON")
    args = parser.parse_args()
    files = sorted(args.pages.glob("*.png"))
    if not files:
        parser.error("需要已排版并审阅的 PNG 页面")
    pages = [{"name": f.name, "src": (args.linked_pages.rstrip("/") + "/" + f.name
                       if args.linked_pages else "data:image/png;base64," +
                       base64.b64encode(f.read_bytes()).decode("ascii"))} for f in files]
    zip_path = args.output.with_suffix(".pages.zip")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # 固定元数据，原生浏览器 ZIP 与此文件的内容及页序一致。
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as archive:
        for file in files:
            info = zipfile.ZipInfo(file.name, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0x1800000
            archive.writestr(info, file.read_bytes())
    page_json = json.dumps(pages, ensure_ascii=False).replace("<", "\\u003c")
    result = TEMPLATE.replace("__TITLE__", html.escape(args.title))
    result = result.replace("__PAGES__", page_json)
    result = result.replace("__ZIP_NAME__", html.escape(args.zip_name or zip_path.name, quote=True))
    result = result.replace("__ZIP_FALLBACK__", html.escape(zip_path.name, quote=True))
    credits = credits_markup(args.credits)
    if credits:
        result = result.replace("</footer>", "</footer>" + credits, 1)
        result = result.replace("</style>", CREDITS_CSS + "</style>", 1)
    args.output.write_text(result, encoding="utf-8")
    print(f"{len(files)} 页：{args.output}；整本 PNG：{zip_path}")


if __name__ == "__main__":
    main()
