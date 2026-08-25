# 草川たくや デザインシステム（ローカル正本）

> 草川たくや（亀山市議会議員）の印刷物・発信物デザインの**正本ディレクトリ**。
> 実績最高品質の4作品からテンプレ・部品・基盤を抽出し、claude.ai/design プロジェクトへ
> DesignSync で push してブラウザのカード一覧からテンプレを選べるようにするための資産。
> 正本は常に**ここ（ローカル）**。claude.ai/design 側は表示用ミラー。

## 構造

```
design_system/
  README.md                    ← このファイル
  v1_refinement_spec.md        ← 過去案件（亀山建設労組 市政報告）のdesign-directorレビュー記録。参照用に残置
  references/                  ← **参照ライブラリ（2026-08-12新設）＝造形の借り先。制作は必ずここから1本選ぶ**
    README.md                    運用ルール・造形カルテ5軸・模写採点表（合格ライン）・参照の質ゲート
    _INDEX.md                    全参照の索引（ジャンプ率／色数／写真占有率／イラスト量の一覧）
    trifold/                     三つ折り9点＋_karte.md（東大病院中面=中面の教科書／議員リーフレット見本=選挙物の正）
    a4_flyer/                    A4チラシ（リソ2〜3色ドッシエ。画像は要再取得）
    poster/ a4_report/           **空。次の該当案件で収集して埋める**
    brand_system/                Warren2020 キャンペーンブランド一式
    _format_only/                様式の確認だけに使う資料（造形は借りない）
  foundations/                 ← 基盤（色・文字・ルール）
    colors.html                  ブランド4色＋印刷インク節約パレット＋使い分け
    typography.html              種4作品から抽出したフォントスタック・サイズ階層
    rules.md                     デザイン制作の恒久ルール集（禁止意匠・CSS確定パターン・入稿手順）
    styles/                      スタイルレシピ7種（v2で新設。配色hex・フォント・装飾語彙・構図・NGの正本）
      _INDEX.md                       条件→様式の判断表。**参照を選ぶ前にここで様式を1枚決める**
      style_bright_illustration.html  淡色水彩・明るいイラスト系（子育て・地域＝理想形）
      style_dark_lime.html            ダーク×ライム（eスポーツ・若者向け。子ども向けにはデフォルト選択しない）
      style_gov_formal.html           官公庁フォーマル系（議会・行政資料／スライド等デジタル面の第一候補）
      style_ink_saving_report.html    インク節約レポート系（木下v22系統）
      style_newspaper_editorial.html  新聞体エディトリアル系（文字量が多い中面・裏面の第2の解）
      style_photo_bold.html           写真大胆系（全面写真＋白帯。選挙・人物もの）
      style_washu_calm.html           和風・落ち着き系（自治会・敬老。朱赤は藍/金茶で置換）
  assets/
    illustrations/               イラスト素材庫（v2で新設。自前nano-banana生成・政治利用セーフ）
      README.md                    運用フロー（生成→投入→台帳化）・multiply合成のコツ
      prompt_cards.md              生成プロンプトカード20枚（水彩花/季節/人物/フレーム/和風）
  components/                  ← 再利用部品（コピペ可能なCSS＋実演）
    lime_heading.html            ライムバー見出し（box-shadow inset下線。gradient hard-stop禁止の注記入り）
    qr_footer_block.html         QR＋連絡先フッター2パターン（討議資料表記含む）
    photo_text_row.html          text-beside-image 2カラム行（float禁止・同高flex）
    stat_numbers.html            数字強調ブロック（2×2数字セル／5連ZEROグリッド）
    icons_policy.html            **政策アイコン8種**（子育て/防災/医療/交通/まちづくり/DX/環境/対話。SVGコピペ可・24〜56px）
    diagram_parts.html           **図解パーツ4種**（メーター/ピクトグラム/関連図/年度タイムライン。色分けしない設計・根拠の検証結果同梱）
  templates/                   ← 完成テンプレ4種（各: template.html=正本verbatim / preview.html=カード用縮図 / README.md=運用手引）
    flyer_a4/                    イベントチラシ（eスポーツ flyer_a2 正本・ダーク×ライム）
    poster/                      イベントポスター（中庄夏祭り2026 正本・品質基準）
    report_a4_duplex/            市政報告レポートA4両面（木下v22 正本・インク節約）
    leaflet_trifold/             後援会リーフレットA4両面（選挙v3 正本・ブランド4色）
    report_kameoka/              市政報告レポートA4両面（**市政報告の正**・かめおか型v2 2026-07-08。design_spec.md同梱・箱ゼロ/明朝×ゴシック/非対称グリッド）
```

## 制作の順序（2026-08-12改訂・最重要）

**templates/ から入らない。references/ から入る。**

templates/ は「破綻しない版面」を保証するもので、**造形の強さは保証しない**。
テンプレだけを埋めると、ベタ帯と水平罫線を積んだだけの平凡な紙面になる（2026-08 三つ折りの失敗）。

正しい順序は次のとおり。

