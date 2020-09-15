from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
info_dict = {
    "蜜柚思月": "散发着奶油芝士味的玉兔，守护着亮黄巧克力喷砂的月寒宫。抹以独特的香柚果酱奶油，让十五的味道在舌尖团圆。清新柔滑的口感，寄托最浓郁的中秋情怀。",
    "偏爱": "蛋糕表面装饰纯手工制作,海盐奥利奥坚果口味,含有较大颗粒坚果，存在食用风险，请老人、小孩谨慎选择。",
    "爱丽丝之梦": "海盐奥利奥坚果口味,含有较大颗粒坚果，存在食用风险，请老人、小孩谨慎选择。",
    "芒莓二重奏": "正当季的蓝莓遇上滑嫩绵软的芒果，一口蛋糕可以吃到两种酸甜。来自宝岛的金煌芒铺满蛋糕。看似几粒点缀的蓝莓果粒，还在奶油与红丝绒蛋糕里藏着惊喜。",
    "四季": "四拼组合，满足众口难调，四味精心搭配，用口感传达四季。绿色春天，日本宇治抹茶，充满希望；黄色夏天，进口芒果芝士，热情洋溢；果满秋天，缤纷时令水果，收获满满；暗色冬天，香草法芙娜黑巧，沉淀甜蜜。",
    "榴芒双拼": "清新芒果慕斯，当季的鲜芒果粒，颗颗明黄灿烂过南国阳光； 霸道榴莲忘返，甜软果肉融合淡奶油、白巧，柔情蜜意让你欲罢不能。",
    "榴莲忘返": "泰国进口金枕，自然成熟，细腻柔滑，连不爱吃榴莲的人也会爱上。配以海绵蛋糕，鲜润滋味比单吃榴莲更高级。榴莲果肉与海绵蛋糕1：1，令榴莲控上瘾。",
    "芒果慕斯": "芒果慕斯与偶像明星郑凯同台共演，诠释青春的骚动与肆意。那一抹明黄身影，是故事里最贴切的甜意。谁是炎炎盛夏里最受爱戴的水果明星，当非芒果莫属！妍媚透亮奔放的香，丰腴得饱满欲滴的甜，新鲜清爽的酸、绵细软糯的口感，让人仿佛置身于阳光、沙滩、椰树、芒果飘香的热带风情里。",
    "芒果芝士": "一个蛋糕尝到3种芒果滋味，搭配澳大利亚奶油芝士，营养美味。表层芒果雕花，还原热带风情，一勺挖下去，软糯细腻的奶油芝士里，猝不及防咬到芒果鲜粒，满是惊喜。",
    "玫瑰情人": "玫瑰情人加入新配方，精选新鲜芒果与法国宝茸果茸，让经典口味再升级，层次口感百转千回。搭配经典百利甜酒淡奶油产生的奇妙反应，丝滑柔润的触感，让你一口满足。朵朵玫瑰上，只摘下相同的大小，像情人节浪漫过分的礼物，包裹着柔软鲜香与告白。",
    "小时光": "这一款蛋糕，将带你回到往日。壹点壹客大厨kevin说：现在出现了许多的新奇的蛋糕，但奶油蛋糕的滋味常常让人难忘。创作这款蛋糕，希望能带给你第一次吃到蛋糕的满足感。鲜香的奶油，多层的柔嫩蛋糕胚，让你感受回到过去旧时光的幸福滋味。",
    "花季": "新晋的蛋糕界时尚“红人”——花季。缀满红颜草莓，藏着开心果，散发着诱人的香气，围上粉系的ladyfinger。酸甜、馥郁、酥软，每一口，都是少女欢喜的秘密。",
    "杨枝甘露糖水蛋糕": "在港剧中，一句“等阵，饮埋糖水先。”总在耳边萦绕。在家庭中，糖水总扮演者一个甜蜜的治愈秘方，能下火，清热解毒。虽然并不清楚它的疗效，但确实治愈繁忙一刻的灵魂，留下一份暖暖的幸福感。在港式糖水中，为人熟知的就是杨枝甘露，它几乎在每一家的糖水店铺都放在了招牌的位置。杨枝甘露与欧洲西点碰撞，结合出一种全新的口感。原创出港式甜点的原味，提起围边，精选的西柚，芒果以及灵魂西米露慢慢落下，在你的嘴巴里迸发全新体验。",
    "海盐奥利奥": "作为饼干界的明星产品，从来不放过和任何好吃的融合的机会。壹点壹客匠心研发，将奥利奥与西点蛋糕巧妙融合，在浓郁法国诺曼底淡奶油的烘托下，微咸海盐与奥利奥，融成不腻口的微糖口感。戚风蛋糕胚，柔软而适口，像舌头躺在沙发一般，让你忍不住一口接一口，满足感立即盈满了你的心。",
    "小确幸": "“小确幸”，是与你在一起，微小的事物也能引起确实的幸福与满足。随着爱情升温，意大利起泡酒开始涌动，结合红颜草莓，醇美搭配酸甜，在时间的印证里，融合成彼此的味道，带来属于你们美好的小确幸。",
    "缪斯": "当甘甜芒果与酸奶相遇，一种独有清新就跃然舌尖上，轻柔婉转，一如众神之女缪斯，在宴会上翩翩起舞。而后是一点马斯卡彭的芝士浓郁，意大利的风情似乎卷起了西西里海岸的潮水，层叠往复，仿佛少女在旋转中，散发的淡淡芬芳。",
    "彩虹独角兽": "当独角的小马奔跑在天际，那么彩虹就是它留下的足记。当彩虹在云间穿梭，留下的还有如梦似幻的甜蜜。翻糖云朵，巧克力冰淇淋甜筒，能实现愿望的纽扣，带上所有梦想能代表的一切，以梦为马，驰骋在路。",
    "初生": "生日，人之初的纪念日。人，生而简单，生而纯粹。正如这款蛋糕，让原料回归纯粹的口味，让色彩回归纯粹的暖，期望这款简单的生日蛋糕，陪你回到最初纯粹的自己",
    "宇治微风": "采用1年产15天的日本京都宇治春茶用石磨研磨而成的抹茶，融合了黄梅果的清甜，口感细腻，茶香悠远，蛋糕底在普通蛋糕底基础上加入了扁桃仁粉颗粒，细细品尝，口齿中有颗粒的质感和扁桃仁的果仁香气",
    "果篮": "经典水果蛋糕新花样，口感清新。6种+严选时令鲜果，有颜有料。加了一点点百利酒的薄层奶油，放大突出水果清甜。柔润细腻的海绵蛋糕，丝滑入喉。",
    "淘气兔兔": "一只揣着怀表的白兔小姐，会带着你跳入神奇的酸奶味兔子洞，开始一段关于味蕾的冒险！表面粉嫩嫩的巧克力喷砂，粉粉惹人爱！兔子的灵魂散发着酸奶的香气，一不小心就陷入它的魅力。慕斯和果冻，口感细腻，入口即化。软萌的外表，让快乐有了形状，也有了滋味。",
    "开森汪汪": "炎炎夏日，开森汪汪举办来一场热带水果的Party！嫩黄的身影，小巧的耳朵，是在这场狂欢中最靓的那只！盛夏里人见人爱的明星水果，当然少不了荔枝&覆盆子！一层层荔枝果肉清甜喜人，还有桑莓的微酸，让你陶醉在酸甜的世界里，此时纵情跃下，迎接你的绝不是硬梆梆土地，唇齿所及是柔软香嫩开心果蛋糕胚。",
    "柚の园": "温柔的黄与白，缤纷的波波池，柔软的蛋糕气孔中散发的清新柚香，每一口，都能看到孩子纯真的笑脸，这是童年的味道，简单而纯粹的欢乐。柚子味道浓郁，咀嚼中有些许菠萝的微酸，不同层次的酸与甜，酸甜中和，却恰到好处，这是成长的味道，痛并快乐着。柚の园，记忆中的幼稚园，梦境般的泡泡童年。",
    "仲夏甜芒": "师傅向来对芒果蛋糕的开发是有自信心的。他对芒果与蛋糕的契合已有多年的研究，此次依然是他得心应手的作品，将芒果融入来自法国诺曼底的淡奶油中，与戚风蛋糕胚的柔软相融，每一口都是来自夏日芒果香。为了符合亚洲人的口味，蛋糕从糖分上已减去大半，保留着恰好诱人的轻甜，夹心的鲜切芒果与黄心奇异果，是奶油蛋糕中不可缺的水果灵魂。",
    "提拉米苏": "松软细腻的意大利马斯卡彭芝士，混合了迷人的意式特浓咖啡，以及意大利杏仁利口酒和顶级可可粉。入口时，芝士的香滑、咖啡的苦涩、杏仁酒的甘浓，交织成馥郁难忘的专属味道，让人不由得想起那个恒古流传的誓言：带我走!",
    "wow，小棕熊": "来自遥远冰川山脉的“棕色”小熊，来壹点壹客啦！Q萌可爱，冰凉顺滑，让小朋友们发出WOW般欢呼的喜悦。馥郁巧克力喷砂搭配意大利“国粹”Gelato冰淇淋，多重美味，入口即化，时刻品味熊熊凉爽，还有费列罗榛果藏在里面哦~",
    "Gelato双子星冰淇淋蛋糕": "Gelato来自意大利的“国粹”冰淇淋！炎炎夏日，当清凉的Gelato遇上浓香的蛋糕，入口即化的冰凉，沁人心脾的浓香，绵密醇厚在唇间跳跃，果香清甜在舌尖回荡。这个夏季，Gelato冰淇淋蛋糕将演绎一场精妙无比的冰爽之旅！",
    "Gelato榴莲冰淇淋蛋糕": "号称水果之王的泰国金枕头榴莲，和意大利国粹GELATO冰淇淋的强强组合，演绎出的味觉盛宴，只有尝过的人才能真正体会",
    "粉红小仙女": "今天，也要做一个吃可爱长大的小仙女。清新淡雅的特制玫瑰奶油，散发出阵阵花香，与法芙娜馥郁巧克力相结合，质地细腻，口感柔滑。 皇冠为庆祝日加冕仪式感， 粉嫩尽显少女心。",
    "雪奈蓝莓": "当夏日把世间所有镀上一层银光闪闪，也为秋日的水果甜蜜积蓄能量时，在盛夏之日，年均日照1500小时以上，颗粒丰润、色泽通透的蓝莓正在给夏日献上酸甜之姿，搭配着法国诺曼底奶油的浪漫口感，一口接着一口的阳光味道，还有内藏的奇异果与芒果，更是精彩纷呈，让你被包围在热情的夏日之果中。",
    "许愿仙子": "圣洁的许愿天使聆听生日的愿望，以爱的魔法为你守候。配以经典花季蛋糕，精选优质草莓，粒粒饱满，酸甜莓香，用匠心的美味助力美好的生日心愿。",
    "梵星·如梦": "手绘梦幻的星空，以法芙娜白巧克力的柔滑与浓甜；星空下，棉花糖样软糯的蛋糕胚上，适合桑梅与草莓果茸的甜美之梦的诞生。",
    "六合寿桃": "桃，自古便是贺寿主角之一，寓意福如东海、寿比南山。复式双层桃山造型，上层细腻绵软，更适长者食用；底层奶油馥郁、丝滑爽口，更适年轻家人，时令鲜果嵌入馥郁奶油，营养健康。",
}


