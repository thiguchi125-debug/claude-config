#!/usr/bin/env python3
"""UserPromptSubmit フック: 草川の自然な言い回しを担当スキル／エージェントへ案内する「単一入口」。

2026-09-06 棚卸しで判明した構造:
  14日間の手動セッション約110本のうち、スキル起動は kugiri 38回を除くと約60回。
  「投稿文としてどうか」「返信を考えて」「街頭演説のテーマは」など、担当が居る依頼が
  トリガー語と一致せず、本体セッションが直接答えていた（主担当agent省略）。
このフックは判定だけを行い、本文に1〜2行の案内を注入する。強制はしない。
"""
import json
import re
import sys

# (正規表現, 担当, 一言)。上から順に最大2件まで案内する。
RULES = [
    (r"^(おはよう|おはよ|morning)", "ohayo", "朝のブリーフィング"),
    (r"^(おやすみ|good night)", "oyasumi", "夜のまとめ"),
    (r"区切|引き継ぎメモ|セッション切|^再開", "kugiri", "区切り／再開"),
    (r"記録", "nichijo", "日次記録（『記録』を含む発言は必ず）"),
    (r"どこ[？?]|どこだっけ|探して|見つけて", "smart-intake（モードB）", "横断検索"),
    (r"会議メモ|^メモ[:：]|保存して|と話した|の件$", "smart-intake（モードA）", "保存先の自動振り分け"),
    (r"意見(が)?届いた|意見コピペ|DMで|フォーム回答|相談コピペ", "iken", "市民意見の登録＋返信3案"),
    (r"返信(を)?(考えて|案)|どう返(そう|す)|返事(を)?(考えて|作って)", "citizen-inquiry-responder（agent）", "返信3案＋次アクション"),
    (r"投稿文|投稿にして|投稿(を)?作って|投稿としてどうか|SNS(に|で|投稿)|インスタ.*(文|投稿)|Xに", "spark（1テーマ）／sns-content-creator（agent）", "SNS原稿。安全ゲート必須"),
    (r"発信ネタ|ひらめき|ネタにして|発信できる|この記事", "spark", "小さな種→発信"),
    (r"ブログ", "content-pipeline／blog-writer(-normal)", "ブログ。冒頭定型＋安全ゲート2段＋サムネ要否を1問"),
    (r"一式|フル展開|全部作って|ブログもSNSも", "content-pipeline", "発信一式"),
    (r"ショート動画|TikTok|Reels|動画(を)?作って", "short-video-create", "台本→ゲート→画像→7PF"),
    (r"この写真で|写真(を|から)投稿", "photo-post", "写真1〜3枚→投稿画像"),
    (r"街頭|街宣|駅前で話す|駅頭", "daily-street-speech（agent）", "トーキングポイント3型"),
    (r"挨拶|懇親会|総会で|集会で話す", "community-rally-speaker（agent）", "地域集会向け短尺演説（aisatsu-prepは凍結中）"),
    (r"スピーチ|演説原稿|祝辞|弔辞|所信表明|年頭", "speech-writer（agent）", "格式スピーチ"),
    (r"チラシ|ポスター|印刷物|リーフレット|三つ折り|市政報告レポート", "design-studio（地区版はchiku-report）", "印刷物。最新表示は show_latest.sh"),
    (r"報告会", "shisei-houkokukai", "5ステージ（企画/案内/スライド/台本/前夜）"),
    (r"一般質問|通告|質問(の)?流れ|想定質問", "general-question-prep／general-question-architect", "会期ハブ×設計"),
    (r"想定答弁|再質問|議会前夜|前夜チェック", "counter-argument-simulator（agent）", "答弁3型＋再質問カード"),
    (r"議案|補正予算|条例(改正)?|請願", "agenda-analyzer／bill-scrutiny-architect（agent）", "議案カルテ／質疑設計"),
    (r"議会だより", "gikai-dayori-creator（agent）", "会議録→650字"),
    (r"意見書|要望書", "ikensho-drafter（agent）", "様式準拠ドラフト"),
    (r"他(の)?自治体|先進事例|事例(を)?調べ|データ(を)?集め|国の(方針|通達)", "policy-researcher／kameyama-researcher（agent）", "先に research_ledger を grep"),
    (r"亀山市の.*(調べ|確認|教えて)|担当課|市の(制度|施策)", "kameyama-researcher（agent）", "市公式・議事録・担当課"),
    (r"市民の声.*(分析|傾向)|世論|何を求めて", "citizen-voice-analyst（agent）", "声コーパス分析"),
    (r"過去(の)?(発言|主張)|アーカイブ|前に(質問|言った)", "policy-archive-miner（agent）", "草川の過去発言の深掘り"),
    (r"実績(を)?(まとめ|集)|答弁(の)?追跡|検討しますの|回収チェック", "toben-tracker（agent）", "約束台帳"),
    (r"ハザード|防災カルテ|浸水|土砂", "district-hazard-analyst（agent）", "地区防災カルテ"),
    (r"票|得票|重点地区|街宣ルート|ポスティング", "electoral-district-strategist（agent）", "データ選挙戦略"),
    (r"政策(アップデート|候補|レーダー)|省庁", "policy-radar", "政策発掘→🎯ネタDB"),
    (r"ニュース", "news-briefing", "当日分は📰ニュースDB"),
    (r"タスク(登録|にして|に入れ)|Todoist(に|へ)", "task-add", "カレンダー突合→登録"),
    (r"棚卸し|タスク(整理|監査)", "task-audit", "6チェック"),
    (r"逆算|準備漏れ", "gyakusan", "イベント逆算"),
    (r"取り込んで|取込", "夜間 _root_intake.py 任せ（drive-intakeは凍結中）", "Drive直下に置けば翌朝配置"),
    (r"AIインタビュー|ヒアリング設計", "ai-interview-config-designer（agent）", "設定DB登録まで"),
    (r"節約|燃費|lean", "lean-mode", "品質据え置きの節約"),
]

SKIP_PREFIX = ("/", "あなたは草川", "# 草川たくや", "<")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = (data.get("prompt") or "").strip()
    if not prompt or len(prompt) > 3000 or prompt.startswith(SKIP_PREFIX):
        return
    head = prompt[:300]
    hits = []
    for pat, owner, note in RULES:
        if re.search(pat, head):
            hits.append("%s → %s（%s）" % (re.search(pat, head).group(0), owner, note))
        if len(hits) >= 2:
            break
    if not hits:
        return
    print("🧭 担当の目安: " + "／".join(hits)
          + "。担当スキル／agentを省略せず起動する（feedback_content_generation_default_flow）。"
          + "違うと思えば無視してよい。")


if __name__ == "__main__":
    main()
