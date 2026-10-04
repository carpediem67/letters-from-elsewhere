// 将示例排版源稿原生渲染为 PNG。需要已安装 Playwright Chromium。
const {chromium}=require('playwright');
const path=require('path');
const fs=require('fs');
const {pathToFileURL}=require('url');
(async()=>{
 const source=path.join(__dirname,'source','composition.html');
 const output=path.join(__dirname,'..','..','docs','pages');
 fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.LETTERS_BROWSER_CHANNEL?{channel:process.env.LETTERS_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1200,height:1000},deviceScaleFactor:2});
  await page.goto(pathToFileURL(source).href);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all(Array.from(document.images).map(im=>im.decode()));});
  const count=await page.locator('.page').count();
  for(let i=1;i<=count;i++)await page.locator('#p'+i).screenshot({path:path.join(output,String(i).padStart(2,'0')+'.png')});
  console.log(`${count} pages exported at 1200 × 1600`);
 }finally{await browser.close();}
})().catch(error=>{console.error(error.message);process.exitCode=1;});
