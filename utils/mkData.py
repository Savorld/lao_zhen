# -*- coding:utf-8 -*-

from DB import Pg_db
from datas import city, pre_areas
import random
import logging


# with open('../static/img1/brank/nature0.jpg', 'rb') as f:
#     cont = f.read()
#     for i in range(4, 27):
#         with open('../static/img1/brank/nature'+str(i)+'.jpg', 'wb') as f1:
#             f1.write(cont)

def lz_details():
    p = Pg_db()
    imgs = [
        'new',
        'shop',
        'work',
        'tour',
        'movie',
        'money',
        'run',
        'it',
        'health',
        'nature',
    ]
    urls = [
        'http://www.huanqiu.com/',
        'https://www.taobao.com/',
        'https://tieba.baidu.com/index.html',
        'https://zh.airbnb.com/',
        'http://www.youku.com/',
        'http://finance.sina.com.cn/',
        'http://sports.sohu.com/',
        'http://www.autohome.com.cn/beijing/',
        'http://www.cnys.com/',
        'http://www.natureasia.com/zh-cn',
    ]
    for i in range(len(imgs)):
        k = range(5)
        for n in range(27):
            img_path = 'img/brank/' + imgs[i] + str(n) + '.jpg'
            url = urls[i]
            desc = '第' + str(i) + '类第' + str(n) + '个'
            cid = i + 6
            if n in range(5):
                sql = 'insert into lz_details(d_img, d_url, d_desc, d_class_id, ' \
                      'd_hot_order) values(%s, %s, %s, %s, %s);'
                args = tuple([img_path, url, desc, cid, k.pop(random.randint(0,
                                                                             len(
                                                                                 k) - 1))])
            else:
                sql = 'insert into lz_details(d_img, d_url, d_desc, d_class_id) ' \
                      'values(' \
                      '%s, ' \
                      '%s, %s, %s);'
                args = tuple([img_path, url, desc, cid])
            p.insert(sql, args)


def shq_hotCitys():
    p = Pg_db()

    city = {"110000": "北京市",
            "150600": "鄂尔多斯市",
            "320200": "无锡市",
            "330100": "杭州市",
            "510100": "成都市",
            "710100": "台北市",
            "532502": "开远市",
            "511529": "屏山县",
            }
    li = range(len(city))
    for k, v in city.items():
        sql = 'insert into shq_hotCitys(hc_name, hc_num, hc_order) VALUES (' \
              '%s, %s, %s)'
        para = (v, int(k), li.pop(random.randint(0, len(li) - 1)))
        p.insert(sql, para)


def shq_mainInfo():
    pg = Pg_db()
    poses = [11, 12, 211, 212, 221, 222, 3]
    for p in poses:
        for k, v in city.items():
            if p == 11:
                sql = 'insert into shq_mainInfo(mi_img, mi_url, mi_city, mi_pos) ' \
                      'VALUES (%s, %s, %s, %s);'
                for i in range(3):
                    args = ('img/living_pic/' + k + '_' + str(i) + '.jpg',
                            'http://travel.cnr.cn/list/20170703/t20170703_523829945.shtml',
                            v,
                            p
                            )
                    pg.insert(sql, args)
            elif p in (12, 211, 221):
                sql = 'insert into shq_mainInfo(mi_desc, mi_url, mi_city, mi_pos) ' \
                      'VALUES (%s, %s, %s, %s);'
                num = {12: 5, 211: 18, 221: 18}
                for i in range(num[p]):
                    args = (v + '资讯' + str(i),
                            'http://city.china.com.cn/',
                            v,
                            p
                            )
                    pg.insert(sql, args)
            elif p == 3:
                sql = 'insert into shq_mainInfo(mi_img, mi_url, mi_desc, mi_city, mi_pos) ' \
                      'VALUES (%s, %s, ' \
                      '%s, %s, %s);'
                for i in range(8):
                    args = (
                        'img/living_pic/m/' + k + '-' + str(i) + '.jpg',
                        'http://bj.58.com/',
                        v + '生活资讯' + str(i),
                        v,
                        p
                    )
                    pg.insert(sql, args)
            else:
                sql = 'insert into shq_mainInfo(mi_img, mi_url, mi_desc, mi_city, mi_pos) ' \
                      'VALUES (%s, %s, ' \
                      '%s, %s, %s);'
                for i in range(2):
                    args = (
                        'img/living_pic/s/' + k + '^' + str(i) + '.jpg',
                        'http://stock.eastmoney.com/',
                        v + '股票期权' + str(i),
                        v,
                        p
                    )
                    pg.insert(sql, args)
        print p, '完成'


