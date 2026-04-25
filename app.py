import dash
from dash import html, dcc, Input, Output, State, ALL, MATCH, ctx, no_update
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# 初始化 App
app = dash.Dash(__name__,title="六朝风雨路，一桥一春秋", external_stylesheets=[dbc.themes.BOOTSTRAP])

# ==========================================
# 1. 核心数据与图表定义
# ==========================================

df_struct = pd.DataFrame({
    "朝代": ["先秦-南北朝", "隋代", "唐代", "宋代", "明代", "清代"],
    "木桥": [100, 0, 25, 10, 4, 4],
    "石拱桥": [0, 100, 62, 73, 82, 81],
    "梁式桥": [0, 0, 13, 17, 14, 15]
})

colors = {
    "木桥": "#5D7376",
    "石拱桥": "#8B5E3C",
    "梁式桥": "#7D9D7D"
}

bridge_data = [
    {
        "name": "赵州桥",
        "dynasty": "隋朝",
        "length": 64.4,
        "prompt": "天下第一敞肩石拱桥，比欧洲早1200年！"
    },
    {
        "name": "宝带桥",
        "dynasty": "唐朝",
        "length": 316.8,
        "prompt": "53孔连拱柔性墩，大运河漕运命脉！"
    },
    {
        "name": "广济桥",
        "dynasty": "宋朝",
        "length": 518,
        "prompt": "世界最早开合式桥梁，通航通行双兼容！"
    },
    {
        "name": "卢沟桥",
        "dynasty": "金朝",
        "length": 266.5,
        "prompt": "501只形态各异的石狮，燕京八景之一！"
    },
    {
        "name": "八里桥",
        "dynasty": "明朝",
        "length": 50,
        "prompt": "不落桅的漕运要冲，见证晚清悲壮历史！"
    },
    {
        "name": "五亭桥",
        "dynasty": "清朝",
        "length": 57.99,
        "prompt": "十五桥洞各衔一月，中国最美的亭桥！"
    }
]

