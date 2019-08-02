# bndbox
## 起動方法
### 必要なライブラリ<br>
- numpy
- cv2
- xml.etree.ElementTree
    - 僕のmacには最初から入ってました(多分標準ライブラリ)<br><br>
```
python3 coo_cap.py
```
<br><br>

## 画像
一度起動すると、```~/coo_cap/data```が作成されているので、そこに画像を入れます。<br><br><br>

## 使い方
1. 表示された画像の座標を取得したいオブジェクトの左上、右下をクリックし、四角で囲みます。<br><br>
2. キーボードのAを押すと、ターミナルでオブジェクト名を聞かれるので、各種キーによって選択。<br><br>
3. 画像内に、座標を取得したいオブジェクトが複数ある場合、1、2を繰り返す。<br><br>
4. 全てのオブジェクトの座標を取得し終えたら、キーボードのXキーを押す。<br><br>
5. ```~/coo_cap/xml```に、xml形式で出力されます。<br><br><br>

## キーバインド <br>
キー|処理|
---|---|
A|座標の確定、オブジェクト名の入力|
X|xml出力、次の画像へ|
C|座標選択やり直し|
N|何もせず次の画像へ|
B|何もせず前の画像へ|
Q|プログラムの終了|