def shq_detailClass():
    pg = Pg_db()
    p_cla = [
        '客店',
        '食界',
        '休闲娱乐',
        '兴趣活动',
        '生活便民',
        '房产相关',
        '国内游',
        '出境游',
        '就近工作',
        '自修·公益',
    ]
    for n, pc in enumerate(p_cla):
        sql = 'insert into shq_detailclass(dc_name, dc_pclass_id) values(%s, ' \
              '%s)'
        for i in range(5):
            args = (
                pc + '详类' + str(i),
                n + 16
            )
            pg.insert(sql, args)


def shq_arealinks():
    pg = Pg_db()
    p_cla = [
        '客店',
        '食界',
        '休闲娱乐',
        '兴趣活动',
        '生活便民',
        '房产相关',
        '国内游',
        '出境游',
        '就近工作',
        '自修·公益',
    ]
    d_cla = [
        '客店详类0',
        '客店详类1',
        '客店详类2',
        '客店详类3',
        '客店详类4',
        '食界详类0',
        '食界详类1',
        '食界详类2',
        '食界详类3',
        '食界详类4',
        '休闲娱乐详类0',
        '休闲娱乐详类1',
        '休闲娱乐详类2',
        '休闲娱乐详类3',
        '休闲娱乐详类4',
        '兴趣活动详类0',
        '兴趣活动详类1',
        '兴趣活动详类2',
        '兴趣活动详类3',
        '兴趣活动详类4',
        '生活便民详类0',
        '生活便民详类1',
        '生活便民详类2',
        '生活便民详类3',
        '生活便民详类4',
        '房产相关详类0',
        '房产相关详类1',
        '房产相关详类2',
        '房产相关详类3',
        '房产相关详类4',
        '国内游详类0',
        '国内游详类1',
        '国内游详类2',
        '国内游详类3',
        '国内游详类4',
        '出境游详类0',
        '出境游详类1',
        '出境游详类2',
        '出境游详类3',
        '出境游详类4',
        '就近工作详类0',
        '就近工作详类1',
        '就近工作详类2',
        '就近工作详类3',
        '就近工作详类4',
        '自修·公益详类0',
        '自修·公益详类1',
        '自修·公益详类2',
        '自修·公益详类3',
        '自修·公益详类4',
    ]
    num = 0
    sql = 'insert into shq_arealinks(al_img, al_url, al_desc, ' \
          'al_declass_id, al_areaid) ' \
          'values(%s, %s, %s, %s, %s)'

    for k, v in pre_areas.items():
        for p_c in p_cla:
            for d_id, d_c in enumerate(d_cla):
                if p_c not in d_c:
                    continue
                for i in range(6):
                    args = (
                        'img/living_pic/dp/' + str(
                            random.randint(1, 4)) + '.jpg',
                        'http://news.sina.com.cn/area/zj.shtml',
                        '/'.join([v, p_c, d_c, str(i)]),
                        d_id + 1,
                        int(k)
                    )
                    pg.insert(sql, args)
        num += 1
        print '%s-%s-完成---%s' % (k, v, num)


def qy_hots():
    pg = Pg_db()
    desc = [
        "洗护清洁",
        "卫生巾",
        "纸尿裤",
        "花卉展",
        "种苗子"
    ]
    url = 'http://www.gsxt.gov.cn/index.html'
    orders = range(len(desc))
    for d in desc:
        sql = 'insert into qy_hots(h_url, h_desc, h_order) values(%s, %s, %s)'
        args = (
            url,
            d,
            orders.pop(random.randint(0, len(orders) - 1))
        )
        pg.insert(sql, args)


def lz_indexslider():
    pg = Pg_db()
    url = 'http://www.sme.gov.cn/'
    cla = range(2, 6)

    sql = 'insert into lz_indexslider(is_url, is_img, is_classid, is_pos) ' \
          'values(%s, %s, %s, %s)'
    for c_id in cla:
        for j in range(3):
            args = (
                url,
                'img/index_slider/home-b' + str(random.randint(1, 2)) + '.jpg',
                c_id,
                1
            )
            pg.insert(sql, args)
        for i in range(9):
            args = (
                url,
                'img/brank/brank' + str(random.randint(1, 9)) + '.png',
                c_id,
                2
            )
            pg.insert(sql, args)


def qy_slider():
    pg = Pg_db()

    sql = 'insert into qy_slider(s_url, s_img, s_classid) values(%s, %s, %s)'

    for i in [26, 29, 30]:
        for j in range(2):
            args = (
                'http://wiki.mbalib.com/wiki/%E4%BC%81%E4%B8%9Ahttp://wiki'
                '.mbalib.com/wiki/%E4%BC%81%E4%B8%9A',
                'img/qy_slider/b' + str(random.randint(1, 3)) + '.jpg',
                i
            )
            pg.insert(sql, args)


def qy_filterclass():
    pg = Pg_db()
    sql = 'insert into qy_filterclass(fc_name, fc_pclassid) values(%s, %s)'
    for k, v in {'26': '会馆', '29': '加盟', '30': '设计'}.items():
        for i in range(6):
            args = (
                v + '大类' + str(i),
                int(k)
            )
            pg.insert(sql, args)


