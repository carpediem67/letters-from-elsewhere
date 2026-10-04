"""纸页先行：15 张原摄影、15 页手作剪贴簿、七个跨页与独立收尾；与阅读器使用同一导出。"""
from pathlib import Path
import html, json, random

B=Path(__file__).resolve().parent
records=json.loads((B.parent/'sources.json').read_text())
sources={r['key']:r for r in records}
usage={k:[] for k in sources}
pages=[]
page_number=1

def pos(x,y,w,h=None,r=0):
 return f'left:{x}px;top:{y}px;width:{w}px;'+(f'height:{h}px;' if h is not None else '')+f'transform:rotate({r}deg);'

def photo(k,x,y,w,h,r=0,cls='',focus='50% 50%',reason='场景留影'):
 usage[k].append({'page':page_number,'role':reason,'type':'photograph'})
 return f'<figure class="photo {cls}" style="{pos(x,y,w,h,r)}"><div class="photo-surface"><img src="photos/{k}.jpg" style="object-position:{focus}" alt="{html.escape(sources[k]["title"])}"></div></figure>'

def sticker(k,x,y,w,r=0):
 source_key={'wheel':'wheel','cablecar':'cablecar-sun','tower':'tower','bison':'bison-solo','griffith':'griffith','palm':'venice'}[k]
 usage[source_key].append({'page':page_number,'role':'异形照片衍生贴纸','type':'derivative-sticker'})
 return f'<img class="sticker" src="../../../docs/process/{k}.png" style="{pos(x,y,w,r=r)}" alt="{html.escape(sources[source_key]["title"])}衍生贴纸">'

def note(t,x,y,w=250,s=30,c='#2c5365',r=0,cls=''):
 return f'<div class="note {cls}" style="{pos(x,y,w,r=r)}font-size:{s}px;color:{c};">{html.escape(t)}</div>'

def label(t,x,y,w=250,s=13,c='#45626b',r=0,cls=''):
 return f'<div class="label {cls}" style="{pos(x,y,w,r=r)}font-size:{s}px;color:{c};">{html.escape(t)}</div>'

def paper(x,y,w,h,c='#eee4ce',r=0,cls=''):
 return f'<div class="scrap-shadow {cls}" style="{pos(x,y,w,h,r)}"><div class="scrap-surface" style="background-color:{c}"></div></div>'

def tape(x,y,r=0,w=82,c='#d4bb80aa'):
 return paper(x,y,w,23,c,r,'tape')

def ink(path,c='#ba6745',width=2.4):
 return f'<svg class="ink" viewBox="0 0 600 800" aria-hidden="true"><path d="{path}" fill="none" stroke="{c}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def add(t):
 global page_number
 pages.append(t); page_number+=1