# ==========================================
# 2. 详细史实数据库
# ==========================================
details_db = {
    "古桥概览": {
        "title": "### 🏛️ 中华营造：古桥里的科学与文明",
        "desc": (
            "**【建筑成就：世界桥梁史的丰碑】**<br>"
            "中国古桥以**“拱、梁、索”**三大体系独步天下。赵州桥首创“敞肩拱”比欧洲早千年，广济桥“十八梭船”开启世界启闭式桥梁先河。这些成就不仅展示了古代工匠对力学与水文的高超驾驭，更弘扬了中华优秀自然科学成就。<br><br>"

            "**【杰出科学家与工匠精神】**<br>"
            "每一座名桥背后都屹立着一位科学巨匠。如**隋代李春**（赵州桥设计者），他突破传统半圆拱限制，首创圆弧拱与敞肩结构，体现了**“勇于探索、精益求精”**的科学家精神；唐代王仲舒（宝带桥）捐带建桥，展现了**“造福桑梓、公而忘私”**的儒匠情怀。<br><br>"

            "**【建筑著作与专著传承】**<br>"
            "虽然桥梁专著多散佚，但**《营造法式》**（宋·李诫）与**《工程做法则例》**（清）中保留了大量桥梁营造的“法式”与“则例”。这些古籍记录了从选材、地基处理到结构拼接的严密逻辑，是弘扬中华优秀古建筑学专著与智慧的活化石。<br><br>"

            "**【文化传承：天人合一的哲学】**<br>"
            "古桥不仅是交通设施，更是**“天人合一”**哲学的载体。从“长虹卧波”的审美意境，到“修桥补路”的功德文化，古桥连接了山水，也连接了人心。保护古桥，即是守护中华优秀古建筑文明与文化传承的根脉。"
        ),
        "img": "/assets/bridge/总览-08.jpg"
    },
    "赵州桥": {
        "title": "### 隋朝·赵州桥",
        "desc": "**【核心数据】** 主拱净跨度37.02米，全长约64.4米。<br>"
                "**【硬核科技】** **敞肩拱与纵向并列砌筑**。李春创造性地在主拱两端各设计两个小拱，不仅节省石料、减轻桥重，更增加了泄洪面积。桥体由28道独立拱券纵向并列，并用“腰铁”和铁拉杆加固，如同现代的“预应力钢筋”。<br>"
                "**【历史价值】** 它是“国际土木工程历史古迹”，首创“圆弧拱”和“敞肩拱”，奠定了中国石拱桥的技术范式，比欧洲同类技术早了1200年。",
        "img": "/assets/bridge/赵州桥-06.png"
    },
    "宝带桥": {
        "title": "### 唐代·宝带桥",
        "desc": "**【核心数据】** 全长316.8米，53孔连拱。<br>"
                "**【硬核科技】** **柔性墩与连续拱券**。为适应大运河软土地基，采用了能通过微小变形吸收冲击的“柔性墩”。53个桥孔如连环扣，将荷载均匀传递，即便单孔受损也不会导致全桥坍塌。<br>"
                "**【历史价值】** 它是大运河漕运的咽喉，见证了古代江南经济的繁荣与漕运制度的兴衰，被誉为“运河第一桥”。",
        "img": "/assets/bridge/宝带桥-02.jpg"
    },
    "广济桥": {
        "title": "### 南宋·广济桥",
        "desc": "**【核心数据】** 全长518米，集梁桥、浮桥、拱桥于一体。<br>"
                "**【硬核科技】** **十八梭船廿四洲**。桥中间由18只木船连成浮桥，遇大船或洪水时可解开移走，是世界上最早的“启闭式桥梁”。这种设计巧妙解决了韩江江面宽、水流急的难题。<br>"
                "**【历史价值】** 作为海上丝绸之路的重要门户，它连接闽粤商道，是潮州商业文明的象征，被茅以升誉为中国桥梁史的集大成者。",
        "img": "/assets/bridge/广济桥-03.jpg"
    },
    "卢沟桥": {
        "title": "### 金代·卢沟桥",
        "desc": "**【核心数据】** 全长266.5米，11孔联拱。<br>"
                "**【硬核科技】** **斩龙剑与铁柱加固**。桥墩前装有三角形的“斩龙剑”铁柱，用于劈开冰块和洪流。船形桥墩和深入地下的铁柱加固，极大增强了桥梁的稳定性。<br>"
                "**【历史价值】** 它是“燕京八景”之一，桥上的501只石狮形态各异。1937年“七七事变”在此爆发，使其成为中华民族抗争与复兴的历史见证。",
        "img": "/assets/bridge/卢沟桥-04.jpg"
    },
    "八里桥": {
        "title": "### ️ 明朝·八里桥",
        "desc": "**【核心数据】** 全长50米，三孔联拱。<br>"
                "**【硬核科技】** **不落桅设计**。桥身中间桥孔最高，两侧渐低，桥面弧度平缓，专为适应漕运大船而设计，实现了“桥不落桅、船不停航”的高效通行模式。<br>"
                "**【历史价值】** 它是京畿地区的漕运要冲，也是著名的古战场。1860年的“八里桥之战”见证了晚清抗击外敌的悲壮历史，是大运河文化带上不可磨灭的印记。",
        "img": "/assets/bridge/八里桥-01.jpg"
    },
    "五亭桥": {
        "title": "### 清代·五亭桥",
        "desc": "**【核心数据】** 桥长57.99米，桥上五亭。<br>"
                "**【硬核科技】** **亭桥结合与声学共鸣**。桥身由三个巨大的拱券组成，桥上五座重檐亭子不仅稳固桥身，还形成了独特的天际线。15个桥洞在中秋之夜能形成“洞洞衔月”的奇观。<br>"
                "**【历史价值】** 它是清代扬州盐商文化的缩影，融合了北方皇家园林的雄浑与江南私家园林的秀丽，被誉为“中国最美的桥”。",
        "img": "/assets/bridge/五亭桥-05.jpg"
    }
}


# ==========================================
# 3. 图表函数
# ==========================================

