# ElevenLabs 声クローン設定ガイド（草川さんの手番・所要20〜30分）

> これが完了すると、AIくさかわが**本人の声**で話せるようになります。
> 完了までは `--dev`（合成音声）のプレビューのみ・投稿不可。

## 1. 録音素材を決める（3〜5分ぶん）

条件: **草川さんひとりが話している・クリアな音・BGMや雑踏なし**。会議録音のように他の人の声が混ざるものは不可（声が混ざって学習される）。

### 既存録音の監査結果（2026-07-09）
`~/Archive` の音声を確認したところ、独り語りかどうか不明の録音が5本ありました。
30秒サンプルを切り出してあります → `~/outputs/ai-kusakawa/_voice_candidates/`

| サンプル | 元ファイル |
|---|---|
| 候補1（2.8時間） | Archive/録音/新規録音 50.m4a |
| 候補2（1.9時間） | Archive/録音/新規録音 74.m4a |
| 候補3（29分） | Archive/録音/安知本町2008.m4a |
| 候補4 | Archive/資料倉庫_2026以前/政治活動/新規録音 56.m4a |
| 候補5 | Archive/資料倉庫_2026以前/政治活動/新規録音 58.m4a |

聴いてみて「自分ひとり・クリア」なものがあればClaudeに「候補◯を声素材にして」と伝えてください（該当区間の切り出し・整音はClaude側でやります）。※委員会・議会系録音（R5.9.13教育民生委員会等）は複数話者のため候補から除外済み。

### 使えるものがなければ新規録音（こちらが確実・5分で終わる）
- 静かな室内で、iPhoneのボイスメモをそのまま使う
- 普段の演説・報告会の調子で3〜5分、途切れても言い直してもOK
- 内容例: 直近の市政報告の内容を話す／過去ブログを1本音読する
- 録音ファイルをMacに送って「これを声素材にして」と伝える

## 2. ElevenLabsアカウント作成

1. https://elevenlabs.io → Sign up（Googleアカウントで可）
2. プランは **Starter（$5/月）** でOK（月30分生成≒ショート動画40本ぶん）
   - 声の再現度に不満が出たら **Creator（$22/月）** にして Professional Voice Clone（高精度版・30分以上の素材推奨）へ昇格

## 3. Instant Voice Clone 登録

1. 左メニュー **Voices → Add a new voice → Instant Voice Clone**
2. 手順1の音声ファイルをアップロード
3. 名前: `Kusakawa`
4. 「本人の声である」旨の同意にチェック → Create

## 4. キーをMacに設置（ターミナルで実行 or Claudeに貼って依頼）

```bash
mkdir -p ~/.config/elevenlabs
echo 'ここにAPIキー' > ~/.config/elevenlabs/api_key
echo 'ここにボイスID' > ~/.config/elevenlabs/voice_id
chmod 600 ~/.config/elevenlabs/api_key ~/.config/elevenlabs/voice_id
```

- APIキー: 左下プロフィール → **API Keys** → Create（`sk_...`）
- ボイスID: **Voices → Kusakawa → ⋯ → Copy Voice ID**
- キーをClaude Codeのチャットに貼って「設置して」でもOK（こちらでファイル化します）

## 5. 本番テスト

Claudeに「**AIくさかわでテスト動画作って**」と言う → devなし生成 → 声の再現度を本人確認。
イマイチなら: 素材を録り直す（長め・クリアに）／Creatorプランで Professional Clone に昇格。
