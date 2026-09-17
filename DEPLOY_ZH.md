# 激光加工论文邮件推送：部署说明

这是基于 [paper-firehose](https://github.com/zrbyte/paper-firehose) 的配置版本，监测 arXiv 应用物理、光学、材料，以及 npj Advanced Manufacturing、Communications Materials、Nature Communications 的 RSS。主题分为金属激光增材制造、在线熔池监测、OCT/OT 与双目视觉。

## 部署到 GitHub

1. 将这个目录上传到你自己的新 GitHub 仓库，建议仓库名 `laser-paper-digest`。保留 `.github/workflows/daily-digest.yml`。
2. 在仓库 `Settings → Secrets and variables → Actions` 创建以下 **Repository secrets**：

   | 名称 | 内容 |
   | --- | --- |
   | `SENDER_EMAIL` | 发信邮箱地址 |
   | `RECEIVER_EMAIL` | 收信邮箱地址 |
   | `SMTP_PASSWORD` | Gmail 的应用专用密码，**不是 Google 账号登录密码** |

   已预置 `smtp.gmail.com` 和 SSL 端口 `465`。如使用其他邮箱，可选填 `SMTP_SERVER`、`SMTP_PORT` 覆盖默认值。Gmail 的 SMTP 发信需要在 Google 账号中开启两步验证，然后创建应用专用密码并填入 `SMTP_PASSWORD`。邮箱的 IMAP 开关仅影响收信，不能代替这一步。

3. 打开 `Actions → Laser paper digest → Run workflow` 手动测试。首次运行要下载句向量模型，可能较慢。检查运行日志与收件箱。
4. 工作流按北京时间每天 08:00 请求执行。GitHub 的定时任务可能延迟；长时间无仓库活动可能再次自动停用，届时在 Actions 页面重新启用。

## 本地试运行

安装 Python 3.11 后，在本目录运行 `python -m pip install -e .`。复制 `github_actions_config` 到独立数据目录，并设置 `PAPER_FIREHOSE_DATA_DIR` 指向该目录的上级。设置同名环境变量后运行 `python scripts/prepare_email_config.py`。再执行：

```text
paper-firehose --config <数据目录>/config/config.yaml status
paper-firehose --config <数据目录>/config/config.yaml filter
paper-firehose --config <数据目录>/config/config.yaml rank
paper-firehose --config <数据目录>/config/config.yaml email --dry-run
```

先检查邮件预览，确认主题词的误报和漏报情况，再正式发送。

## 范围与限制

- 邮件支持已经配置，**自动写入 Zotero 尚未配置**。可从邮件中的 DOI 或链接用 Zotero Connector 保存感兴趣的条目。
- 当前期刊覆盖仍有限。特别是 Elsevier 的 *Additive Manufacturing* 等期刊需要可用 RSS 或增加 Crossref/OpenAlex 采集器。可在 `github_actions_config/config.yaml` 中增加来源。
- 当前英文语义模型适合英文标题和摘要；中文论文来源未纳入。
- 本配置不调用付费 LLM，邮件是文献条目与排序结果，不含生成式长摘要。

不要将邮箱密码、Zotero Key 或其他密钥写入仓库文件。