def qy_subfilter():
    pg = Pg_db()
    f_class = pg.query('select fc_id, fc_name from qy_filterclass')
    sql = 'insert into qy_subfilter(sf_name, sf_pclassid) values(%s,%s)'
    for id, val in f_class:
        for i in range(8):
            args = (
                val + '/' + str(i),
                id
            )
            pg.insert(sql, args)


def qy_links():
    pg = Pg_db()
    sub_f = pg.query('select sf_id, sf_name from qy_subfilter')
    sql = 'insert into qy_links(l_url, l_img, l_desc, l_pclassid, l_areanum) ' \
          'values(%s, %s, %s, %s, %s)'
    for n, a in pre_areas.items():
        for f_id, f_name in sub_f:
            for i in range(8):
                args = (
                    'http://www.globrand.com/',
                    'img/qy_links/1.jpg',
                    a + '/' + f_name + '/' + str(i),
                    f_id,
                    int(n)
                )
                pg.insert(sql, args)
        print a, '--', n, '--ok!'


def qy_nofilterclass():
    pg = Pg_db()
    sql = 'insert into qy_nofilterclass(nfc_name, nfc_pclassid) values(%s, %s)'
    tmp = ['科技商展', '品牌之路']
    for i, t in enumerate(tmp):
        for j in range(3):
            args = (
                t + '/子类' + str(j),
                i + 27
            )
            pg.insert(sql, args)


def qy_nofilterlinks():
    pg = Pg_db()
    pclass = pg.query('select nfc_id, nfc_name from qy_nofilterclass')
    sql = 'insert into qy_nofilterlinks(nfl_url, nfl_img, nfl_desc, ' \
          'nfl_pclassid) values(%s, %s, %s, %s)'
    for id, name in pclass:
        for j in range(9):
            args = (
                'http://www.globrand.com/',
                'img/qy_links/2.jpg',
                name + '/资讯/' + str(j),
                id
            )
            pg.insert(sql, args)


def dx_hots():
    pg = Pg_db()
    sql = 'insert into dx_hots(h_url, h_desc) values(%s, %s)'
    for i in range(6):
        args = (
            'https://www.daoxuehao.com/dxhedu/',
            '导学热门' + str(i)
        )
        pg.insert(sql, args)


def dx_slider():
    pg = Pg_db()
    sql = 'insert into dx_slider(s_url, s_img, s_pclassid) values(%s, %s, %s)'
    for i in range(31, 39):
        for j in range(3):
            args = (
                'http://youxue.xdf.cn/',
                'img/dx_slider/b' + str(random.randint(1, 3)) + '.jpg',
                i
            )
            pg.insert(sql, args)


def dx_links():
    pg = Pg_db()
    cla = pg.query('select c_id, c_name from lz_classes where c_pid=4')
    sql = 'insert into dx_links(l_url, l_img, l_desc, l_pclassid, l_areanum) ' \
          'values(%s, %s, %s, %s, %s)'
    for n, a in pre_areas.items():
        for c_id, c_name in cla:
            for i in range(8):
                args = (
                    'http://www.chinanews.com/life/2015/03-17/7135274.shtml',
                    'img/dx_links/1.jpg',
                    a + '/' + c_name + '/' + str(i),
                    c_id,
                    int(n)
                )
                pg.insert(sql, args)
        print a, '--', n, '--ok!'


def e_hots():
    pg = Pg_db()
    sql = 'insert into e_hots(h_url, h_desc) values(%s, %s)'
    for i in range(6):
        args = (
            'http://www.cnbanbao.cn/',
            'e板报热门' + str(i)
        )
        pg.insert(sql, args)


def e_left():
    pg = Pg_db()
    sql = 'insert into e_left(l_url, l_desc) values(%s, %s)'
    for i in range(8):
        args = (
            'http://www.qingting.fm/',
            'e板报资讯-左-' + str(i)
        )
        pg.insert(sql, args)


def e_slider():
    pg = Pg_db()
    sql = 'insert into e_slider(s_url, s_img, s_desc) values(%s, %s, %s)'
    for i in range(3):
        args = (
            'http://www.cflac.org.cn/ys/',
            'img/e_slider/e-banner-' + str(i) + '.jpg',
            'e板报轮播图-' + str(i)
        )
        pg.insert(sql, args)


def e_right():
    pg = Pg_db()
    sql = 'insert into e_right(r_url, r_img, r_desc) values(%s, %s, %s)'
    for i in range(4):
        args = (
            'https://www.zhihu.com/question/21859177',
            'img/e_right/e-hot-1.jpg',
            'e板报资讯-右-' + str(i)
        )
        pg.insert(sql, args)


