import streamlit as st
from streamlit_folium import folium_static
import folium
from folium import plugins
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
    'Select menu：',
    ['Marker', 'Poly Line', 'MarkerCluster', 'Tooltip'],
    index = 0
    )

# タイトル
st.title("Folium map in Streamlit")
# 地図作成
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
placeholder = st.empty()
if page == 'Marker':
    for (lat, lon) in shop_lst:
        folium.Marker((lat, lon)).add_to(m)
        
elif page == 'Poly Line':
    folium.PolyLine(
        locations = walk_lst
    ).add_to(m)

elif page == 'MarkerCluster':
    plugins.MarkerCluster(shop_lst).add_to(m)

if page == 'Tooltip':
    for _, shop in df_shops.iterrows():
        note = "<b>{}</b><br>{}".format(shop['名称'], shop['住所'])
        folium.Marker((shop['lat'], shop['lon']), tooltip = note).add_to(m)
    placeholder.text("マーカーの上にマウスを持ってきてね")
    
# 地図表示 Folium map in Streamlit
folium_static(m)