1. `references/_INDEX.md` で当たりをつけ、判型フォルダの `_karte.md` を読む
2. 参照を **1本** 選び、**画像を自分で Read する**（カルテを読んだだけで実装に入らない）
3. templates/ の該当テンプレを版面の土台として複製する
4. 参照の造形（級数ジャンプ率・色数・図形語彙・写真占有率・イラスト量）を寸法レベルで写す
5. 出力PNGを参照と並べ、`references/README.md` の**模写採点表**で採点。5軸中4軸「可」で合格

**「破綻ゼロ」は合格条件ではない。** それは natural-design-reviewer の担当範囲であって、
模写採点表を通らない限り紙面は完成していない。

## 使い方（3つのファイル種別）

| ファイル | 役割 | 使い方 |
|---|---|---|
| `template.html` | 種HTMLの**verbatimコピー**（正本） | 実制作時にこれを案件フォルダへ複製し、中身を差し替える。画像は元ディレクトリ相対参照のものあり（各README参照） |
| `preview.html` | claude.ai/design カード用の**自己完結縮図** | 外部画像参照なし・写真/QR/ロゴはプレースホルダー矩形・サンプル文言。レイアウト構造とブランド色を一目で確認する用。**実制作の複製元にしない**（template.htmlを使う） |
| `README.md`（各テンプレ） | 用途・紙サイズ・差し替えポイント・PDF生成コマンド・入稿注意 | 制作開始前に必読 |

## @dsCard カードマーカー規約

全preview系HTML（foundations/components/templates の表示用HTML）の**1行目**に必ず付ける：

```html
<!-- @dsCard group="Foundations" name="ブランドカラー" subtitle="印刷4色と使い分け" -->
```

- `group`: "Foundations" / "Components" / "Templates" の3種のみ
- `name` / `subtitle`: 内容に即した日本語（カード一覧の表示名になる）
- 新しい部品・テンプレを追加したら必ずマーカーを付けてから push する

## design-studio スキル等からの参照方法

制作系スキル・エージェント（print-designer / print-layout-architect / design-studio 等）はこの順で読む：

1. **`foundations/rules.md`** — 禁止意匠・CSS確定パターン・チェックリスト（毎回必読）
2. **`foundations/colors.html` / `typography.html`** — 案件の系統（政治広報系／レポート系／イベント系）に合うパレット・書体を選ぶ
3. **`templates/<該当>/README.md` → `template.html`** — 該当テンプレがあれば複製して差し替え制作。なければ `components/` の部品を組み合わせて新規制作
4. 出来が良い新作は components / templates に**還元**（部品化＋@dsCardマーカー＋README追記）してから claude.ai/design に再push

grep入口の例：
```bash
grep -rl "box-shadow: inset" ~/.claude/agents/knowledge/design_system/
grep -r "@dsCard" ~/.claude/agents/knowledge/design_system/ --include="*.html"
```

## DesignSync push 運用（claude.ai/design へのミラー）

- **正本はローカル**のこのディレクトリ。claude.ai/design 側を直接編集しない（編集したら必ずローカルへ逆反映してから次のpush）
- push対象＝@dsCardマーカー付きHTMLのみ（template.html・README.md・rules.md はローカル参照用。pushする場合もカードにはしない）
- push前チェック：
  1. `grep -r "@dsCard" --include="*.html" -L` 相当で**マーカー漏れがないか**（preview系HTML全数照合）
  2. preview.html が自己完結か（外部URL・ローカル画像パス参照が残っていないか：`grep -nE 'src="(assets|uploads|[a-z_]+\.png)' */preview.html`）
  3. 個人情報・人物写真が混入していないか（電話・メール実値はpreviewでは 000-0000-0000 / sample@example.com のダミーに統一済み）
- 更新履歴はこのREADME末尾に1行追記（日付＋変更点）

## 種ファイル（抽出元の原典・削除しない）

| テンプレ | 原典 |
|---|---|
| report_a4_duplex | `~/.claude/agents/knowledge/print_templates/district_report/v22_kinoshita_final.html` |
| poster | `~/.claude/projects/-Users-kusakawatakuya/drafts/2026-08_中庄夏祭りポスター/poster.html` |
| leaflet_trifold | `~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/2026-05_senkyo_leaflet_v3/index.html` |
| flyer_a4 | `~/.claude/projects/-Users-kusakawatakuya/drafts/2026-06_esports_smash/flyer_a2.html` |

## 更新履歴

- 2026-07-05 初版構築（foundations 3本／components 4本／templates 4種／種4作品から抽出）
- 2026-07-07 v2センス強化（v2_sense_upgrade_spec.md）: foundations/styles/ 5種新設（外部良作分析ベース・design-inspiration-researcher）＋assets/illustrations/ 素材庫新設＋design-studio Step1を参照駆動制作に改修
- 2026-07-07 templates/report_qa_cards/ 昇格（西宮型Q&Aカード）→ **同日草川却下・2026-07-08削除**
- 2026-07-08 **templates/report_kameoka/ 昇格（市政報告の正テンプレ）**: 草川本人指定ベンチマーク=広報かめおか翻訳。design_spec.md同梱（罫線囲みゼロ・ベタ帯ゼロ・明朝×ゴシック・非対称グリッド・円形ヌメラル1点・warm paper）。旧qa_cardsはclaude.ai/designからも削除（カード計16枚）