def e_lowRight():
    pg = Pg_db()
    sql = 'insert into e_lowright(lr_url, lr_img, lr_desc) values(%s, %s, %s)'
    for i in range(11):
        args = (
            'http://www.juzimi.com/article/%E8%82%96%E7%94%B3%E5%85%8B%E7%9A%84%E6%95%91%E8%B5%8E',
            'img/e_lowright/e-ad2.jpg',
            'e板报资讯-右下-' + str(i)
        )
        pg.insert(sql, args)


def e_links():
    pg = Pg_db()
    cla = pg.query('select c_id, c_name from lz_classes where c_pid=5')
    sql = 'insert into e_links(l_url, l_img, l_desc, l_pclassid) values(%s, ' \
          '%s, %s, ' \
          '%s)'
    for c_id, c_name in cla:
        for i in range(11):
            args = (
                'http://www.duanwenxue.com/',
                'img/e_links/e-pic1.jpg',
                'e板报资讯-' + c_name + '-' + str(i),
                c_id
            )
            pg.insert(sql, args)


def js_classes():
    pg = Pg_db()
    cla = [
        "平台介绍",
        "关于我们",
        "商务合作",
        "法律申明",
        "服务协议",
        "老镇招聘"
    ]
    sql = '''insert into js_classes(c_name, c_level) values(%s, %s)'''
    for i, c in enumerate(cla):
        if i == 0:
            args = (c, 1)
        else:
            args = (c, 2)
        pg.insert(sql, args)


def js_details():
    pg = Pg_db()
    tit = '老镇是一块思想的净土!'
    con = ''' 凤凰新媒体（纽交所代码：FENG)创建于1998年，是全球领先的跨平台网络新媒体公司，整合旗下综合门户凤凰网（www.ifeng.com）、手机凤凰网
                    （3g.ifeng.com）及移动客户端、凤凰视频（v.ifeng.com）三大平台，秉承"中华情怀，全球视野，包容开放，进步力量"的媒体理念，
                    为主流华人提
                    供互联网、移动互联网、视频跨平台整合无缝衔接的新媒体优质内容与服务。
                </p>
                <p>
                    <br>
                </p>
                <p>
                    凤凰新媒体不仅是控股的凤凰卫视传媒集团优质电视内容的网络传播渠道，更整合了众多专业媒体机构生产的内容、用户生成的内容、以及自身生产的
                    专业内容，提供含图文音视频的全方位综合新闻资讯、深度报道、观点评论、财经产品、互动应用、分享社区、在线网页游戏等服务，满足主流人群浏
                    览、表达、交流、分享、娱乐、理财等多元化与个性化的诉求，并反向传输给凤凰卫视的电视平台，形成创新的网台联动组合传播模式，为互联网、移
                    动互联网及视频用户提供丰富的内容与随时随地随身的服务。
                </p>
                <p>
                    <br>
                </p>
                <p>
                    凤凰网目前日均浏览界面6.87亿，日均覆盖用户数（UV）约4687万，月度覆盖用户数近4.2亿，移动端累计月度覆盖用户数3亿。根据艾瑞2014年报告
                    显示，凤凰网用户的月均收入、家庭经济状况、受教育程度、管理层和专业人员的比例、单个访问者浏览的页面PV/UV比、日均有效浏览时间等指标
                    在中国互联网门户网站中均处于领先水平。凤凰新媒体以其独特的受众精准性、内容洞察力、平台整合力、及品牌影响力为媒体营销价值核心，为广告
                    客户提供高效的营销投资回报（4I for ROI）。
                </p>
                <p>
                    <br>
                </p>
                <p>
                    在宽带与移动互联网带来颠覆性革新及新旧媒体融合的时代，凤凰新媒体将继续引领互联网、移动互联网、电视的联动组合传播与3G/4G时代的媒体化
                    创新。
                </p>
                <p>
                    <br>
                </p>'''
    clas = pg.query('select c_id, c_name from js_classes WHERE c_level=2')
    sql = 'insert into js_details(d_tit, d_con, d_pclassid) values(%s, %s, %s)'
    for c_id, c_name in clas:
        args = (
            tit + '/' + c_name,
            '<p>' + c_name + '/' + con,
            c_id
        )
        pg.insert(sql, args)


if __name__ == '__main__':
    # lz_details()
    # shq_hotCitys()
    # shq_mainInfo()
    # shq_detailClass()
    # shq_arealinks()
    # qy_hots()
    # lz_indexslider()
    # qy_slider()
    # qy_filterclass()
    # qy_subfilter()
    # qy_links()
    # qy_nofilterclass()
    # qy_nofilterlinks()
    # dx_hots()
    # dx_slider()
    # dx_links()
    # e_hots()
    # e_left()
    # e_slider()
    # e_right()
    # e_lowRight()
    # e_links()
    # js_classes()
    js_details()
