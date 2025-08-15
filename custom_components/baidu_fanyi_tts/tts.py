"""The Baidu Fanyi speech service."""
import logging
import time
import asyncio
import aiohttp
from http import HTTPStatus
from typing import Any
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.tts import (
    CONF_LANG,
    TextToSpeechEntity,
    TtsAudioType,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_SPEED, DEFAULT_SPEED, DEFAULT_AGENT, DEFAULT_LANG, SUPPORTED_LANGUAGES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Baidu Fanyi TTS entity from a config entry."""
    entity = BaiduFanyiTTSEntity(hass, config_entry)
    async_add_entities([entity])


class BaiduFanyiTTSEntity(TextToSpeechEntity):
    """The Baidu Fanyi TTS entity."""

    _attr_name = "Baidu Fanyi TTS"
    _attr_supported_languages = SUPPORTED_LANGUAGES
    
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize Baidu Fanyi TTS entity."""
        self.hass = hass
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}-baidu-fanyi-tts"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "Baidu Fanyi TTS",
            "manufacturer": "Baidu",
            "model": "Cloud TTS",
            "entry_type": DeviceEntryType.SERVICE,
        }

    @property
    def default_language(self) -> str:
        """Return the default language from options."""
        return self._config_entry.options.get(CONF_LANG, DEFAULT_LANG)

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [CONF_SPEED]

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> TtsAudioType:
        """Load TTS audio from Baidu Fanyi API."""
        # 获取配置和选项值
        config = self._config_entry.options
        lang = language or config.get(CONF_LANG, DEFAULT_LANG)
        speed = options.get(CONF_SPEED, config.get(CONF_SPEED, DEFAULT_SPEED))
        
        _LOGGER.debug('%s request: %s', self.name, [message, {'lang': lang, 'speed': speed}])
        
        session = async_get_clientsession(self.hass)
        
        try:
            async with asyncio.timeout(15):
                # 准备请求参数
                params = {
                    'lan': lang,
                    'text': message,
                    'spd': speed,
                    'source': 'web',
                }
                headers = {
                    'Host': 'fanyi.baidu.com',
                    'Referer': 'https://fanyi.baidu.com/',
                    'User-Agent': DEFAULT_AGENT,
                }
                
                # 发送请求并计时
                start_time = time.perf_counter()
                response = await session.get(
                    'https://fanyi.baidu.com/gettts',
                    params=params,
                    headers=headers,
                )
                
                # 检查响应状态
                if response.status != HTTPStatus.OK:
                    error_text = await response.text()
                    _LOGGER.error(
                        'API error %d: %s', response.status, error_text
                    )
                    raise HomeAssistantError(f"API returned {response.status}")
                    
                # 读取音频数据
                data = await response.read()
                elapsed_time = (time.perf_counter() - start_time) * 1000
                _LOGGER.debug('TTS request completed in %.1fms', elapsed_time)
                
                return 'mp3', data
                
        except asyncio.TimeoutError:
            _LOGGER.error('Request timed out')
            raise HomeAssistantError("Request timed out")
            
        except aiohttp.ClientError as exc:
            _LOGGER.error('Network error: %s', exc)
            raise HomeAssistantError(f"Network error: {exc}")