import pandas as pd
import csv
from pyecharts import options as opts
from pyecharts.charts import Map, Tab, Line, Grid
province = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾',
              '内蒙古', '广西', '西藏', '宁夏', '新疆',
              '北京', '天津', '上海', '重庆',
              '香港', '澳门']

# '日期', '省份', '城市', '新增确诊', '新增出院', '新增死亡', '消息来源'


def input():
    data = open('Updates_NC.csv', 'r')
    city_list = list(csv.reader(data))
    city_list = city_list[1:]
    for row in city_list:
        """
            纠正地级市名称
        """
        if row[2]=="恩施州":
            row[2] = "恩施土家族苗族自治州"
        elif row[2]=="湘西州":
            row[2] = "湘西土家族苗族自治州"
        elif row[2] == "阿坝州":
            row[2] = "阿坝藏族羌族自治州"
        elif row[2] == "甘孜州":
            row[2] = "甘孜藏族自治州"
        elif row[2] == "凉山州":
            row[2] = "凉山彝族自治州"
        elif row[2] == "黔西南州":
            row[2] = "黔西南布依族苗族自治州"
        elif row[2] == "黔东南州":
            row[2] = "黔东南苗族侗族自治州"
        elif row[2] == "黔南州":
            row[2] = "黔南布依族苗族自治州"
        elif row[2] == "楚雄州":
            row[2] = "楚雄彝族自治州"
        elif row[2] == "红河州":
            row[2] = "红河哈尼族彝族自治州"
        elif row[2] == "文山州":
            row[2] = "文山壮族苗族自治州"
        elif row[2] == "西双版纳州":
            row[2] = "西双版纳傣族自治州"
        elif row[2] == "大理州":
            row[2] = "大理白族自治州"
        elif row[2] == "德宏州":
            row[2] = "德宏傣族景颇族自治州"
        elif row[2] == "怒江州":
            row[2] = "怒江傈僳族自治州"
        elif row[2] == "迪庆州":
            row[2] = "迪庆藏族自治州"
        elif row[2] == "临夏州":
            row[2] = "临夏回族自治州"
        elif row[2] == "甘南州":
            row[2] = "甘南藏族自治州"
        elif row[2] == "海北州":
            row[2] = "海北藏族自治州"
        elif row[2] == "黄南州":
            row[2] = "黄南藏族自治州"
        elif row[2] == "海南州":
            row[2] = "海南藏族自治州"
        elif row[2] == "果洛州":
            row[2] = "果洛藏族自治州"
        elif row[2] == "玉树州":
            row[2] = "玉树藏族自治州"
        elif row[2] == "海西州":
            row[2] = "海西蒙古族藏族自治州"
        elif row[2] == "昌吉州":
            row[2] = "昌吉回族自治州"
        elif row[2] == "博尔塔拉蒙古州":
            row[2] = "博尔塔拉蒙古自治州"
        elif row[2] == "巴音郭楞蒙古州":
            row[2] = "巴音郭楞蒙古自治州"
        elif row[2] == "克孜勒苏柯尔克孜州":
            row[2] = "克孜勒苏柯尔克孜自治州"
        elif row[2] == "伊犁州":
            row[2] = "伊犁哈萨克自治州"
        """
            改为整数形式
        """
        row[3] = to_int(row[3])
        row[4] = to_int(row[4])
        row[5] = to_int(row[5])
        """
            处理日期
        """
        str = row[0][:-1].split('月')

        row[0] = str[0].zfill(2) + '/' + str[1].zfill(2)
        # print(row[0])
    return city_list


def to_int(x):
    if x:
        return int(x)
    return 0

