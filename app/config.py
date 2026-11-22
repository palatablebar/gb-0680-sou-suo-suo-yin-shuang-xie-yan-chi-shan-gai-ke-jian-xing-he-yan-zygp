from pathlib import Path
import os
ROOT=Path(__file__).resolve().parent.parent
DATA_DIR=Path(os.environ.get("DATA_DIR", "/tmp/indexparity"))
TITLE='搜索索引双写延迟与删改可见性核验'
SHORT='indexparity'
COLUMNS=['event_id', 'doc_id', 'version', 'op', 'source_time', 'visible_time', 'side', 'payload', 'reported', 'note']
MODULES=[('streams', '双端采信'), ('schema', '字段契约'), ('versions', '版本裁决'), ('visibility', '可见性重建'), ('latency', '延迟闸门'), ('parity', '双写对账'), ('backfills', '回补归档')]
RULE_VERSION="2026.11.17-r1"