def draw_parallel_wave_animation():
    dynasties = ["隋代", "唐代", "元代", "宋(含辽金)", "明代", "清代"]
    counts = [2, 8, 11, 52, 68, 96]

    custom_colors = [
        '#C4DEED',
        '#AED4E5',
        '#9CBFD4',
        '#92C8DC',
        '#7CB2D4',
        '#65A0C6'
    ]

    total_frames = 60
    fig = go.Figure()

    # 1. 定义竖排文字
    raw_title = "历代交通古桥数量演变"
    vertical_text = "<br>".join(list(raw_title))

    # 2. 定义 Annotation
    title_annotation = dict(
        x=0.05,
        y=0.92,
        xref='paper',
        yref='paper',
        text=vertical_text,
        showarrow=False,

        # --- 文字样式 ---
        font=dict(
            family="STKaiti, KaiTi, serif",
            size=16,
            color="#2C3E50"
        ),
        align="center",
        valign="top",

        bgcolor="rgba(250, 245, 230, 0.9)",
        bordercolor="#B22222",  # 朱红色
        borderwidth=1,
        borderpad=8,

        opacity=1.0,  # 整体不透明度 (Plotly 中用 opacity 控制，而不是在 style 里写 opacity)
    )

    fig.add_trace(go.Bar(
        x=dynasties, y=[0] * 6, name="数量",
        marker_color=custom_colors
    ))

    fig.add_trace(go.Scatter(
        x=dynasties, y=counts, name="趋势",
        mode='lines+markers',
        line=dict(color='#C05B4D', width=4, shape='spline'),
        opacity=0
    ))

    fig.update_layout(
        annotations=[title_annotation],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, color='#333333'),
        yaxis=dict(showgrid=False, zeroline=False, color='#333333', showticklabels=False),
        transition=dict(duration=0),
        margin=dict(l=0, r=0, t=80, b=0),
        height=400
    )

    frames_list = []
    for i in range(total_frames):
        progress = i / (total_frames - 1)
        current_heights = []
        for idx, target_h in enumerate(counts):
            delay = idx * (0.2 / (len(counts) - 1))
            local_progress = max(0, (progress - delay) / (1 - delay))
            current_heights.append(target_h * local_progress)

        if progress > 0.85:
            line_opacity = min(1.0, (progress - 0.85) / 0.15)
        else:
            line_opacity = 0

        frame = go.Frame(
            data=[go.Bar(y=current_heights), go.Scatter(opacity=line_opacity)],
            name=f"frame_{i}"
        )
        frames_list.append(frame)

    fig.frames = frames_list
    fig.update_layout(
        updatemenus=[{
            "type": "buttons", "showactive": False, "y": 1, "x": 0.8,
            "buttons": [{"label": "▶ 播放演变", "method": "animate",
                         "args": [[f"frame_{i}" for i in range(total_frames)],
                                  {"frame": {"duration": 30, "redraw": True}, "transition": {"duration": 0},
                                   "mode": "immediate"}]}]
        }]
    )
    return fig


def create_treemap():
    labels = ["中国古桥概览"] + [item["name"] for item in bridge_data]
    parents = [""] + ["中国古桥概览"] * len(bridge_data)
    length = [''] + [item["length"] for item in bridge_data]

    custom_colors = [
        'rgba(0,0,0,0)',
        '#dbfad9',
        '#ccf3d0',
        '#b6e8c2',
        '#9edeb3',
        '#89d3a7',
        '#79cc9c'
    ]

    customdata = [None] + [f"{item['dynasty']}<br>{item['prompt']}" for item in bridge_data]

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=length,
        tiling=dict(pad=0, packing="squarify"),
        marker=dict(
            colors=custom_colors,
            line=dict(color='#F8F8F8', width=2)
        ),
        textfont=dict(
            color=["rgba(0,0,0,0)", "black", "black", "black", "black", "black", "black"],
            size=14
        ),
        customdata=customdata,

        maxdepth=2,

        hovertemplate=[''] + [
            '<b>%{label}</b><br>长度：%{value}米<br>%{customdata}<br><span style="font-size: 10px; color: #888;">（注释）图中方块相对大小代表桥梁相对长度</span><extra></extra>'] * len(
            bridge_data),
        hoverinfo='text+value'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, l=0, r=0, b=0),
        autosize=True,
        font=dict(family="STKaiti", size=14),
    )
    return fig


