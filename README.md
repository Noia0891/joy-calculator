# JOY CALCULATOR

Python と Tkinter で作った、シンプルなデスクトップ電卓です。四則演算や括弧を使った式を計算でき、計算履歴を保存・再利用できます。

## 特徴

- 足し算・引き算・掛け算・割り算
- 剰余（`%`）とべき乗（`^`）
- 括弧を含む計算式と小数、負の数に対応
- 計算履歴の表示、式の再利用、個別削除、全件削除
- 履歴を `history.txt` に保存
- キーボードからの式入力に対応

## 動作環境

- Python 3
- Tkinter（通常の Python インストールに含まれています）

外部 Python パッケージは不要です。

## 起動方法

リポジトリをクローンし、プロジェクトのフォルダーで起動します。

```bash
git clone https://github.com/Noia0891/joy-calculator.git
cd joy-calculator
python calculator_gui.py
```

Windows で `python` コマンドが使えない場合は、次をお試しください。

```powershell
py calculator_gui.py
```

## 使い方

- 画面上のボタン、またはキーボードで数字・演算子・括弧を入力します。
- `=` ボタンまたは Enter キーで計算します。
- Backspace キーで末尾を削除し、Escape キーで入力をクリアします。
- 「履歴」ボタンから計算式を再利用したり、履歴を削除したりできます。
- `history.txt` はアプリを起動した作業フォルダーに読み書きされます。

演算子は `+`、`-`、`*`、`/`、`%`、`^` を使用します。たとえば `2 * (3 + 4)` や `2^3` のように入力できます。

## ファイル構成

- `calculator_gui.py` — Tkinter の画面とユーザー操作
- `calculator_engine.py` — 式の解析・計算と履歴の読み書き
- `history.txt` — 計算履歴（実行時に更新されます）
