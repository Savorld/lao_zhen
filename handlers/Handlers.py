# -*- coding:utf-8 -*-

from BaseHandler import BaseHandler
from tornado import gen
from tornado.web import asynchronous
import json
import logging
from pprint import pprint


class Indexhandler(BaseHandler):
    def get(self):
        data = {'classes': []}
        classes_1 = self.db.query('select  c_id, c_name from lz_classes '
                                  'where c_level=1;')
        nav_hots = []
        len_sub_cla = None
        for cid, cl in classes_1:
            sub_cla = self.db.query('select c_name from lz_classes '
                                    'where '
                                    'c_level=2 and c_pid=%s;', (cid,))
            if cid == 1:
                len_sub_cla = len(sub_cla)
            data['classes'].append([cl, sub_cla])

        for n in range(len_sub_cla):
            nav_hots.append(self.db.query(
                'select d_desc, d_url from lz_details where d_class_id=6+%s and d_hot_order is not null order by d_hot_order desc',
                (n,)))

        slides = []
        for i in range(10):
            slides.append(self.db.query('select a.d_img, a.d_url from '
                                        'lz_details a LEFT JOIN lz_classes b on '
                                        'd_class_id=c_id where d_class_id=%s+6;',
                                        (i,)))

        shq_hots = self.db.query('select hc_name, hc_num from shq_hotCitys '
                                 'order by hc_order limit 6;')
        qy_hots = self.db.query('select h_url, h_desc from qy_hots order by '
                                'h_order desc;')
        mid_sliders = []
        for i in range(4):
            mid_sliders.append(
                self.db.query('select is_url, is_img, is_classid '
                              'from '
                              'lz_indexslider where is_classid=%s+2 and'
                              ' is_pos=1;', (i,)))
        right_sliders = []
        for i in range(4):
            right_sliders.append(self.db.query('select is_url, is_img, '
                                               'is_classid from '
                                               'lz_indexslider where '
                                               'is_classid=%s+2 '
                                               'and is_pos=2', (i,)))

        dx_hots = self.db.query('select h_url, h_desc from dx_hots')

        e_hots = self.db.query('select h_url, h_desc from e_hots')

        self.render('index.html', data=data, slides=slides,
                    nav_hots=nav_hots, shq_hots=shq_hots, qy_hots=qy_hots,
                    mid_sli=mid_sliders, right_sli=right_sliders,
                    dx_hots=dx_hots, e_hots=e_hots)