def create_animation_figure():
    fig = go.Figure()
    for bridge_type in ["木桥", "石拱桥", "梁式桥"]:
        fig.add_trace(go.Scatter(
            x=df_struct['朝代'], y=df_struct[bridge_type],
            mode='lines+markers', name=bridge_type,
            line=dict(color=colors[bridge_type], width=3, shape='spline', smoothing=1.3),
            marker=dict(size=10, line=dict(width=2, color='white')),
            text=df_struct.apply(lambda row: f"朝代：{row['朝代']}<br>类型：{bridge_type}<br>占比：{row[bridge_type]}%",
                                 axis=1),
            hoverinfo='text'  # 只显示自定义的 text 内容
        ))

    fig.add_shape(
        type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1,
        fillcolor="rgba(250, 245, 230, 1)", line_width=0, layer="above"
    )

    num_steps = 100
    frames = []
    for i in range(num_steps + 1):
        progress = i / num_steps
        current_x = progress * 1
        frames.append(go.Frame(
            layout=go.Layout(
                shapes=[dict(type="rect", xref="paper", yref="paper", x0=current_x, y0=0, x1=1, y1=1,
                             fillcolor="rgba(250, 245, 230, 1)", line_width=0, layer="above")]
            )
        ))
    fig.frames = frames

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x",
        hoverlabel=dict(
            bgcolor="rgba(250, 245, 230, 0.9)",  # 悬停框米色
            font_size=14,
            font_family="STKaiti",  # 悬停框字体
            bordercolor="#8B5E3C"  # 边框深褐色
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=False, linewidth=0, linecolor='#8B5E3C', mirror=False,
                   tickfont=dict(family="STSong", size=12), range=[-0.5, 5.5]),
        yaxis=dict(showline=False, linewidth=0, linecolor='#8B5E3C', mirror=False, range=[-5, 110],
                   tickfont=dict(family="STSong", size=12)),
        height=500,

        updatemenus=[dict(
            type="buttons", buttons=[dict(label="画卷展开", method="animate", args=[None, {
                "frame": {"duration": 30, "redraw": True}, "transition": {"duration": 0}, "fromcurrent": True}])],
            x=0.85, y=1.05, xanchor="left", yanchor="bottom", pad={"r": 10}, showactive=False,
        )],

    )
    return fig


def create_ghost_chart(title, color, data_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5], y=data_y,
        mode='lines+markers',
        line=dict(color=color, width=4, shape='spline'),
        marker=dict(size=10, color=color),
        name=title, hoverinfo='y'
    ))
    yaxis_config = dict(showgrid=False, zeroline=False, visible=False, showticklabels=False, scaleanchor="x",
                        scaleratio=1)
    fig.update_layout(
        title=dict(text=title, font=dict(color='#fff', size=16, family="Arial"), x=0.5, y=0.9, xanchor='center'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False, showticklabels=False),
        yaxis=yaxis_config, showlegend=False, height=250, clickmode='event+select'
    )
    return fig


