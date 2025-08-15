# Baidu Fanyi text-to-speech for HomeAssistant

本插件基于百度翻译的TTS服务，无需在百度语音开放平台申请appid等。


## 安装

> 下载并复制`custom_components/baidu_fanyi_tts`文件夹到HomeAssistant根目录下的`custom_components`文件夹

```shell
# Auto install via terminal shell
wget -q -O - https://cdn.jsdelivr.net/gh/al-one/hass-xiaomi-miot/install.sh | DOMAIN=baidu_fanyi_tts REPO_PATH=hasscc/hass-baidu-fanyi-tts bash -
```


## 配置

[UI: config - integrations - add integration - Baidu Fanyi TTS ]

config： \
<img width="500" height="300" alt="config" src="https://github.com/user-attachments/assets/141a206b-828d-46be-af64-40eeb024c619" />


### 支持的语言

```yaml
- `zh`  🇨🇳 汉语
- `cte` 🇨🇳 粤语
- `en`  🇬🇧 英语
- `ara` 🇸🇦 阿拉伯语
- `de`  🇩🇪 德语
- `fra` 🇫🇷 法语
- `kor` 🇰🇷 韩语
- `pt`  🇵🇹 葡萄牙语
- `ru`  🇷🇺 俄语
- `spa` 🇪🇸 西班牙语
- `th`  🇹🇭 泰语
```

## 使用

- [![Call service: tts.speak](https://my.home-assistant.io/badges/developer_call_service.svg)](https://my.home-assistant.io/redirect/developer_call_service/?service=tts.speak)
- [REST API: /api/tts_get_url](https://www.home-assistant.io/integrations/tts#post-apitts_get_url)

### 基本示例

```yaml
action: tts.speak
target:
  entity_id: tts.baidu_fanyi_tts
data:
  media_player_entity_id: media_player.your_player_entity_id
  message: 你好
```

### 完整示例

```yaml
action: tts.speak
target:
  entity_id: tts.baidu_fanyi_tts
data:
  media_player_entity_id: media_player.your_player_entity_id
  message: 吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮
  language: zh
  cache: true
  options:
    speed: 7
```

### Curl 示例

```shell
curl -X POST -H "Authorization: Bearer <ACCESS TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"platform": "tts.baidu_fanyi_tts", "message": "欢迎回家", "language": "zh", "cache": true, "options": {"speed": "7"}}' \
     http://home-assistant.local:8123/api/tts_get_url
```