class IntoClassHandler(BaseHandler):

    def get(self, cid, sub_cla_id):
        cla_name = self.db.query('select c_name from lz_classes where '
                                 'c_id=%s+1;', (cid,))
        hot = self.db.query(
            'select d_desc from lz_details where d_class_id=%s+6 and '
            'd_hot_order is not null ORDER by d_hot_order desc',
            (sub_cla_id,))
        sub_cla = self.db.query('select c_name from lz_classes where '
                                'c_level=2 and c_pid=%s+1;', (cid,))
        details = self.db.query('select a.d_img, a.d_url from '
                                'lz_details a LEFT JOIN lz_classes b on '
                                'd_class_id=c_id where d_class_id=%s+6;',
                                (sub_cla_id,))

        qy_hots = self.db.query('select h_url, h_desc from qy_hots order by '
                                'h_order desc;')
        qy_classes = self.db.query('select c_name from lz_classes where '
                                   'c_pid=3')

        dx_hots = self.db.query('select h_url, h_desc from dx_hots')
        dx_classes = self.db.query('select c_name from lz_classes where '
                                   'c_pid=4')

        e_classes = self.db.query('select c_name from lz_classes where c_pid=5')
        e_left = self.db.query('select l_url, l_desc from e_left')
        e_slider = self.db.query('select s_url, s_img, s_desc from e_slider')
        e_right = self.db.query('select r_url, r_img, r_desc from e_right')
        e_lowRight = self.db.query('select lr_url, lr_img, lr_desc from '
                                   'e_lowright')
        e_all = self.db.query('select l_url, l_img, l_desc from e_links')
        e_sub0 = self.db.query('select l_url, l_img, l_desc from e_links '
                               'where l_pclassid=39')
        e_sub1 = self.db.query('select l_url, l_img, l_desc from e_links '
                               'where l_pclassid=40')
        e_sub2 = self.db.query('select l_url, l_img, l_desc from e_links '
                               'where l_pclassid=41')
        e_sub3 = self.db.query('select l_url, l_img, l_desc from e_links '
                               'where l_pclassid=42')
        e_sub4 = self.db.query('select l_url, l_img, l_desc from e_links '
                               'where l_pclassid=43')
        if cid == u'6':
            cl = self.db.query('select c_name from js_classes where c_level=1')
            sub_cl = self.db.query('select c_name from js_classes where '
                                   'c_level=2')
            details = self.db.query('select d_tit, d_con from js_details where '
                                    'd_pclassid=%s+2;', (sub_cla_id,))
            self.render('nav_index6.html', cl=cl,
                        sub_cl=sub_cl, details=details)
        self.render('nav_index%s.html' % cid, cid=cid, cla_name=cla_name[0],
                    hot=hot, sub_cla=sub_cla, details=details,
                    qy_hots=qy_hots, qy_classes=qy_classes, dx_hots=dx_hots,
                    dx_classes=dx_classes, e_left=e_left, e_slider=e_slider,
                    e_right=e_right, e_lowRight=e_lowRight, e_all=e_all,
                    e_sub0=e_sub0, e_sub1=e_sub1, e_sub2=e_sub2,
                    e_sub3=e_sub3, e_sub4=e_sub4, e_classes=e_classes)
    # @asynchronous
    # @gen.coroutine
    def post(self, cid, sub_cla_id):
        sub_id = self.json_args.get('sub_id', '')
        if cid == '6':
            details = yield self.db.query('select d_tit, d_con from js_details '
                                          'where d_pclassid=%s+2;', (sub_id,))
            self.write({'details': details})
            # gen.Return({'details': details})


class ShqInfoHandler(BaseHandler):
    # '生活圈详情分类信息获取'
    def get(self):
        sel = self.get_argument('sel', '')
        area = self.get_argument('area', '')
        dc_ind = self.get_argument('dc_ind', '')
        # print sel, area, dc_ind,type(dc_ind)
        # logging.info('sel', sel)
        d_names = self.db.query(
            'select dc_name from shq_detailclass a LEFT JOIN lz_classes b on a.dc_pclass_id=b.c_id WHERE b.c_name=%s;',
            (sel,))
        print d_names, type(d_names)
        dc_name = d_names[int(dc_ind)][0]
        print dc_name
        if area[-2:] == '00':
            d_info = self.db.query(
                'SELECT al_img,al_url,al_desc FROM (shq_arealinks a LEFT JOIN '
                'shq_detailclass '
                'b ON a.al_declass_id = '
                'b.dc_id) c LEFT JOIN lz_classes d ON '
                'c.dc_pclass_id=d.c_id where c_name=%s and dc_name=%s and '
                'al_areaid '
                'BETWEEN %s and %s;',
                (sel, dc_name, int(area), int(area) + 100))

        elif not area:
            d_info = None
            logging.error('no area args')

        else:
            d_info = self.db.query(
                'SELECT al_img,al_url,al_desc,dc_name FROM (shq_arealinks a '
                'LEFT JOIN '
                'shq_detailclass '
                'b ON a.al_declass_id = '
                'b.dc_id) c LEFT JOIN lz_classes d ON '
                'c.dc_pclass_id=d.c_id where c_name=%s and al_areaid =%s and '
                'dc_name=%s;',
                (sel, area, dc_name))

        self.write({'d_names': d_names, 'd_info': d_info})

    # '生活圈首页市级信息ajax接口'
    def post(self):
        city = self.json_args.get('city')
        main_info_11 = self.db.query(
            'select mi_url, mi_img from shq_maininfo where mi_city=%s and '
            'mi_pos=11', (city,))
        main_info_12 = self.db.query(
            'select mi_url, mi_desc from shq_maininfo where mi_city=%s and '
            'mi_pos=12', (city,)
        )
        main_info_211 = self.db.query(
            'select mi_url, mi_desc from shq_maininfo where mi_city=%s and '
            'mi_pos=211', (city,)
        )
        main_info_212 = self.db.query(
            'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s '
            'and '
            'mi_pos=212', (city,)
        )
        main_info_221 = self.db.query(
            'select mi_url, mi_desc from shq_maininfo where mi_city=%s and '
            'mi_pos=221', (city,)
        )
        main_info_222 = self.db.query(
            'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s '
            'and '
            'mi_pos=222', (city,)
        )
        main_info_3 = self.db.query(
            'select mi_url, mi_desc, mi_img from shq_maininfo where mi_city=%s '
            'and '
            'mi_pos=3', (city,)
        )
        main_info = {
            "mi_11": main_info_11,
            "mi_12": main_info_12,
            "mi_211": main_info_211,
            "mi_212": main_info_212,
            "mi_221": main_info_221,
            "mi_222": main_info_222,
            "mi_3": main_info_3
        }
        # print 'main_info',main_info
        self.write({'main_info': main_info})


