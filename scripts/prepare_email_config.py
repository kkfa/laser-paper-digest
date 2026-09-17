"""Write runtime email settings from environment variables (never commit secrets)."""
import os
from pathlib import Path

import yaml


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required secret: {name}")
    return value


data_dir = Path(os.environ["PAPER_FIREHOSE_DATA_DIR"])
config_path = data_dir / "config" / "config.yaml"
config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
sender = required("SENDER_EMAIL")
receiver = required("RECEIVER_EMAIL")
config["email"]["from"] = sender
config["email"]["smtp"]["username"] = sender
config["email"]["smtp"]["host"] = os.environ.get("SMTP_SERVER", "").strip() or "smtp.gmail.com"
config["email"]["smtp"]["port"] = int(os.environ.get("SMTP_PORT", "").strip() or "465")
config["defaults"]["abstracts"]["mailto"] = sender
config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")

secrets_dir = data_dir / "config" / "secrets"
secrets_dir.mkdir(parents=True, exist_ok=True)
(secrets_dir / "email_password.env").write_text(required("SMTP_PASSWORD"), encoding="utf-8")
recipients = {"recipients": [{"to": receiver, "topics": ["laser_additive_manufacturing", "in_situ_monitoring", "optical_metrology"], "mode": "ranked", "limit": 12}]}
(secrets_dir / "mailing_lists.yaml").write_text(yaml.safe_dump(recipients, allow_unicode=True), encoding="utf-8")
print("Email settings prepared without printing credentials.")
