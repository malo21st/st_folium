import streamlit as st
from streamlit_folium import folium_static
import folium
from folium import plugins
from folium.features import CustomIcon
import gpxpy
import pandas as pd

# コンビニの位置データ
df_shops = pd.read_json('shop.json')
shop_lst = []
for _, pos in df_shops.iterrows():
    shop_lst.append((pos['lat'], pos['lon']))

# ウォーキングのトレースデータ
gpx_file = open('track-2690684.gpx')
gpx = gpxpy.parse(gpx_file)
walk_lst = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            walk_lst.append([point.latitude, point.longitude])
gpx_file.close()
df_gpx = pd.DataFrame(walk_lst, columns=['lat', 'lon'])

# 地図の中心の緯度と経度
center_lat = (df_gpx['lat'].min() + df_gpx['lat'].max())/2
center_lon = (df_gpx['lon'].min() + df_gpx['lon'].max())/2

# サイドメニュー
page = st.sidebar.radio(
    '次のメニューからお選び下さい：',
    ['Marker', 'Poly Line', 'MarkerCluster', 'Tooltip', '全部がっちゃんこ', 'CircleMarker', 'CustomIcon'],
    index = 0
    )

tile = st.sidebar.selectbox(
        "お好みの地図を選んでね：",
        ('OpenStreetMap', 'cartodbdark_matter', 'cartodbpositron', 'stamenterrain', 'stamentoner', 'stamenwatercolor')
    )

# タイトル
st.title("Folium map in Streamlit お試し中")
# 地図作成
m = folium.Map(location=[center_lat, center_lon], tiles=tile, zoom_start=12)

if page == 'Marker':
    for (lat, lon) in shop_lst:
        folium.Marker((lat, lon)).add_to(m)
    msg = "地図上にマーカーを置けます"
        
elif page == 'Poly Line':
    folium.PolyLine(
        locations = walk_lst
    ).add_to(m)
    folium.TopoJson(
        data=open('41201.topojson'),
        object_path='objects.41201',
        name="topojson"
    ).add_to(m)
    msg = "線も引けちゃうよ"

elif page == 'MarkerCluster':
    plugins.MarkerCluster(shop_lst).add_to(m)
    msg = "倍率を変えると面白いよ"

if page == 'Tooltip':
    for _, shop in df_shops.iterrows():
        note = "<b>{}</b><br>{}".format(shop['名称'], shop['住所'])
        folium.Marker((shop['lat'], shop['lon']), tooltip = note).add_to(m)
    msg = "マーカーの上にマウスを持ってきてね"

if page == '全部がっちゃんこ':
    marker_cluster = plugins.MarkerCluster().add_to(m)
    for _, shop in df_shops.iterrows():
        note = "<b>{}</b><br>{}".format(shop['名称'], shop['住所'])
        folium.Marker((shop['lat'], shop['lon']), tooltip = note).add_to(marker_cluster)
    folium.PolyLine(
        locations = walk_lst,
        tooltip = "いつぞや歩いたルートです。"
    ).add_to(m)
    msg = "全部がっちゃんこできます"

if page == 'CircleMarker':
    for _, shop in df_shops.iterrows():
        note = "<b>{}</b><br>{}".format(shop['名称'], shop['住所'])
        folium.CircleMarker((shop['lat'], shop['lon']), 
                            radius= 5,
                            color = shop['color'],
                            opacity = 0.6,
                            fill_color = shop['color'],
                            fill_opacity = 0.4,
                            tooltip = note,
                           ).add_to(m)
    msg = "コンビニ別に色分けしました"

if page == 'CustomIcon':
    for _, shop in df_shops.iterrows():
        note = "<b>{}</b><br>{}".format(shop['名称'], shop['住所'])
        folium.Marker((shop['lat'], shop['lon']), 
                   icon = CustomIcon(shop['icon'], icon_size=(20, 20)),
                   tooltip = note,
                  ).add_to(m)
    msg = "アイコンもカスタマイズできますよ"
    
# 地図表示 Folium map in Streamlit
folium_static(m)
st.markdown("**{}**".format(msg))
