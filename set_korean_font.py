# set_korean_font.py
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request

def setup_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR-Regular.otf"
    font_path = "/tmp/NotoSansKR-Regular.otf"

    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)

    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())