# ==========================================
# 4. 配置区域 (新增左上角概览配置)
# ==========================================
CONFIG = [
    {
        "id": "btn_1",
        "label": "隋朝·赵州桥",
        "pos": {"top": "7.5%", "left": "68%"},
        "color": "#8B4513",
        "content": [
            html.H3("隋朝·赵州桥", style={'margin': '0 0 10px 0', 'color': '#8B4513'}),
            html.P("核心标签：天下第一敞肩石拱桥", style={'fontSize': '16px', 'fontWeight': 'bold'}),
            html.P("震撼亮点：比欧洲同类敞肩拱桥技术早1200余年", style={'fontSize': '14px', 'color': '#d35400'}),
            html.P("简介：由隋代工匠李春主持设计，是世界现存最古老、保存最完整的敞肩石拱桥。",
                   style={'fontSize': '14px', 'lineHeight': '1.5'})
        ]
    },
    {
        "id": "btn_2",
        "label": "唐代·宝带桥",
        "pos": {"top": "21%", "left": "24%"},
        "color": "#8B0000",
        "content": [
            html.H3("唐代·宝带桥", style={'margin': '0 0 10px 0', 'color': '#8B0000'}),
            html.P("核心标签：中国现存最长古代连拱石桥·大运河漕运命脉",
                   style={'fontSize': '16px', 'fontWeight': 'bold'}),
            html.P("震撼亮点：53孔连拱柔性墩设计，抗震结构", style={'fontSize': '14px', 'color': '#d35400'}),
            html.P("简介：始建于唐代元和年间，由苏州刺史王仲舒捐宝带资助修建，横跨京杭大运河。",
                   style={'fontSize': '14px', 'lineHeight': '1.5'})
        ]
    },

    {
        "id": "btn_3",
        "label": "金代·卢沟桥",
        "pos": {"top": "36%", "left": "62.6%"},
        "color": "#A52A2A",
        "content": [
            html.H3("金代·卢沟桥", style={'margin': '0 0 10px 0', 'color': '#A52A2A'}),
            html.P("核心标签：燕京八景之一·华北官道咽喉", style={'fontSize': '16px', 'fontWeight': 'bold'}),
            html.P("震撼亮点：501只石狮形态各异，石作雕刻艺术巅峰", style={'fontSize': '14px', 'color': '#d35400'}),
            html.P("简介：始建于金代大定年间，横跨永定河，是“卢沟晓月”的所在地。",
                   style={'fontSize': '14px', 'lineHeight': '1.5'})
        ]
    },

    {
        "id": "btn_4",
        "label": "南宋·广济桥",
        "pos": {"top": "60%", "left": "24.2%"},
        "color": "#FF8C00",
        "content": [
            html.H3("南宋·广济桥", style={'margin': '0 0 10px 0', 'color': '#FF8C00'}),
            html.P("核心标签：世界最早开合式石拱桥·海上丝绸之路门户", style={'fontSize': '16px', 'fontWeight': 'bold'}),
            html.P("震撼亮点：首创“十八梭船廿四洲”开合式设计", style={'fontSize': '14px', 'color': '#d35400'}),
            html.P("简介：始建于南宋乾道年间，横跨韩江，是中国四大古桥之一。",
                   style={'fontSize': '14px', 'lineHeight': '1.5'})
        ]
    },
    {
        "id": "btn_5",
        "label": "明朝·八里桥",
        "pos": {"top": "68%", "left": "72.6%"},
        "color": "#B22222",
        "content": [
            html.H3("明朝·八里桥", style={'margin': '0 0 10px 0', 'color': '#B22222'}),
            html.P("核心标签：运河上的古战场·京畿漕运要冲", style={'fontSize': '16px', 'fontWeight': 'bold'}),
            html.P("震撼亮点：“八里桥不落桅”的民间传说", style={'fontSize': '14px', 'color': '#d35400'}),
            html.P("简介：始建于明代正统年间，横跨通惠河，是明清时期京城通往通州的官道咽喉。",
                   style={'fontSize': '14px', 'lineHeight': '1.5'})
        ]
    },
    {
        "id": "btn_6",
        "label": "清代·五亭桥",
        "pos": {"top": "83%", "left": "33.2%"},
        "color": "#32CD32",
        "content": [
            html.H3("清代·五亭桥", style={'margin': '0 0 10px 0', 'color': '#32CD32'}),
            html.P("核心标签：中国最美的桥·瘦西湖点睛之笔", style={'fontSize': '16px', 'fontWeight': 'bold'}),
            html.P("震撼亮点：十五个桥洞各衔一月，形成“月满中天”奇景", style={'fontSize': '14px', 'color': '#d35400'}),
            html.P("简介：建于清代乾隆年间，位于扬州瘦西湖上，是中国古代桥梁与园林艺术结合的巅峰之作。",
                   style={'fontSize': '14px', 'lineHeight': '1.5'})
        ]
    }
]

card_states = {item["id"]: False for item in CONFIG}

# ==========================================
# 5. 布局架构
# ==========================================
styles = {
    'bg_image': {
        'position': 'absolute',
        'top': 0,
        'left': 0,
        'width': '100vw',  # 强制宽度填满
        'height': '100vh',  # 强制高度填满
        'zIndex': 0,
        'pointerEvents': 'none',
        'backgroundColor': '#000'
    },
    'corner_box': {
        'position': 'absolute',
        'zIndex': 10,
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'boxSizing': 'border-box',
        'overflow': 'hidden'
    }
}


