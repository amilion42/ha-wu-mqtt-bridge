# Changelog

## 0.1.1

- Fix WU forwarding loop caused by aiohttp following redirects back through local DNS override
- Filter out -9999 sentinel values (WU "sensor unavailable") instead of publishing them to HA
- Throttle MQTT publishing with latest-value buffering — publishes the most recent reading when the throttle window expires, not the first one
- Deduplicate identical data points (same station + dateutc) arriving via multiple DNS-redirected hostnames
- Configurable publish interval (default 60s) to reduce update frequency
- Use HTTP instead of HTTPS for WU forwarding to avoid TLS issues with IP-based connections

## 0.1.0

- Initial release
- HTTPS/HTTP server accepting WU protocol uploads
- MQTT publishing with Home Assistant auto-discovery
- Dynamic sensor detection (known + unknown parameters)
- Optional forwarding to real Weather Underground servers
- Auto-generated self-signed TLS certificate
- MQTT auto-discovery from Mosquitto add-on
- Station availability tracking with configurable timeout
- Graceful shutdown with offline status publishing