# 01–02 开篇与地点索引：撕边码头、物件跨层、手绘联结。索引不是导航。
add(
 paper(0,0,600,800,'#dbc5a2')
 +photo('pier',0,0,279,800,0,'edge torn','24% 50%','封面海岸撕边：保留码头与浪花')
 +paper(257,-12,358,832,'#f1e7cc',-1.6,'torn')
 +note('美西',294,36,260,87,'#315b64',-6)
 +note('把风，贴进本子里',287,147,280,34,'#315b64',-3)
 +note('WESTWARD',23,37,260,40,'#fff5d9',-7)
 +photo('griffith',354,214,198,256,5,'polaroid','50% 48%','封面天文台照片：和第三跨页的建筑贴纸呼应')
 +tape(405,207,-10,85)
 +sticker('wheel',32,377,353,-6)
 +photo('twilight',295,517,272,177,-4,'film',reason='封面蓝调照片：白天与入夜的码头对照')
 +note('把海岸折成一页，\n把旷野留给下一页。',285,700,285,29,'#3c5e5f',-4)
 +note('SANTA MONICA',15,720,253,30,'#fff2d0',-4)
 +ink('M 270 335 Q 220 324 183 367 M 183 367 l 0 -14 M 183 367 l 14 -5','#efdbab')
)
add(
 paper(0,0,600,800,'#c8cbb6')
 +paper(13,24,569,744,'#ece3cb',2,'torn')
 +note('这一本，从哪里寄来？',30,28,538,40,'#3e655e',-2)
 +paper(54,86,369,97,'#d9c5a4',-4,'lined')
 +note('海岸寄来蓝色，桥寄来红。\n石头与田野，各有回信。',66,96,340,25,'#715844',-4)
 +note('沿着颜色，\n往远处读。',329,193,240,25,'#4c685d',4)
 +photo('venice',41,214,218,144,-5,'film',reason='地点索引：洛杉矶海岸')
 +photo('goldengate',323,311,238,150,5,'polaroid',reason='地点索引：旧金山海湾')
 +photo('canyon',48,411,229,154,-4,'edge torn',reason='地点索引：亚利桑那岩层')
 +photo('farm',303,543,252,156,4,'polaroid',reason='地点索引：蒙大拿田野')
 +note('LOS ANGELES',41,365,281,25,'#41645d',-5)
 +note('SAN FRANCISCO',307,472,276,25,'#88583f',4)
 +note('PAGE / ARIZONA',44,577,279,25,'#88583f',-3)
 +note('MONTANA',317,708,260,27,'#4a6552',4)
 +ink('M 243 355 C 310 366 279 433 299 451 M 299 451 l -2 -14 M 299 451 l -13 -4 M 310 486 C 314 527 287 554 288 592 M 288 592 l -9 -9 M 288 592 l 8 -10','#5f7c78',2.5)
 +label('地点索引 · 依画面串联，非导航路线',39,748,497,10,'#616e61',-1)
 +tape(109,201,7,84)+tape(399,300,-8,81)+tape(374,534,-8,82)
)
# 03–04 洛杉矶：完整海岸与建筑、植物采集；含长段观察。
add(
 photo('tower',0,0,600,445,0,'edge','50% 50%','加州海岸环境照片，完整救生塔和海面')
 +note('海风翻到蓝色这一页',28,36,550,42,'#2b5a6a',-4)
 +paper(-8,416,624,407,'#ece3ce',-2,'torn')
 +photo('venice',306,464,272,188,5,'edge torn','50% 66%','威尼斯滑板场：真实游客与棕榈树林')
 +paper(24,445,266,293,'#d9c6a5',-4,'lined')
 +note('海岸来信',44,456,218,32,'#6f583f',-4)
 +note('台阶收着阴影，\n海把光铺开。\n树下，有人转弯。\n蓝色留在纸上，\n风从纸边\n继续往前。',45,506,225,24,'#4f605b',-4)
 +sticker('tower',211,579,327,-4)
 +tape(377,452,-9,94)+tape(98,430,9,87)
 +note('45 号塔',380,734,190,24,'#446771',3)
 +ink('M 88 661 Q 91 704 181 712 M 181 712 l -10 -8 M 181 712 l -12 8','#426b76')
 +label('CALIFORNIA COAST',332,669,247,10,'#4e6b67',5)
)
add(
 paper(0,0,600,800,'#c9cdb8')
 +photo('griffith',-2,0,603,353,0,'edge torn','50% 8%','格里菲斯天文台全景：圆顶、坡地与天空')
 +paper(18,332,569,452,'#efe7d3',-2,'torn')
 +note('白房子，向天空借光',193,352,399,35,'#3b5c54',-4)
 +paper(295,414,273,238,'#d5bca0',4,'grid')
 +note('圆顶接住半束光，\n另一半藏进白墙。\n坡上的绿还没走。\n把影子，也留下。',314,433,240,27,'#695842',4)
 +sticker('griffith',-7,492,371,-5)
 +sticker('palm',21,223,186,-7)
 +note('一根细线\n托起一团风',184,399,141,23,'#55715b',-7)
 +ink('M 218 418 Q 192 415 139 365 M 139 365 l 3 15 M 139 365 l 15 4','#67794e')
 +note('GRIFFITH OBSERVATORY',221,714,369,24,'#395f57',-2)
 +note('把天空留给纸边。',151,736,412,26,'#8b6349',-2)
 +tape(401,406,-6,90)
)
# 05–06 旧金山：真实人像与街道，纸窗、便笺、缆车跨层。
add(
 paper(0,0,600,800,'#7c9aaa')
 +paper(12,19,405,754,'#f0e6cd',-2,'torn')
 +note('金门，把风借给衣角',33,28,545,45,'#ae553c',-4)
 +photo('portrait',43,179,307,471,-4,'polaroid','50% 50%','真实原摄影人物留影：不生成新面孔')
 +photo('goldengate',289,125,277,170,7,'film',reason='金门桥全景，与留影的桥塔互相对应')
 +tape(94,168,-9,88)+tape(383,111,9,90)
 +paper(347,349,225,246,'#d5c6a8',5,'lined')
 +note('桥把红色\n交给蓝天。\n风在卷发里\n停了片刻，\n又去更远的海湾。\n照片也有辽阔。',365,371,195,24,'#345c68',5)
 +ink('M 365 308 Q 449 320 484 295 M 484 295 l -14 1 M 484 295 l -6 14','#e5d6b6')
 +note('GOLDEN GATE',411,623,175,22,'#fcf0d5',4)
 +paper(70,694,424,63,'#c7b48f',-4,'torn')
 +note('风不入镜，却留在每一根发梢。',88,707,414,26,'#516357',-4)
 +label('SAN FRANCISCO / BAY',341,665,223,10,'#314f5a',2)
)
add(
 paper(0,0,600,800,'#c9cbb6')
 +photo('cablecar-sun',0,0,299,737,0,'edge torn','46% 50%','缆车街景纵幅，保留木车厢与坡道轨道')
 +paper(298,-13,309,829,'#ede4cb',1.5,'torn')
 +paper(330,26,239,337,'#f5ecd9',-3,'lined')
 +note('把坡道，\n折进木头车厢',344,46,215,32,'#3b6458',-3)
 +note('轨道拐一个弯，\n木窗收进白房子。\n暖棕色的车顶下，\n街道慢慢展开。\n这一页的边缘，\n也跟着有了坡度。',347,154,205,22,'#756248',-3)
 +sticker('cablecar',259,314,295,-8)
 +paper(33,664,203,63,'#b4b7a2',-4,'tag')
 +note('CABLE CAR\n木头的车厢',49,672,185,23,'#36594f',-4)
 +paper(-12,730,634,100,'#ddd4bb',-2,'torn')
 +note('SAN FRANCISCO',29,741,387,26,'#3e6058',-3)
 +ink('M 493 375 Q 556 398 555 449 M 555 449 l -10 -11 M 555 449 l 6 -14','#a16d4e')
 +tape(408,18,8,84)
)
# 07–08 亚利桑那：真正的圆润异形纸窗与河曲采集页。
add(
 paper(0,0,600,800,'#c59775')
 +paper(11,13,581,777,'#ede0c3',-1,'torn')
 +note('光，在石头里写信',31,21,548,49,'#a45137',-4)
 +note('ANTELOPE CANYON',88,104,456,30,'#85563d',-4)
 +photo('canyon',58,161,499,494,0,'window canyon-window','50% 50%','圆润不对称纸窗：沿着岩层曲线观看峡谷')
 +note('岩纹把赭红写成淡紫，\n光落下来，不急着离开。\n石头的褶皱里，也有柔软的地方。',50,670,510,25,'#82513c',-3)
 +ink('M 430 165 Q 411 197 328 222 M 328 222 l 13 -3 M 328 222 l 8 -12','#a05a3a')
 +note('这束光',384,139,166,23,'#96573f',5)

)
add(
 paper(0,0,600,800,'#c6a57e')
 +photo('horseshoe',0,0,600,427,0,'edge','50% 50%','马蹄湾全景，完整河曲作为主景')
 +note('HORSESHOE BEND',24,27,553,41,'#fff3d9',-3)
 +paper(-9,407,627,415,'#eee0c4',-2,'torn')
 +paper(32,447,306,284,'#dbc6a5',-4,'grid')
 +note('河流的一封长信',50,458,290,33,'#945336',-4)
 +note('河水绕过岩壁，\n把远处写成一个弯。\n蓝绿色的那一笔，\n留在赭红的纸上。\n读到这里，慢一点。',53,520,266,26,'#765d45',-4)
 +photo('horseshoe',356,464,211,209,7,'round','52% 65%','同一河曲的圆窗近景，突出水与岩壁的关系')
 +photo('canyon',355,659,210,106,-5,'film',reason='峡谷岩层横幅作为地点间纹理对照')
 +note('岩石的褶皱',367,685,217,22,'#fff0d2',-5)
 +ink('M 321 529 Q 337 549 367 558 M 367 558 l -8 -11 M 367 558 l -13 4','#426c71')
 +tape(106,436,11,92)+tape(451,450,-8,83)
)
# 09–10 黄石：色彩笔记、展开的白色的回信与野牛剪贴。
add(
 photo('prismatic',0,0,600,482,0,'edge','50% 50%','大棱镜温泉：原摄影天然水色与橙色边缘')
 +note('大地，也写彩色的信',27,127,559,43,'#fff5dc',-4)
 +paper(-7,455,625,370,'#e5dfc3',2,'torn')
 +paper(34,489,267,246,'#f1e8d4',-5,'grid')
 +note('采下一小页颜色',51,510,244,33,'#426c69',-5)
 +'<div class="swatches" style="left:51px;top:572px;transform:rotate(-5deg)"><i style="background:#548c9b"></i><i style="background:#c6bf7d"></i><i style="background:#c17342"></i><i style="background:#695041"></i></div>'
 +note('蓝绿留在水心，\n赭红沿岸慢慢晕开。\n蒸汽让边界轻了些。',54,630,244,25,'#4a6a60',-5)
 +photo('prismatic',341,511,204,204,6,'round','51% 70%','温泉圆形观察片：重复原图的颜色边界')
 +tape(110,482,10,86)
 +note('水边的色带',355,738,220,26,'#805c42',3)
 +ink('M 316 580 Q 318 606 347 619 M 347 619 l -8 -12 M 347 619 l -14 2','#557969')
 +label('YELLOWSTONE / COLOR NOTES',28,759,301,10,'#5d7064',-2)
)
add(
 paper(0,0,600,800,'#b8bfa9')
 +photo('oldfaithful',13,19,406,383,-3,'edge torn','50% 45%','老忠实泉喷发原摄影主片，完整蒸汽与森林关系')
 +paper(343,49,235,299,'#eee6d2',4,'flap lined')
 +note('白色的回信',365,72,198,35,'#416558',4)
 +note('蒸汽升起，\n像未写完的信。\n深绿的林线，\n压着大地页脚。\n天空留着空白。',365,130,187,26,'#6f634b',4)
 +tape(433,41,-8,83)
 +note('OLD FAITHFUL',29,391,371,28,'#f8ecd3',-3)
 +photo('bison-solo',312,426,260,174,5,'polaroid',reason='黄石野牛原摄影，保留干草和林地环境')
 +paper(19,461,278,281,'#ded3b6',-4,'torn')
 +note('旷野的慢句子',40,478,245,34,'#3e5f50',-4)
 +note('卷毛接住了光，\n干草藏住了蹄子。\n把这一团安静\n贴在纸边。',42,533,234,27,'#5c6650',-4)
 +sticker('bison',268,566,294,-4)
 +note('远远地看',28,723,230,28,'#876342',-4)
 +ink('M 470 575 Q 492 597 461 629 M 461 629 l 1 -15 M 461 629 l 14 -6','#85724d')
 +tape(399,414,-9,90)
)
# 11–12 田野：绿色采集与山脚白谷仓；不编造成同一天的连续行程。
add(
 paper(0,0,600,800,'#d1c8a4')
 +photo('farm',0,0,600,444,0,'edge','50% 50%','蒙大拿田野：保留山脉、农场与绿地关系')
 +note('让绿色，慢慢漫过纸边',26,27,556,44,'#32543e',-4)
 +note('MONTANA',351,359,225,29,'#fff1d3',2)
 +paper(-10,419,625,410,'#eee2c7',-2,'torn')
 +paper(27,461,269,268,'#d6c9a8',-4,'lined')
 +note('给田野留白',46,477,243,32,'#52674b',-4)
 +note('小房子退到远处，\n绿色就有了余地。\n山把云留在肩上，\n纸页替草地\n留下一小块晴天。',48,532,229,27,'#4a644b',-4)
 +photo('farm',341,467,223,156,6,'film','54% 56%','缩小观察片：农场与山脉的尺度')
 +paper(319,656,242,87,'#c5c7a9',3,'grid')
 +'<div class="swatches" style="left:334px;top:671px;transform:rotate(3deg)"><i style="background:#6d874b"></i><i style="background:#aab064"></i><i style="background:#738784"></i><i style="background:#e9e1c6"></i></div>'
 +note('草地 / 云影 / 纸白',324,716,242,21,'#4a644b',3)
 +tape(399,455,-10,88)+tape(102,445,7,82)
 +label('MONTANA / FIELD NOTES',307,755,270,10,'#687253',-1)
)
add(
 paper(0,0,600,800,'#b4bca4')
 +photo('barn',20,22,383,690,-3,'edge torn','70% 50%','博兹曼白谷仓与山脉纵幅，保留建筑整体')
 +paper(327,99,252,335,'#f0e5ce',3,'flap lined')
 +note('山脚的空白页',347,123,234,35,'#875a3e',3)
 +note('白色谷仓，\n收好山的影子。\n草地铺过门前。\n天空没有落款，\n信就留在山脚。',347,194,215,27,'#59624d',3)
 +tape(418,91,-6,86)
 +photo('barn',335,483,224,201,7,'round','74% 87%','谷仓圆窗细节：在同一张照片中重读建筑')
 +note('BOZEMAN',359,709,218,30,'#415d47',4)
 +note('让一座山，成为一封信的背景。',32,733,530,27,'#45654d',-3)
 +ink('M 508 444 Q 517 466 505 480 M 505 480 l -9 -8 M 505 480 l 9 -8','#8c6b4e')
)
# 13–14 采集与独立贴纸：票签造型不伪造订单，贴纸都有原图关系。
add(
 paper(0,0,600,800,'#7c9693')
 +paper(19,22,558,358,'#efe4ce',-3,'lined')
 +note('有些远方，适合夹在纸页里',34,40,544,34,'#395d56',-3)
 +photo('pier',45,137,172,247,-8,'polaroid','26% 50%','纸袋里露出的码头照片：首尾索引')
 +photo('goldengate',248,124,285,170,5,'film',reason='纸袋里的海湾照片：首尾索引')
 +photo('twilight',313,332,237,157,9,'edge torn',reason='照片口袋里露出的夜景，与白天留影对照')
 +paper(60,395,188,259,'#d4c7a7',-8,'ticket')
 +note('沿途采集',80,419,160,32,'#765438',-8)
 +note('海风\n木头窗框',87,477,165,26,'#4e645c',-8)
 +paper(4,547,593,286,'#b59b72',-2,'pocket torn')
 +'<div class="pocket-fold" style="left:23px;top:563px;width:554px"></div>'
 +note('把风，暂存在这里。',42,647,483,37,'#3f5b50',-4)
 +note('纸边会卷，光会褪去。\n有些片刻，仍愿意再读一次。',46,690,470,27,'#f6edd4',-4)
 +sticker('wheel',392,531,174,6)
 +tape(102,129,10,83)+tape(340,112,-8,88)
)
add(
 paper(0,0,600,800,'#ece4ce')
 +paper(15,18,571,769,'#e5dbc0',-1,'torn')
 +note('把远方，剪成小小的形状',31,27,552,40,'#416352',-4)
 +note('让一座城，从照片里走到纸边',37,99,519,27,'#796047',-3)
 +sticker('wheel',16,147,258,-6)
 +sticker('griffith',298,135,275,4)
 +sticker('tower',310,340,248,4)
 +sticker('cablecar',29,294,197,-7)
 +sticker('bison',35,614,191,-4)
 +sticker('palm',229,348,147,-5)
 +note('摩天轮',37,325,196,25,'#386776',-4)
 +note('三个圆顶',367,333,211,25,'#7b6248',4)
 +note('木头车厢',38,566,200,23,'#7a6248',-6)
 +note('救生塔',402,529,160,23,'#386776',4)
 +note('细细的树干',221,587,175,21,'#5e744e',-5)
 +note('野牛的卷毛',32,751,250,23,'#7a6248',-3)
 +paper(363,607,200,135,'#cbc7a8',4,'lined')
 +note('带走轮廓，\n风景留在原处。',380,637,182,25,'#51674f',4)
 +ink('M 545 286 Q 560 284 562 270 M 562 270 l -8 8 M 562 270 l 2 12','#a47c51',1.8)
)
# 15 独立收尾页：不是空出来的第 16 页。
add(
 paper(0,0,600,800,'#d7c8a7')
 +paper(21,23,555,753,'#efe6d0',-2,'torn')
 +note('Letters from\nElsewhere',39,48,527,62,'#315c62',-5)
 +note('从别处寄来的小纸片',48,209,505,34,'#88583e',-3)
 +paper(47,294,433,223,'#d4c4a5',-4,'lined')
 +note('桥把红色借给天空，\n车窗收进街道的一角。\n光在石头里停了片刻。\n这些小小的远方，\n在纸上，有了重读的形状。',67,308,396,29,'#486153',-4)
 +photo('twilight',174,525,380,198,6,'film',reason='收尾夜景：呼应封面码头，由白天读到入夜')
 +tape(326,511,-8,88)
 +sticker('palm',19,532,148,-8)
 +note('留一页，给下一阵风。',276,739,284,26,'#416556',4)
)

