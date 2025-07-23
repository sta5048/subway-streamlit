import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os

def setup_korean_font():
    font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = "Noto Sans KR"
    else:
        print("❗ 폰트 파일이 존재하지 않습니다. fonts/NotoSansKR-Regular.ttf 확인 필요.")
