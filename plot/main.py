# Python 3.8.1
import xlrd  # 1.2.0
import numpy as np  # 1.18.1
from matplotlib import pyplot as plt  # 3.2.1


# Excelファイルをインポート
book = xlrd.open_workbook("./excel/data.xls")
# Excelファイルを絶対パスから開く
# book = xlrd.open_workbook(r"C:\\Users\○○\...\○○.xls")

# Excelにシートが複数ある場合，0から始まるインデックスで何枚目か指定する
sheet = book.sheet_by_index(0)

# matplotlibのインタラクティブモードをONに
# 数値を動的に変更できる
plt.ion()

# 新しいfigureを作成
plt.figure()

# グラフの変数を定義
# 100はグラフに一度に表示される点の数で，大きければより広い時間的範囲を表示できる
t = np.zeros(100)

# 使用するセンサーの値が並ぶ列番号を指定
# 普通経過時間が列0に来るので，ここでは1以上の数値を指定するはず
# 基本的にはsensor_colsを編集するだけでプロットするデータを増やせる様になっている
sensor_cols = [1, 2, 3, 4]
sensor_num = len(sensor_cols)

# それぞれのセンサーについて一度に表示される数値のリストを格納したリストを作る
ys = []
for i in range(sensor_num):
    ys.append(np.zeros(100))

# データをプロットする
# あとで数値を変更するのでlineオブジェクトとしてリストに格納しておく
# (line,)をlineに変えると，代入されるのはlineオブジェクトではなくリストになるので注意
lines = []
for i in range(sensor_num):
    (line,) = plt.plot(t, ys[i])
    lines.append(line)

# x軸のラベルを設定
plt.xlabel("t [s]")

# y軸のラベルを設定
plt.ylabel("a [m/s^2]")

# 時間の初期値をt_intとする
# 1サンプルあたりかかる時間をt_diffとする
# データの途中から処理を始めたい場合は，範囲を適宜変更するかExcelファイルを編集してください
data1 = sheet.row_values(1)
data2 = sheet.row_values(2)
t_int = float(data1[0])
t_diff = float(data2[0] - data1[0])

# 初期値を除くすべての行に関して処理を繰り返す
for rownum in range(2, sheet.nrows):
    try:
        # 新しい行を読み込み
        data = sheet.row_values(rownum)

        # グラフの表示範囲指定のため，センサデータの最大最小値を記録しておく
        ymaxs = []
        ymins = []

        # 配列をキューと見たてて要素を追加・削除
        # float(data[0])-t_int は初期時刻との差，つまり経過時間
        t = np.append(t, float(data[0]) - t_int)
        t = np.delete(t, 0)
        for i in range(sensor_num):
            ys[i] = np.append(ys[i], float(data[sensor_cols[i]]))
            ys[i] = np.delete(ys[i], 0)
            lines[i].set_xdata(t)
            lines[i].set_ydata(ys[i])
            ymaxs.append(max(ys[i]))
            ymins.append(min(ys[i]))

        # x軸の範囲を指定
        plt.xlim(min(t), max(t))
        # y軸の範囲を指定
        plt.ylim(min(ymins) - 0.1 * abs(min(ymins)), max(ymaxs) + 0.1 * abs(max(ymaxs)))

        # figureを再描画
        plt.draw()

        # アニメーションが一瞬で終わらないように一時停止
        plt.pause(t_diff)
    except KeyboardInterrupt as e:
        print(e)
        break