def generate_center_controls():
    controls = []
    for i, item in enumerate(CONFIG):
        btn_id = item['id']

        # --- 修复开始 ---
        position_wrapper = html.Div(
            children=[
                html.Div(
                    id={'type': 'info-card', 'index': btn_id},
                    className="scroll-card",
                    children=item["content"],
                    style={
                        'opacity': 0,
                        'pointerEvents': 'none',
                        'transition': 'opacity 0.3s ease-out',
                        'width': '300px',
                        'maxWidth': '25vw',
                    }
                )
            ],
            style={
                'position': 'fixed',  # 外层保持 fixed
                'top': item['pos']['top'],
                'left': item['pos']['left'],
                'transform': 'translate(-50%, -50%)',
                'zIndex': 1000,
                'pointerEvents': 'none',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center'
            }
        )
        controls.append(position_wrapper)

        btn = html.Div(
            id={'type': 'center-btn', 'index': btn_id},
            children=[item["label"]],
            className='map-btn',
            style={
                'top': item['pos']['top'], 'left': item['pos']['left'],
                'backgroundColor': 'rgba(255, 50, 50, 0.5)',
                'border': '2px solid #FFFFFF',
            }
        )
        controls.append(btn)
    return controls


app.layout = html.Div([
    html.Img(src="/assets/背景-07.jpg", style=styles['bg_image']),
    html.Div([
        html.Div(
            children=[dcc.Graph(id='treemap-chart', figure=create_treemap(), config={'displayModeBar': False},
                                style={'height': '100%', 'width': '100%'})],
            style={
                'position': 'absolute', 'bottom': '2%', 'left': '0%',
                'width': '22vw', 'height': '30vh', 'zIndex': 80,
                'borderRadius': '8px', 'overflow': 'hidden', 'backgroundColor': ''
            }
        ),
        html.Div(
            id='treemap-detail-pane', children=[],
            style={
                'position': 'absolute', 'bottom': '38%', 'left': '0.5%',
                'width': '21vw', 'height': '18vh', 'zIndex': 85,
                'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '8px',
                'boxSizing': 'border-box', 'display': 'flex'
            }
        ),
        html.Div(
            id='bridge-container',
            children=[
                dcc.Graph(id='bridge-animation', figure=create_animation_figure(), config={'displayModeBar': False},
                          style={'height': '100%', 'width': '100%'})],
            style={
                'position': 'absolute', 'top': '2.7%', 'right': '0%',
                'width': '30%', 'height': '50%', 'backgroundColor': 'transparent',
                'zIndex': 50, 'border': 'none'
            }
        ),
        html.Div(
            children=[dcc.Graph(id='parallel-wave-chart', figure=draw_parallel_wave_animation(),
                                config={'displayModeBar': False}, style={'width': '100%', 'height': '100%'})],
            style={
                'position': 'absolute', 'bottom': '0%', 'right': '0%',
                'width': '24vw', 'height': '55vh', 'zIndex': 90,
                'border': 'none', 'backgroundColor': 'transparent', 'pointerEvents': 'auto'
            }
        ),
        html.Div(
            children=generate_center_controls(),
            style={
                'position': 'absolute', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'width': '100%', 'height': '100%', 'zIndex': 20
            }
        ),
        dcc.Markdown("""<style>[id*="center-btn"], [id*="info-card"] { pointerEvents: auto !important; }</style>""",
                     dangerously_allow_html=True, style={'display': 'none'}),
    ], style={'position': 'relative', 'width': '100%', 'height': '100%', 'zIndex': 1}),
], style={
    'margin': 0, 'padding': 0, 'width': '100vw', 'height': '100vh',
    'overflow': 'hidden', 'display': 'flex', 'justifyContent': 'center',
    'alignItems': 'center', 'backgroundColor': '#000'
})


