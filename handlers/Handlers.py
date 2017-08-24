# -*- coding:utf-8 -*-

from BaseHandler import BaseHandler
from tornado import gen, httpclient
from datetime import datetime
from lxml import etree
import math
import logging
import constants


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        data = {'classes': []}
        classes_1 = yield self.query('select  c_id, c_name from '
                                     'lz_classes '
                                     'where c_level=1;')
        footer_cla = yield self.query('select c_name from js_classes where '
                                      'c_level=2')
        nav_hots = []
        for c in classes_1:
            cid = c['c_id']
            cl = c['c_name']
            sub_cla = yield self.query('select c_name from lz_classes '
                                       'where '
                                       'c_level=2 and c_pid=%s;', (cid,))
            if cid == 1:
                len_sub_cla = len(sub_cla)
                for n in range(len_sub_cla):
                    hot = yield self.query(
                        'select d_desc, d_url from lz_details where d_class_id=6+%s and d_hot_order is not null order by d_hot_order desc',
                        (n,))
                    nav_hots.append(hot)
            data['classes'].append([cl, sub_cla])

        shq_hots = yield self.query('select hc_name, hc_num from shq_hotCitys '
                                    'order by hc_order limit 6;')
        qy_hots = yield self.query('select h_url, h_desc from qy_hots order by '
                                   'h_order desc;')
        dx_hots = yield self.query('select h_url, h_desc from dx_hots')

        e_hots = yield self.query('select h_url, h_desc from e_hots')

        slides = []
        for i in range(10):
            sli = yield self.query('select a.d_img, a.d_url from '
                                   'lz_details a LEFT JOIN lz_classes b on '
                                   'd_class_id=c_id where d_class_id=%s+6;',
                                   (i,))
            slides.append(sli)
        mid_sliders = []
        for i in range(4):
            m_sli = yield self.query('select is_url, is_img, is_classid '
                                     'from '
                                     'lz_indexslider where is_classid=%s+2 and'
                                     ' is_pos=1;', (i,))
            mid_sliders.append(m_sli)
        right_sliders = []
        for i in range(4):
            r_sli = yield self.query('select is_url, is_img, '
                                     'is_classid from '
                                     'lz_indexslider where '
                                     'is_classid=%s+2 '
                                     'and is_pos=2', (i,))
            right_sliders.append(r_sli)

        self.render('index.html', footer_cla=footer_cla, data=data,
                    slides=slides, nav_hots=nav_hots, shq_hots=shq_hots,
                    qy_hots=qy_hots, mid_sli=mid_sliders,
                    right_sli=right_sliders, dx_hots=dx_hots, e_hots=e_hots)