class QyInfoHandler(BaseHandler):
    # '企业之友详细链接信息获取'
    def get(self):
        cla_ind = self.get_argument('cla_ind', '')
        filter_cla = self.get_argument('filter_cla', '')
        sub_filter = self.get_argument('sub_filter', '')
        area_num = self.get_argument('area_num', '')
        print '-***-'.join([cla_ind, filter_cla, sub_filter, area_num])
        if int(cla_ind) in (0, 3, 4):
            print '1'
            if not filter_cla:
                print '2', filter_cla
                filter_cla = self.db.query('select fc_name from qy_filterclass '
                                           'where fc_pclassid=%s+26',
                                           (cla_ind,))
                sliders = self.db.query('select s_url, s_img from '
                                        'qy_slider where s_classid=%s+26',
                                        (cla_ind,))
                self.write({'filter': filter_cla, 'sliders': sliders})
            else:
                if not sub_filter:
                    print 'sub', filter_cla
                    sub_filter = self.db.query('select sf_name from '
                                               'qy_subfilter a LEFT JOIN '
                                               'qy_filterclass b on a'
                                               '.sf_pclassid=b.fc_id where '
                                               'fc_name=%s', (filter_cla,))
                    self.write({'sub_filter': sub_filter})
                else:
                    print '4'
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

                    sql += ' limit 8'
                    print 'sql ====', sql
                    print 'args ====', tuple(args)
                    ret = self.db.query(sql, tuple(args))
                    print 'ret ====', ret
                    self.write({'ret': ret})

        elif int(cla_ind) in (1, 2):
            print '5'
            de_cla = self.db.query('select nfc_id, nfc_name from '
                                   'qy_nofilterclass '
                                   'where nfc_pclassid=%s+26', (cla_ind,))
            detail = []
            for nfc_id, nfc in de_cla:
                detail.append(self.db.query('select nfl_url, nfl_img, '
                                            'nfl_desc from qy_nofilterlinks '
                                            'where nfl_pclassid=%s', (nfc_id,)))
            self.write({'de_cla': de_cla, 'detail': detail})
        else:
            pass


class DxInfoHandler(BaseHandler):
    # '导学详细信息获取'
    def get(self):
        cla_ind = self.get_argument('cla_ind', '')
        area_num = self.get_argument('area_num', '')
        sql = 'select l_url, l_img, l_desc from dx_links where ' \
              'l_pclassid=%s+31'
        count = 'select count(*) from dx_links where l_pclassid=%s+31'
        args = [cla_ind, area_num, area_num]
        if not area_num:
            slider = self.db.query('select s_url, s_img from dx_slider where '
                                   's_pclassid=%s+31', (cla_ind,))

            self.write({'slider': slider})
        elif area_num[-4:] == '0000':
            sql += ' and l_areanum between %s and %s + 10000'
            count += ' and l_areanum between %s and %s + 10000'
        elif area_num[-2:] == '00':
            sql += ' and l_areanum between %s and %s + 100'
            count += ' and l_areanum between %s and %s + 100'
        else:
            sql += ' and l_areanum=%s'
            count += ' and l_areanum=%s'
            args.pop()
        links = self.db.query(sql, tuple(args))
        count = self.db.query(count, tuple(args))
        # print 'sql ====', sql
        # print 'args ====', tuple(args)
        # print 'ret ====', links
        self.write({'links': links, 'count': count})
