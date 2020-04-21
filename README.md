# ics_rws_python_2020

このコードは phyphox にて事前に記録した加速度の時系列データを再生しながら，加速度の絶対値が$6m/s^2$を超えたときにWebhookへリクエストを送信します．phyphox は xlsファイル，csvファイルを出力できます．それぞれのファイル向けにソースコードを用意しています．また，IFTTTと連携することを前提にしています．

これにより，例えばIFTTTを利用すれば条件を満たしたときにLINEへ通知するようなアプリケーションを実現できます．これを実現するために作るべきアプレットは「Webhook → LINE」のような連携である必要があります．

自分の環境で実行するためには，ソースコードの Event ID, Webhook Key を設定してください．

```python
# 以下の文字列を自分のものにおきかえてください
***EVENT ID***
***YOUR WEBHOOK KEY***
```