class IntoClassHandler(BaseHandler):
    @gen.coroutine
    def get(self, cid, sub_cla_id):
        change = self.get_argument('change', '')
        cla_name = yield self.query('select c_name from lz_classes where '
                                    'c_id=%s+1;', (cid,))
        footer_cla = yield self.query('select c_name from js_classes where '
                                      'c_level=2')
        if cid == '0':
            hot = yield self.query(
                'select d_url, d_desc from lz_details where d_class_id=%s+6 '
                'and d_hot_order is not null ORDER by d_hot_order desc',
                (sub_cla_id,))
            details = yield self.query('select a.d_img, a.d_url from '
                                       'lz_details a LEFT JOIN lz_classes b on '
                                       'd_class_id=c_id where d_class_id=%s+6;',
                                       (sub_cla_id,))
            if change == '1':
                self.write(dict(hot=hot, details=details))
                self.finish()
                return
            sub_cla = yield self.query('select c_name from lz_classes where '
                                       'c_level=2 and c_pid=%s+1;', (cid,))
            self.render('nav_index0.html', cid=cid, cla_name=cla_name[0],
                        footer_cla=footer_cla,
                        hot=hot, sub_cla=sub_cla, details=details)
        if cid == '1':
            self.render('nav_index1.html', cid=cid, cla_name=cla_name[0],
                        footer_cla=footer_cla, )
        if cid == '2':
            qy_hots = yield self.query(
                'select h_url, h_desc from qy_hots order by '
                'h_order desc;')
            qy_classes = yield self.query('select c_name from lz_classes where '
                                          'c_pid=3')
            self.render('nav_index2.html', cid=cid, cla_name=cla_name[0],
                        footer_cla=footer_cla,
                        qy_hots=qy_hots, qy_classes=qy_classes)
        if cid == '3':
            dx_hots = yield self.query('select h_url, h_desc from dx_hots')
            dx_classes = yield self.query('select c_name from lz_classes where '
                                          'c_pid=4')
            self.render('nav_index3.html', cid=cid, cla_name=cla_name[0],
                        footer_cla=footer_cla,
                        dx_hots=dx_hots, dx_classes=dx_classes)
        if cid == '4':
            e_classes = yield self.query(
                'select c_name from lz_classes where c_pid=5')
            e_left = yield self.query('select l_url, l_desc from e_left')
            e_slider = yield self.query(
                'select s_url, s_img, s_desc from e_slider')
            e_right = yield self.query(
                'select r_url, r_img, r_desc from e_right')
            e_lowRight = yield self.query('select lr_url, lr_img, lr_desc from '
                                          'e_lowright')
            e_all = yield self.query('select l_url, l_img, l_desc from e_links')
            e_sub0 = yield self.query(
                'select l_url, l_img, l_desc from e_links '
                'where l_pclassid=39')
            e_sub1 = yield self.query(
                'select l_url, l_img, l_desc from e_links '
                'where l_pclassid=40')
            e_sub2 = yield self.query(
                'select l_url, l_img, l_desc from e_links '
                'where l_pclassid=41')
            e_sub3 = yield self.query(
                'select l_url, l_img, l_desc from e_links '
                'where l_pclassid=42')
            e_sub4 = yield self.query(
                'select l_url, l_img, l_desc from e_links '
                'where l_pclassid=43')
            self.render('nav_index4.html', cid=cid, cla_name=cla_name[0],
                        footer_cla=footer_cla,
                        e_left=e_left, e_slider=e_slider,
                        e_right=e_right, e_lowRight=e_lowRight, e_all=e_all,
                        e_sub0=e_sub0, e_sub1=e_sub1, e_sub2=e_sub2,
                        e_sub3=e_sub3, e_sub4=e_sub4, e_classes=e_classes)
        if cid == '6':
            cl = yield self.query(
                'select c_name from js_classes where c_level=1')
            sub_cl = yield self.query('select c_name from js_classes where '
                                      'c_level=2')
            details = yield self.query(
                'select d_tit, d_con from js_details where '
                'd_pclassid=%s+2;', (sub_cla_id,))
            self.render('nav_index6.html', cl=cl, footer_cla=footer_cla,
                        sub_cl=sub_cl, details=details)

    @gen.coroutine
    def post(self, cid, sub_cla_id):
        sub_id = self.json_args.get('sub_id', '')
        if cid == '6':
            details = yield self.query('select d_tit, d_con from js_details '
                                       'where d_pclassid=%s+2;', (sub_id,))
            self.write({'details': details})
            # gen.Return({'details': details})


