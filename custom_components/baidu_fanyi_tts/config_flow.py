import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.components.tts import CONF_LANG
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode
from .const import CONF_SPEED, DOMAIN, DEFAULT_SPEED, DEFAULT_AGENT, DEFAULT_LANG, SUPPORTED_LANGUAGES

class BaiduFanyiTTSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """BaiduFanyi TTS config flow."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        # 检查是否已经有配置条目
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # 创建一个空的配置条目
        return self.async_create_entry(title="Baidu Fanyi TTS", data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return BaiduFanyiTTSOptionsFlowHandler(config_entry)

class BaiduFanyiTTSOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for BaiduFanyi TTS."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # 更新配置到 hass.data
            self.hass.data[DOMAIN] = user_input
            return self.async_create_entry(title="Baidu Fanyi TTS Options", data=user_input)

        # 默认值从现有配置中读取，如果不存在则使用默认值
        default_language = self._config_entry.options.get(CONF_LANG, DEFAULT_LANG)
        default_speed = self._config_entry.options.get(CONF_SPEED, DEFAULT_SPEED)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_LANG, 
                    default=default_language): SelectSelector(
                    SelectSelectorConfig(
                        options=SUPPORTED_LANGUAGES,
                        multiple=False,translation_key=CONF_LANG
                    )
                ),
                vol.Required(CONF_SPEED, default=default_speed): int,
            })
        )
