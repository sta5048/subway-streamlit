import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os
import urllib.request

def setup_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR-Regular.ttf"
    font_path = "/tmp/NotoSansKR-Regular.ttf"
    
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)

    fm.fontManager.addfont(font_path)
    plt.rcParams["font.family"] = "Noto Sans KR"