class ShqInfoHandler(BaseHandler):
    # '生活圈详情分类信息获取'
    @gen.coroutine
    def get(self):
        sel = self.get_argument('sel', '')
        area = self.get_argument('area', '')
        dc_ind = self.get_argument('dc_ind', '')
        page = self.get_argument('page', '')
        # print sel, area, dc_ind,type(dc_ind)
        d_names = yield self.query(
            'select dc_name from shq_detailclass a LEFT JOIN lz_classes b on a.dc_pclass_id=b.c_id WHERE b.c_name=%s;',
            (sel,))
        # print d_names, type(d_names)
        dc_name = d_names[int(dc_ind)]['dc_name']
        # print dc_name
        if area[-2:] == '00':
            sql = 'SELECT al_img,al_url,al_desc FROM (shq_arealinks a LEFT JOIN shq_detailclass b ON a.al_declass_id = b.dc_id) c LEFT JOIN lz_classes d ON c.dc_pclass_id=d.c_id where c_name=%s and dc_name=%s and al_areaid BETWEEN %s and %s limit %s'
            args = [sel, dc_name, int(area), int(area) + 100,
                    6]
            if int(page):
                sql += ' offset %s'
                args.append((int(page) - 1) * 6)
                d_info = yield self.query(sql, tuple(args))
                self.write({'d_info': d_info})
                self.finish()
                return
            totle = yield self.query('SELECT COUNT(*) FROM ('
                                     'shq_arealinks a LEFT JOIN shq_detailclass b ON a.al_declass_id = b.dc_id) c LEFT JOIN lz_classes d ON c.dc_pclass_id=d.c_id where c_name=%s and dc_name=%s and al_areaid BETWEEN %s and %s',
                                     (sel, dc_name, int(area),
                                      int(area) + 100))
            print sql, args
            d_info = yield self.query(sql, tuple(args))
        elif not area:
            logging.error('no area args')
            self.finish()
            return
        else:
            sql = 'SELECT al_img,al_url,al_desc,dc_name FROM (shq_arealinks a LEFT JOIN shq_detailclass b ON a.al_declass_id = b.dc_id) c LEFT JOIN lz_classes d ON c.dc_pclass_id=d.c_id where c_name=%s and al_areaid =%s and dc_name=%s limit %s'
            args = [sel, area, dc_name, 6]
            if int(page):
                sql += ' offset %s'
                args.append((int(page) - 1) * 6)
                print sql, args
                d_info = yield self.query(sql, tuple(args))
                self.write({'d_info': d_info})
                self.finish()
                return
            totle = yield self.query(
                'SELECT COUNT(*) FROM (shq_arealinks a LEFT JOIN shq_detailclass b ON a.al_declass_id = b.dc_id) c LEFT JOIN lz_classes d ON c.dc_pclass_id=d.c_id where c_name=%s and al_areaid =%s and dc_name=%s',
                (sel, area, dc_name))
            d_info = yield self.query(sql, tuple(args))
        totle = math.ceil(float(totle[0]['count']) / 6)
        self.write({'d_names': d_names, 'd_info': d_info, 'totle': totle})

    # '生活圈首页市级信息ajax接口'
    @gen.coroutine
    def post(self):
        city = self.json_args.get('city')
        page = self.json_args.get('page')
        # print 'args = ', city, page
        if int(page):
            main_info_3 = yield self.query(
                'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s and mi_pos=3 limit %s offset %s',
                (city, constants.PAGE_CAPACITY,
                 (int(page) - 1) * constants.PAGE_CAPACITY))
            main_info = {
                "mi_3": main_info_3
            }
            # print 'main_info', main_info
            # print "select mi_url, mi_desc, mi_img from shq_maininfo where " \
            #       "mi_city=%s and mi_pos=3 limit %s offset %s" % (city,
            #                                                       constants.PAGE_CAPACITY,
            #                                                       (int(
                                                                      # page) - 1) * constants.PAGE_CAPACITY)
            self.write({'main_info': main_info})
            self.finish()
            return
        else:
            totle = yield self.query(
                'select count(*) from shq_maininfo where mi_city=%s and mi_pos=3',
                (city,))
            main_info_11 = yield self.query(
                'select mi_url, mi_img from shq_maininfo where mi_city=%s and '
                'mi_pos=11', (city,))
            main_info_12 = yield self.query(
                'select mi_url, mi_desc from shq_maininfo where mi_city=%s and '
                'mi_pos=12', (city,)
            )
            main_info_211 = yield self.query(
                'select mi_url, mi_desc from shq_maininfo where mi_city=%s and '
                'mi_pos=211', (city,)
            )
            main_info_212 = yield self.query(
                'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s '
                'and '
                'mi_pos=212', (city,)
            )
            main_info_221 = yield self.query(
                'select mi_url, mi_desc from shq_maininfo where mi_city=%s and '
                'mi_pos=221', (city,)
            )
            main_info_222 = yield self.query(
                'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s '
                'and '
                'mi_pos=222', (city,)
            )
            main_info_3 = yield self.query(
                'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s '
                'and mi_pos=3 limit %s', (city, constants.PAGE_CAPACITY)
            )
            main_info = {
                "totle": math.ceil(float(totle[0][
                                             'count']) / constants.PAGE_CAPACITY),
                "mi_11": main_info_11,
                "mi_12": main_info_12,
                "mi_211": main_info_211,
                "mi_212": main_info_212,
                "mi_221": main_info_221,
                "mi_222": main_info_222,
                "mi_3": main_info_3
            }
            # print 'main_info', main_info
            self.write({'main_info': main_info})