"""
导出全国新冠肺炎累计确诊人数、现在确诊人数、累计治愈人数、死亡人数
"""
def china_total(city_list):

    china_dict = {}
    # print(city_list)
    for name in province:
        china_dict.update({name: [0, 0, 0]})
    for row in city_list:
        name = row[1]
        if name in province:
            day = china_dict[name]
            china_dict[name] = [day[0]+row[3], day[1]+row[4], day[2]+row[5]]

    print(china_dict)

    confirm = [(k, v[0]) for k, v in china_dict.items()]
    heal = [(k, v[1]) for k, v in china_dict.items()]
    dead = [(k, v[2]) for k, v in china_dict.items()]
    current_confirm = [(k, v[0]-v[1]-v[2]) for k, v in china_dict.items()]
    tab = Tab()

    _map = (
        Map()
        .add('确诊人数', confirm, "china")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="新型冠状病毒全国疫情地图",
                                      subtitle="更新时间：{}".format(city_list[-1][0])),
            legend_opts=opts.LegendOpts(is_show=True),
            visualmap_opts=opts.VisualMapOpts(is_show=True, max_=1000,
                                              is_piecewise=True,
                                              pieces=[
                                                  # 数据范围
                                                  {"min": 10000, "label": ">=10000", "color": "#80707"},
                                                  {"max": 9999, "min": 1000, "label": "1000 - 9999 人", "color": "#8B0000"},
                                                  {"max": 999, "min": 500, "label": "500 - 999 人", "color": "#CB0000"},
                                                  {"max": 499, "min": 100, "label": "100 - 499 人", "color": "#DD5C5C"},
                                                  {"max": 99, "min": 10, "label": "10 - 99 人", "color": "#FFA07A"},
                                                  {"max": 9, "min": 1, "label": "1 - 9 人", "color": "#FFFF00"},
                                              ]
                                            #range_color=['#FFFFE0', '#FFA07A', '#CD5C5C', '#8B0000'])
        )
        )
        # .render("全国确诊.html")
    )
    tab.add(_map, "累计确诊")

    _map = (
        Map()
            .add('当前确诊人数', current_confirm, "china")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新型冠状病毒全国疫情地图",
                                      subtitle="更新时间：{}".format(city_list[-1][0])),
            legend_opts=opts.LegendOpts(is_show=True),
            visualmap_opts=opts.VisualMapOpts(is_show=True, max_=30,
                                              is_piecewise=True,
                                              range_color=['#FFFFE0', '#FFA07A', '#CD5C5C', '#8B0000'])
        )
            # .render("全国确诊.html")
    )
    tab.add(_map, "当前确诊")

    _map = (
        Map()
            .add('当前治愈人数', heal, "china")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新型冠状病毒全国疫情地图",
                                      subtitle="更新时间：{}".format(city_list[-1][0])),
            legend_opts=opts.LegendOpts(is_show=True),
            visualmap_opts=opts.VisualMapOpts(is_show=True, max_=1500,
                                              is_piecewise=True,
                                              pieces=[
                                                  # 数据范围
                                                  {"min": 10000, "label": ">=10000", "color": "#143601"},
                                                  {"max": 9999, "min": 1000, "label": "1000 - 9999 人",
                                                   "color": "#1A4301"},
                                                  {"max": 999, "min": 500, "label": "500 - 999 人", "color": "#245501"},
                                                  {"max": 499, "min": 300, "label": "300 - 499 人", "color": "#538D22"},
                                                  {"max": 299, "min": 100, "label": "100 - 299 人", "color": "#73A942"},
                                                  {"max": 99, "min": 0, "label": "1 - 99 人", "color": "#AAD576"},
                                              ]
                                              )
        )
            # .render("全国确诊.html")
    )
    tab.add(_map, "累计治愈")

    _map = (
        Map()
            .add('当前死亡人数', dead, "china")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新型冠状病毒全国疫情地图",
                                      subtitle="更新时间：{}".format(city_list[-1][0])),
            legend_opts=opts.LegendOpts(is_show=True),
            visualmap_opts=opts.VisualMapOpts(is_show=True, max_=50,
                                              is_piecewise=True,
                                              range_color=['#FFFFE0', '#FFA07A', '#CD5C5C', '#8B0000'])
        )
        # .render("全国确诊.html")
    )
    tab.add(_map, "累计死亡")

    tab.render(path="各省确诊人数.html")


