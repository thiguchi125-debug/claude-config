# v2 デザインセンス強化仕様（2026-07-07 承認済み）

> 背景: design-studio運用開始後も「硬い・暗い・AIっぽい／レイアウト素人／引き出し不足」が残存。
> 根因: 種4作品が全部Claude自作＝AIの癖を教科書に再生産する閉ループ。外部良作の流入経路ゼロ。
> 勝ちパターンは判明済み（中庄夏祭り2026＝参照物の忠実再現）。

## Part A: 参照駆動制作の標準化（design-studio SKILL.md改修）

- Step 1 を「テンプレ選択」→「参照＆方向性選択」に拡張:
  - 実装前に design-inspiration-researcher（軽案件はインラインWebSearch）で外部参考2〜3枚収集
  - 既存テンプレ＋スタイル棚と並べて草川に提示、選択された参照は案件フォルダに保存
- print-layout-architect への指示に「参照画像を自分でReadして構図・配色・余白比率を模写。ゼロからのHTML発明禁止」を必須追加
- ガードルール: 参照から踏襲してよいのは構図・配色・雰囲気まで。イラスト・写真・ロゴ素材そのもののコピーは禁止（著作権）
- 短縮経路は外部収集を省略し、スタイル棚から選ぶ

## Part B: スタイル棚（foundations/styles/ 新設・5種）

1. `style_bright_illustration.html` — 淡色水彩・明るいイラスト系（地域・子ども向け＝理想形 DESIGN_RULES.md §1（明るいイラストチラシ））
2. `style_dark_lime.html` — ダーク×ライム（既存ブランド・eスポーツ系）
3. `style_ink_saving_report.html` — インク節約レポート系（木下v22系統）
4. `style_photo_bold.html` — 写真大胆系（全面写真＋白帯タイポ・選挙/人物もの）
5. `style_washu_calm.html` — 和風・落ち着き系（自治会・年配層向け）

- 各レシピ1ファイル: @dsCard（group="Foundations"）＋配色パレット・フォント・装飾語彙・使いどころ・コピペ可能CSS・ミニプレビュー
- 1・4・5は design-inspiration-researcher の外部良作分析を反映してから抽出
- 完成後 DesignSync で claude.ai/design へ差分push

## Part C: イラスト素材庫（assets/illustrations/ 新設）

- nano-banana（Gemini 2.5 Flash Image）用生成プロンプトカード15〜20点（水彩花・季節4季・子ども/家族キャラ・飾り罫等・全て透過PNG指定）
- 運用: Claudeがプロンプト設計→草川がGeminiで生成→フォルダ投入→Claudeが台帳化（一覧プレビューHTML）
- フリー素材（いらすとや等）は政治利用禁止規約があるため使わない。自前生成が権利的に安全
- design-studio Step2（素材収集）にこの素材庫参照を追加

## 成果物チェックリスト

- [ ] SKILL.md改修（Step1拡張・Step2素材庫・ガードルール・短縮経路）
- [ ] foundations/styles/ 5本（@dsCard付き・自己完結）
- [ ] assets/illustrations/ プロンプトカード＋台帳雛形＋README
- [ ] design_system README 構造・更新履歴反映
- [ ] DesignSync push（styles 5カード）
- [ ] メモリ project_design_studio.md 更新
