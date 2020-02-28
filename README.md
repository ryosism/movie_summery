# movie summary

![Python](https://img.shields.io/badge/Python-3.6.5-blue.svg)
![Anaconda](https://img.shields.io/badge/Anaconda-5.2.0-green.svg)

***
特徴抽出器によって得た特徴ベクトルで類似度検索を行った結果を元に、ユーザに候補を提示するGUIシステム

## Requiements (recommended)
- MacOS Catalina(10.15.2)
- ffmpeg (シェルで起動できるようにしておくこと，homebrewでインストールすると楽)


その他のパッケージはAnacondaでインストールすることをお勧めする．
特にTkinter周りはバージョンの違いにより動作しない可能がある

## Usage
### 1, Create `candidate.json` & `query.json`
- 類似度検索や物体検出との照合によって`candidate.json`と`query.json`を用意する
    - `/home/tcn_tripletloss/src/tcn_tripletloss_value2.py`
        - kerasによる類似度検索(卒論・修論で使用したモデル)
    - `/home/tcn_tripletloss/pytorch/similarSearch.py`
        - pytorchによる類似検索(swapの調整も可能)
    - `/home/OSS/keras_frcnn_forEPIC-KITCHEN_predict/detector+tcnResult.ipynb`
        - 物体検出結果を利用し照合を行い，`candidate.json`の更新を行う

などで生成できる．
`candidate.json`と`query.json`には手順画像と候補動画フレームのファイルパスが含まれている．

### 2, modify `summary.py`
- `candidate.json`と`query.json`のパスをソースコード内に記載
    - 332行目と335行目に記入

### 3, Launch `summary.py`
- `python summary.py [要約対象の動画ファイルのパス]`
    - 第１引数に動画ファイルのパスを指定
- GUIが立ち上がるので，マウスで操作
    - 適切な動画フレームを選択し，Set as keyframeのボタンを押す
    - 字幕は右側のテキストボックスに入力し，Apply descriptionボタンを押すことで反映される
    - 一番下にタイトルを入力する

## Outputs
- `summarizedMovie_srt.mp4`
    - 要約済みの動画(字幕付き)
- `summarizedMovie.mp4`
    - 要約済みの動画(字幕なし)
- `clopMovie_[手順番号].mp4`
    - 選択した動画フレームを元に作成したクロップ(手順数分だけ出力される)
- `zimaku.srt`
    - 字幕情報，このファイルと`summarizedMovie.mp4`を元に字幕を付与している

これらのファイルは次回起動時に削除される．\
また，一部の環境ではボタンの文字が表示されない．その場合一度ウィンドウサイズを変更させると解決する場合がある．
