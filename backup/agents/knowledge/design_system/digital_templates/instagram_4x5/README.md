# Instagram 4:5スターター

- 出力：1080×1350px PNG
- 上部86px、下部155pxをUIとプロフィール表示を考慮した固定帯として設計
- 一枚一メッセージを原則とし、本文は4行程度まで
- 写真は`.photo`を実画像へ置換し、顔と目線を1080px表示で確認する

```bash
~/.agents/bin/design-render \
  --html ~/.agents/knowledge/design_system/digital_templates/instagram_4x5/template.html \
  --output-dir ./render-instagram \
  --profile instagram-4x5
```
