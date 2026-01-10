#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "=== 🚀 Concurrent Tasks [$TIMESTAMP] ==="

gcc output_data/source_code/zombie_maker.c -o zombie_exec

# 5개 프로세스 동시 실행
for i in {1..5}; do
  ./zombie_exec &
done

# 시스템 스냅샷 로그 누적
LOG_FILE="output_data/logs/concurrent_history/sys_snapshot_${TIMESTAMP}.log"
{
  echo "snapshot_time: $TIMESTAMP"
  uptime
  free -h
  ps aux | grep 'Z\|defunct'
} > "$LOG_FILE"

wait
rm -f zombie_exec
echo "✅ Tasks Done."