def commodity_info(request, commodity_name):
    for info_key in info_dict:
        if commodity_name == info_key:
            commodity_info = info_dict[commodity_name]
    commodity_pic_address = '/static/commidity_pic/' + commodity_name + '.jpg'
    result = {'commodity_name': commodity_name, 'commodity_info': commodity_info, 'commodity_pic_address': commodity_pic_address}
    print(result)
    return render(request, 'pay.html', locals())











# import os

# from cairo._cairo import Content
# from django.conf import settings
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt

# from .models import CommodityInfo, ProductsCategory, ImageInfo


# # Create your views here.
# # 类别列表
# def productscategory_list(request):
#     productscategory_list = ProductsCategory.objects.filter(is_active=True)
#     return render(request, 'commodity/productscategory_list.html', locals())


# # 新增类别
# @csrf_exempt
# def productscategory_add(request):
#     if request.method == "GET":
#         return render(request, 'commodity/productscategory_add.html')
#     elif request.method == "POST":
#         CategoryName = request.POST['CategoryName']
#         try:
#             ProductsCategory.objects.create(CategoryName=CategoryName)
#         except Exception as e:
#             print('create error %s' % e)
#             return HttpResponse('create productscategory error')
#     return HttpResponseRedirect('/commodity/productscategory_list')


