# Baidu Fanyi text-to-speech for HomeAssistant

本插件基于百度翻译的TTS服务，无需在百度语音开放平台申请appid等。


## 安装

> 下载并复制`custom_components/baidu_fanyi_tts`文件夹到HomeAssistant根目录下的`custom_components`文件夹

```shell
# Auto install via terminal shell
wget -q -O - https://cdn.jsdelivr.net/gh/al-one/hass-xiaomi-miot/install.sh | DOMAIN=baidu_fanyi_tts REPO_PATH=al-one/hass-baidu-fanyi-tts bash -
```


## 配置

```yaml
# configuration.yaml
tts:
  - platform: baidu_fanyi_tts
    language: zh # 默认语言(可选)
    speed: 5     # 默认语速(可选)
```


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