def generate_city(city_list):
    input()
    china_province = {}
    for _province in province:
        china_province.update({_province:{}})
    for x in city_list:
        if x[1] in province:
            china_province[x[1]].update({x[2]:[0, 0, 0]})
    for item in city_list:
        name = item[1]
        if name in province:
            day = china_province[name][item[2]]
            # if name == '北京' or name == '上海' or name == '天津' or name == '重庆':
            #     item[2] = item[2] + "区"
            # elif "自治" in name:
            #     continue
            # else:
            #     item[2] = item[2] + '市'
            china_province[name].update({item[2]: [day[0]+item[3], day[1]+item[4], day[2]+item[5]]})
    tab = Tab()
    for x in province:
        dict_province = china_province[x]
        confirm = [(k, v[0]) for k, v in dict_province.items()]
        if x =="湖北":
            _map = (
                Map()
                    .add('确诊人数', confirm, x)
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="新型冠状病毒 {} 疫情地图".format(x),
                                              subtitle="更新时间：{}".format(city_list[-1][0])),
                    legend_opts=opts.LegendOpts(is_show=True),
                    visualmap_opts=opts.VisualMapOpts(is_show=True, max_=5000,
                                                      is_piecewise=True,
                                                      pieces=[
                                                          # 数据范围
                                                          {"min": 5000, "label": ">=5000", "color": "#807070"},
                                                          {"max": 4999, "min": 2000, "label": "2000 - 4999 人",
                                                           "color": "#8B0000"},
                                                          {"max": 1999, "min": 1500, "label": "1500 - 1999 人",
                                                           "color": "#CB0000"},
                                                          {"max": 1499, "min": 500, "label": "500 - 1499 人",
                                                           "color": "#DD5C5C"},
                                                          {"max": 499, "min": 200, "label": "200 - 499 人", "color": "#FFA07A"},
                                                          {"max": 199, "min": 1, "label": "1 - 199 人", "color": "#FFFF00"},
                                                      ]
                                                      # range_color=['#FFFFE0', '#FFA07A', '#CD5C5C', '#8B0000'])
                                                      )
                )
                # .render("全国确诊.html")
            )
        else:
            _map = (
                Map()
                    .add('确诊人数', confirm, x)
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="新型冠状病毒 {} 疫情地图".format(x),
                                              subtitle="更新时间：{}".format(city_list[-1][0])),
                    legend_opts=opts.LegendOpts(is_show=False),
                    visualmap_opts=opts.VisualMapOpts(is_show=True, max_=int(max([x[1] for x in confirm])),
                                                      is_piecewise=True,
                                                      range_color=['#FFFFE0', '#FFA07A', '#CD5C5C', '#8B0000'])
                )
                # .render("全国确诊.html")
            )
        tab.add(_map, x)
    # page.add(tab)
    tab.render(path="新型冠状病毒全国疫情地图.html")


def quanguo_wuhan_compare(city_list):
    time = set()
    for item in city_list:
        time.add(item[0])
    TIME = {}
    for x in time:
        TIME.update({x: (0, 0)})
    for item in city_list:
        if item[1] in province:
            if item[1] != "湖北":
                TIME.update({item[0]: (TIME[item[0]][0]+item[3], TIME[item[0]][1])})
            else:
                TIME.update({item[0]: (TIME[item[0]][0], TIME[item[0]][1] + item[3])})

    time_others_wuhan = []
    for k, v in TIME.items():
        time_others_wuhan.append([k, v[0], v[1]])
    time_others_wuhan.sort()

    L1 = (
        Line()
        .add_xaxis(xaxis_data=[x[0] for x in time_others_wuhan])
        .add_yaxis(
            series_name="全国其他地区",
            y_axis=[x[1] for x in time_others_wuhan],
            symbol_size=8,
            is_hover_animation=False,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=1.5),
            is_smooth=True,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="湖北地区和全国其他地区确诊人数对比图", subtitle="截止至2020年5月21日", pos_left="center"
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True, link=[{"xAxisIndex": "all"}]
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    is_realtime=True,
                    start_value=30,
                    end_value=70,
                    xaxis_index=[0, 1],
                )
            ],
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=True),
            ),
            yaxis_opts=opts.AxisOpts(is_inverse=False, name="人数"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                feature={
                    "dataZoom": {"yAxisIndex": "none"},
                    "restore": {},
                    "saveAsImage": {},
                },
            ),
        )
    )

    L2 = (
        Line()
        .add_xaxis(xaxis_data=[x[0] for x in time_others_wuhan])
        .add_yaxis(
            series_name="湖北地区",
            y_axis=[x[2] for x in time_others_wuhan],
            xaxis_index=1,
            yaxis_index=1,
            symbol_size=8,
            is_hover_animation=False,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=1.5),
            is_smooth=True,
        )
        .set_global_opts(
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True, link=[{"xAxisIndex": "all"}]
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(
                grid_index=1,
                type_="category",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=True),
                position="top",
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_realtime=True,
                    type_="inside",
                    start_value=30,
                    end_value=70,
                    xaxis_index=[0, 1],
                )
            ],
            yaxis_opts=opts.AxisOpts(is_inverse=True, name="确诊人数"),
            legend_opts=opts.LegendOpts(pos_left="15%"),
        )
    )

    (
        Grid(init_opts=opts.InitOpts(width="1024px", height="768px"))
        .add(chart=L1, grid_opts=opts.GridOpts(pos_left=50, pos_right=50, height="35%"))
        .add(
            chart=L2, grid_opts=opts.GridOpts(pos_left=50, pos_right=50, pos_top="55%", height="35%"),
            )
        .render(path="compare.html")
    )

if __name__ == '__main__':
    # page = Page()
    city_list = input()
    china_total(city_list)
    generate_city(city_list)
    quanguo_wuhan_compare(city_list)
    # page.render("疫情可视化分析.html")
    # print(data)