# # 删除类别
# def productscategory_delete(request):
#     pid = request.GET.get('pid')
#     if not pid:
#         return HttpResponse('--pid error--')
#     try:
#         productscategory = ProductsCategory.objects.get(id=pid, is_active=True)
#     except Exception as e:
#         print("get ProductsCategory error %s" % e)
#         return HttpResponse('get productscategory error')
#     productscategory.is_active = False
#     productscategory.save()
#     return HttpResponseRedirect('/commodity/productscategory_list')


# # 修改类别
# def productscategory_update(request, pid):
#     try:
#         productscategory = ProductsCategory.objects.get(id=pid, is_active=True)
#     except Exception as e:
#         print("get productscategory error %s" % e)
#         return HttpResponseRedirect('get productscategory error')
#     if request.method == "GET":
#         return render(request, 'commodity/productscategory_update.html', locals())
#     elif request.method == "POST":
#         CategoryName = request.POST['CategoryName']
#         productscategory.CategoryName = CategoryName
#         productscategory.save()
#         return HttpResponseRedirect('/commodity/productscategory_list')


# # 图片列表
# def Images_list(request):
#     Images_list = ImageInfo.objects.filter(is_active=True)
#     return render(request, 'commodity/Images_list.html', locals())

# # 添加大图片
# @csrf_exempt
# def MaxImages_add(request):
#     if request.method == 'GET':
#         return render(request, 'commodity/MaxImages_add.html')
#     elif request.method == 'POST':
#         title = request.POST['title']
#         a_file = request.FILES['myfile']
#         ImageInfo.objects.create(ImageName=title, ImgUrl=a_file)
#         return HttpResponse('upload success:%s,%s' % (a_file.name, title))


