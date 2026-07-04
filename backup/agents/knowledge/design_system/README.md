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
  foundations/                 ← 基盤（色・文字・ルール）
    colors.html                  ブランド4色＋印刷インク節約パレット＋使い分け
    typography.html              種4作品から抽出したフォントスタック・サイズ階層
    rules.md                     デザイン制作の恒久ルール集（禁止意匠・CSS確定パターン・入稿手順）
  components/                  ← 再利用部品（コピペ可能なCSS＋実演）
    lime_heading.html            ライムバー見出し（box-shadow inset下線。gradient hard-stop禁止の注記入り）
    qr_footer_block.html         QR＋連絡先フッター2パターン（討議資料表記含む）
    photo_text_row.html          text-beside-image 2カラム行（float禁止・同高flex）
    stat_numbers.html            数字強調ブロック（2×2数字セル／5連ZEROグリッド）
  templates/                   ← 完成テンプレ4種（各: template.html=正本verbatim / preview.html=カード用縮図 / README.md=運用手引）
    flyer_a4/                    イベントチラシ（eスポーツ flyer_a2 正本・ダーク×ライム）
    poster/                      イベントポスター（中庄夏祭り2026 正本・品質基準）
    report_a4_duplex/            市政報告レポートA4両面（木下v22 正本・インク節約）
    leaflet_trifold/             後援会リーフレットA4両面（選挙v3 正本・ブランド4色）
```

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