def ragged_polygon():
 rng=random.Random(87); points=[]
 for i in range(0,101,2): points.append(f'{i}% {rng.uniform(.05,.55):.2f}%')
 for i in range(2,101,2): points.append(f'{100-rng.uniform(.05,.65):.2f}% {i}%')
 for i in range(98,-1,-2): points.append(f'{i}% {100-rng.uniform(.05,.55):.2f}%')
 for i in range(98,0,-2): points.append(f'{rng.uniform(.05,.65):.2f}% {i}%')
 return 'polygon('+','.join(points)+')'

css='''
@font-face{font-family:hand;src:url(assets/LongCang-Regular.ttf)}
*{box-sizing:border-box}body{margin:0;background:#283144;color:#355b60}
.page{position:relative;width:600px;height:800px;overflow:hidden;isolation:isolate;background:#eee4cd}
.page>*{position:absolute}figure{margin:0}
.scrap-shadow{filter:drop-shadow(1.5px 3px 3px #29352525)}
.scrap-surface{position:absolute;inset:0;overflow:hidden}
.scrap-surface:after{content:'';position:absolute;inset:0;background:url(assets/paper.png) center/600px 800px;mix-blend-mode:multiply;opacity:.21}
.photo{filter:drop-shadow(2px 4px 3px #182c333a)}
.photo-surface{height:100%;background:#f3edda;padding:6px;overflow:hidden}
.photo img{height:100%;width:100%;object-fit:cover;display:block}
.edge .photo-surface{padding:0}.film .photo-surface{padding:10px;background:#252e2b;border:2px dashed #b6aa8d}
.polaroid .photo-surface{padding:8px 8px 28px;background:#f4edda}
.window{filter:drop-shadow(3px 7px 2px #54412466)}
.window .photo-surface{padding:0;clip-path:polygon(14% 1%,39% 0%,57% 3%,64% 8%,62% 16%,72% 24%,89% 29%,98% 42%,94% 55%,82% 62%,80% 71%,97% 83%,99% 95%,83% 99%,67% 97%,48% 100%,27% 98%,6% 94%,2% 82%,9% 66%,3% 50%,7% 36%,0% 19%)}
.window:before{content:'';position:absolute;inset:-2px;background:#b67d42;clip-path:polygon(14% 1%,39% 0%,57% 3%,64% 8%,62% 16%,72% 24%,89% 29%,98% 42%,94% 55%,82% 62%,80% 71%,97% 83%,99% 95%,83% 99%,67% 97%,48% 100%,27% 98%,6% 94%,2% 82%,9% 66%,3% 50%,7% 36%,0% 19%)}
.note{font-family:hand,cursive;line-height:1.12;white-space:pre-line;z-index:5;font-weight:400}
.label{font-family:-apple-system,BlinkMacSystemFont,sans-serif;line-height:1.4;letter-spacing:1.4px;white-space:pre-line;z-index:5}
.serif{font-family:Georgia,serif;letter-spacing:2px}
.sticker{height:auto;z-index:6;filter:drop-shadow(1.5px 3px 1.5px #17282230)}
.ink{inset:0;width:100%;height:100%;pointer-events:none;z-index:7}
.tape{z-index:9;filter:none}
.tape .scrap-surface{clip-path:polygon(2% 0,98% 3%,94% 17%,100% 31%,95% 53%,100% 76%,95% 98%,0 100%,4% 80%,0 64%,3% 47%,0 24%)}
.lined .scrap-surface{background-image:repeating-linear-gradient(0deg,transparent 0 28px,#78806b18 28px 29px)}
.tag .scrap-surface:before{content:'';position:absolute;left:7px;top:7px;width:7px;height:7px;border-radius:50%;background:#e9e0c8;box-shadow:inset 0 1px 2px #67523444}
.folio{position:absolute;bottom:7px;left:18px;font:9px sans-serif;letter-spacing:1.2px;color:#405a5e;background:#eee6d3bd;padding:3px 6px;z-index:12}
.swatches{display:flex;gap:8px;z-index:5}.swatches i{display:block;width:43px;height:38px;box-shadow:1px 2px 2px #28433420;clip-path:polygon(0 3%,92% 0,100% 94%,4% 100%)}
.pocket-fold{height:2px;background:#826b463a;box-shadow:0 2px 3px #efdab533;z-index:3;transform:rotate(-2deg)}
.pocket .scrap-surface{box-shadow:inset 0 6px 6px #62553720;background-image:linear-gradient(115deg,transparent 20%,#f6ddbc24 50%,transparent 80%)}
'''
css+='.torn .photo-surface,.torn .scrap-surface{clip-path:'+ragged_polygon()+'}'