# # 添加小图片
# @csrf_exempt
# def MinImages_add(request):
#     if  request.method == 'GET':
#         return render(request, 'commodity/MinImages_add.html')
#     elif request.method == 'POST':
#         title = request.POST['title']
#         a_file = request.FILES['myfile']
#         ImageInfo.objects.create(ImageName=title, ImgDesc=a_file)
#         return HttpResponse('upload success:%s,%s' % (a_file.name, title))


# # 商品列表
# # 增加分页功能
# def commodity_list(request):
#     commodity_list = CommodityInfo.objects.filter(is_active=True)
#     # 每页显示的条数
#     paginator = Paginator(commodity_list, 10)
#     # 第几页
#     current_page = request.GET.get('page', 1)
#     # 页数转换为整数
#     current_page = int(current_page)
#     page = paginator.page(current_page)
#     # 展示当前页面的数据
#     commodity_list = paginator.get_page(current_page)
#     return render(request, 'commodity/commodity_list.html', locals())


# # 添加商品
# @csrf_exempt
# def commodity_add(request):
#     if request.method == 'GET':
#         return render(request, 'commodity/commodity_add.html')
#     elif request.method == 'POST':
#         name = request.POST['Name']
#         info = request.POST['Info']
#         material = request.POST['Material']
#         price = request.POST['Price']
#         size = request.POST['Size']
#         putaway = request.POST['Putaway']
#         version = request.POST['version']
#         sell = request.POST['Sell']
#         best = request.POST['Best']
#         badc = request.POST['Badc']
#         # productscategory = ProductsCategory.objects.get(id=pid)
#         try:
#             CommodityInfo.objects.create(Name=name, Info=info, Material=material,
#                                          Price=price, Size=size, Putaway=putaway,
#                                          version=version, Sell=sell, Best=best,
#                                          Badc=badc, ProductsCategory_id=1,
#                                          ImageInfo_id=2)
#         except Exception as e:
#             print('create error %s' % e)
#             return HttpResponse('create commodity error')
#     return HttpResponseRedirect('/commodity/commodity_list')