class QyInfoHandler(BaseHandler):
    # '企业之友详细链接信息获取'
    # TODO:query slow
    @gen.coroutine
    def get(self):
        cla_ind = self.get_argument('cla_ind', '')
        filter_cla = self.get_argument('filter_cla', '')
        sub_filter = self.get_argument('sub_filter', '')
        area_num = self.get_argument('area_num', '')
        page = self.get_argument('page', '')
        print '-***-'.join([cla_ind, filter_cla, sub_filter, area_num, page])
        if int(cla_ind) in (0, 3, 4):
            if not filter_cla:
                filter_cla = yield self.query(
                    'select fc_name from qy_filterclass '
                    'where fc_pclassid=%s+26',
                    (cla_ind,))
                sliders = yield self.query('select s_url, s_img from '
                                           'qy_slider where s_classid=%s+26',
                                           (cla_ind,))
                self.write({'filter': filter_cla, 'sliders': sliders})
                self.finish()
                return
            else:
                if not sub_filter:
                    # print 'sub', filter_cla
                    sub_filter = yield self.query('select sf_name from '
                                                  'qy_subfilter a LEFT JOIN '
                                                  'qy_filterclass b on a'
                                                  '.sf_pclassid=b.fc_id where '
                                                  'fc_name=%s', (filter_cla,))
                    self.write({'sub_filter': sub_filter})
                    self.finish()
                    return
                else:
                    sql = 'select l_url, l_img, l_desc from qy_links a'
                    args = []
                    if filter_cla == u'全部' and sub_filter == u'全部':
                        sql += ' left join qy_subfilter b on ' \
                               'a.l_pclassid=b.sf_id left join ' \
                               'qy_filterclass c on sf_pclassid=fc_id ' \
                               'where fc_pclassid=%s+26'
                        args.append(cla_ind)
                    if filter_cla != u'全部' and sub_filter == u'全部':
                        sql += ' left join qy_subfilter b on ' \
                               'a.l_pclassid = b.sf_id LEFT JOIN ' \
                               'qy_filterclass c on sf_pclassid = ' \
                               'fc_id where fc_name=%s'
                        args.append(filter_cla)
                    if filter_cla != u'全部' and sub_filter != u'全部':
                        sql += ' left join qy_subfilter b on ' \
                               'a.l_pclassid = b.sf_id LEFT JOIN ' \
                               'qy_filterclass c on sf_pclassid = ' \
                               'fc_id where sf_name=%s'
                        args.append(sub_filter)

                    if area_num[-4:] == '0000':
                        if sql[-1] == 'a':
                            sql += ' where a.l_areanum between %s and %s ' \
                                   '+ 10000'
                        else:
                            sql += ' and a.l_areanum between %s and %s + ' \
                                   '10000'
                        args.append(area_num)
                        args.append(area_num)
                    elif area_num[-2:] == '00':
                        if sql[-1] == 'a':
                            sql += ' where a.l_areanum between %s and %s + 100'
                        else:
                            sql += ' and a.l_areanum between %s and %s + ' \
                                   '100'
                        args.append(area_num)
                        args.append(area_num)
                    elif area_num == '':
                        pass
                    else:
                        sql += ' and a.l_areanum=%s'
                        args.append(area_num)

                    totle = yield self.query(
                        sql.replace('l_url, l_img, l_desc', 'count(*)'),
                        tuple(args))

                    sql += ' limit %s'
                    args.append(constants.PAGE_CAPACITY)
                    if int(page):
                        sql += ' offset %s'
                        args.append((int(page) - 1) * constants.PAGE_CAPACITY)
                        ret = yield self.query(sql, tuple(args))
                        print 'sql ====', sql
                        print 'args ====', tuple(args)
                        print 'ret ====', ret
                        self.write({'ret': ret})
                        self.finish()
                        return
                    totle = math.ceil(
                        float(totle[0]['count']) / constants.PAGE_CAPACITY)
                    ret = yield self.query(sql, tuple(args))
                    print 'sql ====', sql
                    print 'args ====', tuple(args)
                    print 'ret ====', ret
                    self.write({'ret': ret, 'totle': totle})

        elif int(cla_ind) in (1, 2):
            de_cla = yield self.query('select nfc_id, nfc_name from '
                                      'qy_nofilterclass '
                                      'where nfc_pclassid=%s+26', (cla_ind,))
            detail = []
            for de_c in de_cla:
                nfc_id = de_c['nfc_id']
                de = yield self.query('select nfl_url, nfl_img, '
                                      'nfl_desc from qy_nofilterlinks '
                                      'where nfl_pclassid=%s', (nfc_id,))
                detail.append(de)
            # print 'detail=', detail
            self.write({'de_cla': de_cla, 'detail': detail})
        else:
            pass


