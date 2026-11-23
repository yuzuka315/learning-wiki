# 操作紀錄

## 2026-11-16 建立 Wiki
- 主題定為「高效學習法」。
- 建立三層結構與規則檔 `CLAUDE.md`。
- 取得 5 篇原始資料存入 `raw/`（另有 1 篇 Wikipedia "Interleaving" 頁面網址無效，未取得）。

## 2026-11-16 ingest S1：Spaced repetition
- 討論後的決定：
  - 概念頁的歷史人物只留 Ebbinghaus、Mace、Leitner，其餘放來源頁。
  - 收錄「遞增間隔與固定間隔效果相近」這個限制，不寫成「一定要越拉越長」。
- 使用者提出的問題：遺忘曲線的實驗是背無意義的內容，有意義的內容遺忘速度是否不同？→ 留待 ingest S3（Forgetting curve）時處理。
- 新增：`sources/s1-spaced-repetition.md`、`concepts/spaced-repetition.md`
- 更新：`index.md`

## 2026-11-16 ingest S3：Forgetting curve
- 討論後的決定：
  - 使用者的問題（無意義內容 vs 有意義內容）成為概念頁「限制與注意」的第一條。
  - 來源沒有給「有意義內容慢多少」的數字，所以不寫具體差距。
  - 「24 小時內複習可重設曲線」收錄，但標明是主張、非定論。
- 更正：使用者原本記得是背「數列」，來源寫的是無意義音節（nonsense syllables）。
- 新增：`sources/s3-forgetting-curve.md`、`concepts/forgetting-curve.md`

## 2026-11-16 ingest S2：Testing effect
- 討論後的決定：
  - 來源沒有效果量或百分比，概念頁與簡報都以文字說明，不寫「提升幾 %」。
- 新增：`sources/s2-testing-effect.md`、`concepts/testing-effect.md`
- 更新：`concepts/spaced-repetition.md`（補相關頁面連結）、`index.md`

## 2026-11-23 ingest S4、S5：Desirable difficulty、Dunlosky
- 討論後使用者的決定：
  - S4 延後回饋那句擷取壞掉，整句不收，只留「任何回饋都比沒有好」。
  - S2 與 S5 對「卡片何時移出」的說法不同：兩邊都寫，並標明差別在移出之後有沒有再測。
  - 新增三個概念頁：有益的困難、學習策略評比、交錯練習；追問為什麼與自我解釋只放在評比頁，不另開。共 6 個概念頁。
- 新增：`sources/s4-desirable-difficulty.md`、`sources/s5-dunlosky-toolbox.md`、`concepts/desirable-difficulty.md`、`concepts/study-strategy-ratings.md`、`concepts/interleaved-practice.md`
- 更新：`concepts/testing-effect.md`（補 S5 差異與連結）、`concepts/spaced-repetition.md`、`concepts/forgetting-curve.md`（相關頁面）、`index.md`

## 2026-11-23 lint
- 檢查：概念頁每一條都有 `[S#]`、連結沒有失效、每頁都收進 index、沒有互相矛盾的說法。結果：沒有問題。
- 網頁版導覽修正：每頁上方改為「首頁 / Wiki 目錄 / 本頁」，Wiki 目錄頁不再連到自己。