css+="""
.grid .scrap-surface{background-image:linear-gradient(#7c86611c 1px,transparent 1px),linear-gradient(90deg,#7c86611c 1px,transparent 1px);background-size:24px 24px}
.flap:before{content:'';position:absolute;left:0;top:0;bottom:0;width:8px;background:linear-gradient(90deg,#766d4b25,transparent);z-index:1}
.ticket .scrap-surface{background-image:linear-gradient(90deg,transparent 10px,#8774474a 10px,#8774474a 11px,transparent 11px);border-top:2px dashed #8f77544a;border-bottom:2px dashed #8f77544a}
.round .photo-surface{border-radius:50%;padding:7px;background:#ebe3ce}
.round img{border-radius:50%}.detail img{transform:scale(2.5);transform-origin:75% 35%}
.canyon-window .photo-surface,.canyon-window:before{clip-path:url(#paper-window)}
.canyon-window:before{inset:-3px;background:#ba8b51}
"""

body=''.join(f'<article class="page" id="p{i}" aria-label="第 {i} 页手帐">{content}<small class="folio">WESTWARD / {i:02} · 旅途影像采集</small></article>' for i,content in enumerate(pages,1))
(B/'composition.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>美西旅行手帐 · 纸页排版源稿</title><style>{css}</style><body><svg style="position:absolute;width:0;height:0" aria-hidden="true"><defs><clipPath id="paper-window" clipPathUnits="objectBoundingBox"><path d="M .18 .018 C .27 0 .43 .004 .53 .035 C .62 .06 .6 .13 .655 .19 C .715 .25 .775 .224 .854 .268 C .94 .322 .977 .395 .958 .472 C .948 .558 .883 .597 .87 .676 C .864 .748 .979 .8 .97 .877 C .972 .941 .891 .986 .801 .97 C .718 .959 .658 .985 .56 .985 C .419 .99 .325 .963 .239 .978 C .143 .989 .032 .957 .028 .888 C .027 .808 .077 .728 .068 .635 C .062 .557 .025 .502 .029 .429 C .03 .331 .105 .27 .071 .182 C .054 .1 .074 .038 .18 .018 Z"/></clipPath></defs></svg>{body}</body></html>')
for r in records:
 r['usage']=usage[r['key']]
 r['selected']=bool(r['usage'])
 r['included_as_photograph']=any(u['type']=='photograph' for u in r['usage'])
 r['selection_reason']='原摄影入册，保留自然光与主体细节' if r['included_as_photograph'] else '仅用于摩天轮主体衍生贴纸，不计入原照片数量'
(B/'usage.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pages':len(pages),'unique_photographs':sum(r['included_as_photograph'] for r in records),'sticker_source_photos':6,'source_photos_total':len(records)},ensure_ascii=False))