class DxInfoHandler(BaseHandler):
    # '导学详细信息获取'

    @gen.coroutine
    def get(self):
        cla_ind = self.get_argument('cla_ind', '')
        area_num = self.get_argument('area_num', '')
        page = self.get_argument('page', '')
        sql = 'select l_url, l_img, l_desc from dx_links where ' \
              'l_pclassid=%s+31'
        count_sql = 'select count(*) from dx_links where l_pclassid=%s+31'
        args = [cla_ind, area_num, area_num]
        # print 'args=', args
        if not area_num:
            slider = yield self.query(
                'select s_url, s_img from dx_slider where '
                's_pclassid=%s+31', (cla_ind,))
            # print 'slider=', slider
            self.write({'slider': slider})
            self.finish()
            return
        elif area_num[-4:] == '0000':
            sql += ' and l_areanum between %s and %s + 10000'
            count_sql += ' and l_areanum between %s and %s + 10000'
        elif area_num[-2:] == '00':
            sql += ' and l_areanum between %s and %s + 100'
            count_sql += ' and l_areanum between %s and %s + 100'
        else:
            sql += ' and l_areanum=%s'
            count_sql += ' and l_areanum=%s'
            args.pop()
        count = yield self.query(
            sql.replace('l_url, l_img, l_desc', 'count(*)'), tuple(args))
        print 'count_sql=', count_sql
        print 'args=', args
        print 'count=', count
        totle = math.ceil(float(count[0]['count'] / constants.PAGE_CAPACITY))
        sql += ' limit %s' % constants.PAGE_CAPACITY
        if int(page):
            sql += ' offset %s'
            args.append((int(page) - 1) * constants.PAGE_CAPACITY)
            links = yield self.query(sql, tuple(args))
            self.write({'links': links})
            self.finish()
            return
        links = yield self.query(sql, tuple(args))
        # print 'count=', count
        # print 'sql ====', sql
        # print 'args ====', tuple(args)
        # print 'ret ====', links
        self.write({'links': links, 'totle': totle, 'count': count[0]['count']})


class DateInfoHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        query = str(datetime.now())
        try:
            solarTerm = self.redis.get('solar_term_%s' % query[:10])
        except Exception as e:
            logging.error(e)
            solarTerm = None
        if solarTerm:
            self.write(dict(solarTerm=solarTerm))
            self.finish()
            return

        http_client = httpclient.AsyncHTTPClient()
        xpath_query = query[:4] + '月' + query[5:7] + '月' + query[8:10] + '日'
        resp = yield http_client.fetch(
            'https://wannianrili.51240.com/ajax/?q=' + query[:7])
        # print '-----resp======', resp, '----type----', type(resp.body)
        page = etree.HTML(resp.body.decode('utf-8'))
        solarTerm = page.xpath(
            u'//span[text()="' + unicode(xpath_query,
                                         'utf-8') + u' 详细信息"]/../following::div['
                                                    u'1]//span[text('
                                                    u')="节气"]/following::span[1]')
        # print len(solarTerm), solarTerm, type(solarTerm[0].text)
        solarTerm_ret = solarTerm[0].text.replace(u'下一个节气', '').replace(u'，还有',
                                                                        '')

        try:
            self.redis.setex('solar_term_%s' % query[:10],
                             constants.SOLAR_TERM_EXPIRE_SECONDS,
                             solarTerm_ret)
        except Exception as e:
            logging.error(e)
        self.write(dict(solarTerm=solarTerm_ret))
