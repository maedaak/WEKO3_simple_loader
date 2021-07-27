# WEKO3 simple loader (簡略書式によるWEKO3へのアイテムimport)

## はじめに
[国立情報学研究所(NII)](https://www.nii.ac.jp/)では、機関リポジトリソフトウエア"WEKO"を開発・公開しています。
このWEKOは[オープンアクセスリポジトリ推進協会(JPCOAR)](https://jpcoar.repo.nii.ac.jp/)とNIIが共同運用する国内のリポジトリ環境提供サービス"JAIRO Cloud"で採用されていることから、国内の多くの大学・研究機関において利用があります。
このWEKOですが、WEKO2からWEKO3にメジャーバージョンアップをしたことにより、ツリー構造をもつメタデータスキーマに対応できるようになりました。
これにより、学術情報流通用にあらたに策定された[JPCOARスキーマ](https://schema.irdb.nii.ac.jp/ja)に対応を行っています。

しかし、ツリー構造をもつメタデータスキーマをExcelといったスプレッドシートやTSVで記述し、それを一括登録にかけることは難しいところがあります。
WEKO3のアイテムimport機能では、表形式データ(TSV)のカラム名に値を直接指し示すJSON形式のパスを使うことにより、この難題をクリアしています。これであれば、JSONを記述しているのと等価ですので、複雑なツリー構造のメタデータ中の項目を特定し、値を登録できます。ただし、メタデータ記述の表現力が高い反面、容易に記述することが難しいところがあります。

そこで、JPCOARスキーマの記述の表現力をある程度犠牲にするかわりに、旧バージョンのWEKO2のような簡易な登録フォーマットにより、アイテムの一括登録を行える仕組みを用意しました。もし、このツールではうまく登録できない値についても、最終的に出力されるTSVを直に編集することとで、対応はできます。このツールは、WEKO3のいち利用者として開発を行ったもになります。ぜひWEKO3のユーザコミュニティ内にて活用や発展をしていければ幸いです。また、WEKO3に限らず、表形式のメタデータをJSONパスにマップするためのツールとしても使えるかもしれません。

## 簡略書式の実現方法
WEKO3の機能ではなく、外付けの仕組みです。利用に際してはアイテムタイプに合わせたマッピング設定ファイルと、登録必要なメタデータ項目をすべて列挙したテンプレートの事前用意が必要です。
1. 簡易書式によりExcelなどスプレッドシートでメタデータを記述
2. 上記1のスプレッドシートのデータをutf8文字コードのTSVに変換
3. 上記2のTSVを、2つのPythonスクリプトを順にかけ、WEKO3標準のメタデータ登録形式に変換

4. 上記3のメタデータを（あれば本文ファイルと合わせて）dataフォルダに置き、zipファイルに圧縮
5. 上記4のzipファイルを、 WEKO3のimport機能で一括登録

## 簡易フォーマット
WEKO2の一括登録フォーマットとほぼ近い形です。

1. JPCOARスキーマの項目の値と属性をひとつのカラムにまとめられます。たとえば、次のような形です。属性は「固定値」で2つまで指定できます。プログラムの修正により利用できる属性の個数を増やすことが可能です。
    + 例：簡易フォーマット項目「抄録」 ⇒　スキーマ項目：「内容記述」、属性1:「"Abstruct"」

2. 「Allow Multiple」を指定したカラムにおいて値の繰り返しができます。
    + 同じカラム名の列を用意し、それに値を入れると繰り返しとして扱われます。
    + セル内で繰り返しを表現できます。繰り返し項目の区切り記号はWEKO2のデフォルトである"|"を使っていますが、プログラム中のパラメータ変更で任意の文字列に変更することも可能です。

3. 「桁合わせ」により項目同士の関連付けができます。<br>
次の例では「用語」に"ja"が、「Word」に"en"が関連付けられます。「???」は桁合わせにより「関連付けなし」になります。

	| キーワード | キーワード_言語 |
	| :-------------------------------: | :---------------: |
	| 用語\|???\|Word    |    ja\|\|en |

4. 直前の項目に関連し、すべて固定値をセットするには、repeat()関数を使います。<br>
次の例だと「用語」「名詞」「形容詞」「副詞」「動詞」が全て"ja"に関連付けられます 。

	| キーワード | キーワード_言語 |
	| :--------------------------------: | :---------------: |
	| 用語\|名詞\|形容詞\|副詞\|動詞    |    repeat("ja") |

## マッピング方法
### WEKO3のimportデータ形式の確認
WEKO3管理画面の「import」から「テンプレート出力」実行することで、アイテムタイプに沿った一括登録形式を確認できます。<br>
値が具体的にどのJSON形式のパスにセットされているか確認するために、登録済データをEXPORTして確認するとわかりやすいかと存じます。

WEKO3一括登録フォーマットの確認では、カラム名が多く行が長くなりがちです。このままPC画面を横スクロールし、どのようなカラムが含まれるか確認するのは面倒です。データの縦横をいれかえたほうが、見通しがよくなります。Excelであれば、データをシートに張り付けるときに、カラムとレコードの縦横変換可能です。
+ Windowsのメモ帳などでTSVファイルを開き、テキスト全体をコピーします。
+ 上記のデータをExcelのシートに張り付けます。
+ Excelでデータが入っている行をコピーします。
+ Excelで別シートを作り、コピーした行を張り付けます。
+ 貼り付けの際に、貼り付けオプションを指定するアイコンが表示されます。そこで縦横の変換を選んでください。


### マッピング設定
+ 任意の名称のutf8のTSVファイルに記載します。Excel等のスプレッドシートで記述し、それを変換して使うのが容易かと思います。
+ TSVのカラムは以下のとおりです。

	| カラム名 | 説明文 |
	| ---------- | -------------------------------------------------- |
	| name | 簡易一括登録フォーマットのカラム名を記載します。 |
	| config | 「Allow Multiple」を設定すると繰り返し項目として扱われます。 |
	| path1 | WEKO3のJSON形式パスを指定します。末尾の値の指定は削除ください。繰り返し項目の場合は繰り返しの起点までです。その際は繰り返しの添え字記述（例"[0]")を削除ください。 |
	| path2 | path1の繰り返しの起点のあとにさらにJSON形式パス（値の記述を除く）があれば、記載します。 |
	| value | JSON形式パス中の値を示す部分パスを記載します。path1、path2で完結する場合は、# を記入ください。 |
	| attrib1 | JSON形式パス中の属性1を示す部分パスを記載します。形式は「属性名="属性の固定値"」とします。 |
	| attrib2 | JSON形式パス中の属性2を示す部分パスを記載します。形式は「属性名="属性の固定値"」とします。 |

+ valueとattib1、attrib2でパスの階層の深さが違う場合があります。path1もしくはpath2からの起点をそろえて設定ください。たとえば、以下の「刊行年月日」の例では、valueとattrib1の記述を「subitem_relation_type_id」から行うことで対応をとっています。

	| マッピング項目 | 設定
	| -------------- | --------------------------------------------------- |
	| value | subitem_relation_type_id.subitem_relation_type_id_tex |
	| attrib1 | subitem_relation_type_id.subitem_relation_type_select="ISBN" |
	| attirb2 | subitem_relation_type="isIdenticalTo"

+ 「.POS_INDEX」などJSON形式パスが繰り返しで終わるとき（valueに値をセットしないとき）は、valueに # を記載します。
+ path1「.」からパスを記載ください。path1に値があるときは、path2、value、attrib1、attrib2の先頭にパス区切りの「.」は不要です。
+ 項目とその関連する項目を「桁合わせ」によりセットするときは、path1とpath2の組み合わせが異なってる必要があります。valueに値を入れる、path1とpath2までとしvalueに#をセットするといったテクニックをうまく活用ください。

### （参考情報）マッチングの理解のために
具体的にはサンプルの設定をみていただくのが理解しやすいと思います。以下、マッピングがどう動作するかその考え方について説明します。
+ 最低限フルのJSON形式パスを value にセットすればマッピングが行われます。ただし、これでは設定が大変です。
+ valueに対応する属性情報（たとえば、「タイトル」に対応した「言語」など）を設定するために、attrib1(属性1)とattrib2(属性2）を使っています。valueとattirib1,attrib2はパスの階層(起点）を合わせる必要があります。これはpath1とpath2で指定します。
+ path1とpath2は繰り返しの項目を処理する場合に使っています。path1とpath2の間に繰り返しの番号（配列の添え字）がセットされます。
+ path1とpath2の組み合わせ回数で繰り返しの番号を決めています。そのため、path1とvalueに設定をした場合(path2を空値にした場合）と、path1とpath2のみに設定をした場合（valueを#にした場合）とでは動作が異なります。


### テンプレート設定
WEKO3のアイテムimport機能では、メタデータの記述に指定の形式のTSVを使う必要があります。WEKO3 Simple Loaderでは、最終的ににこのテンプレートをもとに値をセットします。ただし、WEKO3管理画面で取得できるテンプレートは、項目の繰り返しに対応がでっきていないので、あらかじめ必要な個数の繰り返しを用意したテンプレートに作り直します。
+ 任意の名称のutf8のTSVファイルに記載します。Excel等のスプレッドシートで記述し、それを変換して使うのが容易かと思います。
+ WEKO3の管理者画面にあるテンプレートを元に、必要な繰り返し項目について、あらかじめ入力列を用意したテンプレートを用意してください。
+ Pythonプログラム実行時にテンプレートとマッチしていない項目の情報は画面に警告が出ます。


## プログラムの実行
### 実行環境
<strong>Pyhon3の実行環境が必要です。</strong>

### コマンド書式
以下のコマンドで実行します。出力ファイル名は固定で<strong>jsonheader_metadata.txt</strong>になります。

`python weko3_simple_loder.py -i input.tsv -m mapping.txt`

jsonheader_metadata.txtは、処理のための中間ファイルであり、値のセット先のJSON形式パスと値の表になっています。しかし、WEKO3では空値の場合でもJSON形式パスを省略することはできません。そこであらかじめ、必要なデータ項目をすべて記載したテンプレートにデータを流し込みます。

重要なポイントとして、マッピングの設定ミスをここで確認できることがあります。もしマッピングに存在しない入力データのカラム名が存在していた場合、該当のカラム名に続けて<i>"is ignored"</i>のワーニングメッセージが処理画面に出力されます。


`python WEKO3_templateset.py -t template.txt -o output.tsv`

最終的に出力される<i>output.tsv</i>sがWEKO3の一括登録メタデータ形式になっています。このツールではうまく登録できない値については、必要に応じ手を入れてください。たとえば、出力されたTSVファイルをExcelなどのスプレッドシートに取り込み、必要な編集を行った後、TSVとして保存するといったやりかたがあります。

重要なポイントとして、マッピングの設定ミスをここで確認できることがあります。もしテンプレートに存在しないJSON形式パスが入力データ中に存在していた場合、該当のJSON形式パス名に続けて<i>"is invalid"</i>のワーニングメッセージが処理画面に出力されます。

## 出力結果を得た後は
本文ファイル(PDFなど）とパックにしたWEKO3のimport形式のデータ(zip形式ファイル)にしてからお使いください。
+ dataフォルダに出力ファイルを置きます
+ メタデータ中で指定したディレクトリ・ファイル名で、アイテムと合わせ登録する本文ファイルを置きます
+ zip形式でファイルをまとめれば、WEKO3のimport形式フィルができあがります。

## サンプルについて
sampleフォルダには、Thesis (学位論文)とBulletin Paper(紀要論文)それぞれについて、マッピング、テンプレート、テストデータをサンプルとしておいています。各WEKO3環境によってアイテムタイプの設定は異なるため、そのままではお使いいただけませんが、設定の際の参考にしてください。またJSON形式パス中の数値を書き換えることで流用できるところもあるはずです。ただし、アイテムタイプ、たとえば図書などでは「subitem_relation_type="isIdenticalTo"」ではなく「relationType="isPartOf"」を使っているなどのケースも考えられ、細かいチェックが必要となりますので、ご注意願います。<br>
sampleフォルダにはsample_Thesis.bat、sample_BulletionPaper.batの2つのサンプルプログラムを置きました。Windows環境であれば、コマンドプロンプトからこれを実行することで、サンプルデータでWEKO3 Simple Loaderがどのように動作するか試すことができます。

## Developer
[Maeda Akira](https://researchmap.jp/genroku)<br>
orcid: https://orcid.org/0000-0002-4566-8085