# # 删除商品信息
# def commodity_delete(request):
#     cid = request.GET.get('cid')
#     if not cid:
#         return HttpResponse('--cid error--')
#     try:
#         commodityinfo = CommodityInfo.objects.get(id=cid, is_active=True)
#     except Exception as e:
#         print('get commodityinfo error %s' % e)
#         return HttpResponse('get commodityinfo error ')
#     commodityinfo.is_active = False
#     commodityinfo.save()
#     return HttpResponseRedirect('/commodity/commodity_list')


# # 修改商品信息
# def commodity_update(request, cid):
#     try:
#         commodityinfo = CommodityInfo.objects.get(id=cid, is_active=True)
#     except Exception as e:
#         print("get commodityinfo error %s" % e)
#         return HttpResponseRedirect('get commodityinfo error')
#     if request.method == "GET":
#         return render(request, 'commodity/commodity_update.html', locals())
#     elif request.method == "POST":
#         Name = request.POST['Name']
#         Info = request.POST['Info']
#         CategoryName = request.POST['CategoryName']
#         # ImgUrl = request.POST['ImgUrl']
#         # ImgDesc = request.POST['ImgDesc']
#         Material = request.POST['Material']
#         Price = request.POST['Price']
#         Size = request.POST['Size']
#         Putaway = request.POST['Putaway']
#         commodityinfo.Name = Name
#         commodityinfo.Info = Info
#         commodityinfo.CategoryName = CategoryName
#         # commodityinfo.ImgUrl = ImgUrl
#         # commodityinfo.ImgDesc = ImgDesc
#         commodityinfo.Material =Material
#         commodityinfo.Price = Price
#         commodityinfo.Size = Size
#         commodityinfo.Putaway = Putaway
#         commodityinfo.save()
#         return HttpResponseRedirect('/commodity/commodity_list')


# # 加载商品分类
# def loadinfo(request):
#     context = {}
#     context['productscategory'] =ProductsCategory.objects.all()
#     return context


# # 首页商品展示
# def commodity_index(request, page=1):
#     commodity_list = CommodityInfo.objects.all()
#     # 分页
#     # 每页显示的条数
#     paginator = Paginator(commodity_list, 10)
#     # 第几页
#     current_page = request.GET.get('page', 1)
#     # 页数转换为整数
#     current_page = int(current_page)
#     page = paginator.page(current_page)
#     # 展示当前页面的数据
#     commodity_list = paginator.get_page(current_page)
#     return render(request, 'commodity/commodity_index.html', locals())


# #商品详情页面
# def commodity_info(request):
#     cid = request.GET.get('cid')
#     # 商品详情页
#     context = loadinfo(request)
#     # 加载商品详情信息
#     return render(request, 'commodity/commodity_info.html', locals())