# ==========================================
# 6. 交互逻辑 (兼容概览)
# ==========================================
@app.callback(
    [Output({'type': 'info-card', 'index': MATCH}, 'className'),
     Output({'type': 'info-card', 'index': MATCH}, 'style'),
     Output({'type': 'center-btn', 'index': MATCH}, 'style')],
    [Input({'type': 'center-btn', 'index': ALL}, 'n_clicks'),
     Input({'type': 'info-card', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def toggle_cards(n_clicks_btns, n_clicks_cards):
    triggered_id = ctx.triggered_id
    if not triggered_id or not isinstance(triggered_id, dict):
        raise PreventUpdate

    target_idx = triggered_id['index']
    trigger_type = triggered_id['type']
    config_item = next((item for item in CONFIG if item["id"] == target_idx), None)
    if not config_item:
        raise PreventUpdate

    color = config_item['color']
    global card_states

    # ----状态更新逻辑
    if trigger_type == 'center-btn':
        card_states[target_idx] = True
    elif trigger_type == 'info-card':
        card_states[target_idx] = False
    else:
        raise PreventUpdate

    new_state = card_states[target_idx]

    # ----卡片弹窗
    if new_state:
        # ----状态显示
        card_class = "scroll-card active"
        card_style = {
            'opacity': 1,
            'pointerEvents': 'auto',
            'boxShadow': f'0 10px 30px rgba(0,0,0,0.4), 0 0 15px {color}60',
            'zIndex': 9999,  # 强制最高层级
            'position': 'fixed',
            'width': '320px',
            'maxWidth': '28vw',
            'top': config_item['pos']['top'],
            'left': config_item['pos']['left'],
            'transform': 'translate(-50%, -50%)',  # 卡片显示在按钮上方
        }
    else:
        # ----状态隐藏
        card_class = "scroll-card"
        card_style = {
            'opacity': 0,
            'pointerEvents': 'none',
            'boxShadow': 'none',
            'zIndex': 9999,
            'position': 'fixed',
            'width': '320px',
            'maxWidth': '28vw',
            'top': config_item['pos']['top'],
            'left': config_item['pos']['left'],
            'transform': 'translate(-50%, -50%)',
        }

    btn_style = {
        'position': 'absolute',
        'top': config_item['pos']['top'],
        'left': config_item['pos']['left'],
        'transform': 'translate(-50%, -50%)',
        'backgroundColor': 'transparent',
        'border': '2px solid #b22222',
        'color': '#b22222',

        'padding': "clamp(8px, 1vh, 20px) clamp(15px, 2vw, 40px)",
        'borderRadius': '8px',
        'cursor': 'pointer',
        'fontSize': "clamp(12px, 1.5vw, 24px)",
        'zIndex': 40,
        'pointerEvents': 'auto',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'boxShadow': '0 4px 6px rgba(178, 34, 34, 0.1)'
    }

    return card_class, card_style, no_update


@app.callback(
    [Output('treemap-detail-pane', 'children'),
     Output('treemap-detail-pane', 'style')],
    [Input('treemap-chart', 'clickData')]
)
def update_bridge_detail(clickData={'points': [{'label': '中国古桥概览'}]}):
    # 显示样式
    show_style = {
        'position': 'absolute', 'bottom': '38%', 'left': '0.5%',
        'width': '21vw', 'height': '44vh', 'maxHeight': '600px',
        'zIndex': 85, 'backgroundColor': 'rgba(255, 255, 255, 0.98)',
        'borderRadius': '12px', 'padding': '15px', 'boxSizing': 'border-box',
        'display': 'flex', 'flexDirection': 'column', 'boxShadow': '0 4px 20px rgba(0,0,0,0.15)', 'overflow': 'hidden'
    }

    if not clickData:
        bridge_name = "中国古桥概览"
    else:
        bridge_name = clickData['points'][0].get('label', "中国古桥概览")

    data = details_db.get(bridge_name, details_db['古桥概览'])

    # 渲染内容
    content = [
        html.Div(data['title'].replace("### ", ""),
                 style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#333', 'marginBottom': '10px'}),
        html.Div(html.Img(src=data['img'], style={'width': '100%', 'height': '220px', 'objectFit': 'cover',
                                                  'borderRadius': '8px'}),
                 style={'height': '220px', 'marginBottom': '10px', 'overflow': 'hidden', 'flexShrink': 0}),
        html.Div(dcc.Markdown(data['desc'], dangerously_allow_html=True),
                 style={'fontSize': '14px', 'color': '#555', 'lineHeight': '1.6', 'flex': 1,
                        'overflowY': 'auto', 'paddingRight': '5px'})
    ]

    return content, show_style


if __name__ == '__main__':
    app.run(debug=False)