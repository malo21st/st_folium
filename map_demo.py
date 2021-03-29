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
    'Select map type',
    ['Marker', 'Poly Line', 'MarkerCluster'],
    index = 0
    )

# 地図作成
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
if page == 'Marker':
    folium.Marker(shop_lst).add_to(m)
        
elif page == 'Poly Line':
    folium.PolyLine(
        locations = walk_lst
    ).add_to(m)

elif page == 'MarkerCluster':
    plugins.MarkerCluster(shop_lst).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)
