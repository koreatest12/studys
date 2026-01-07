#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "=== 🚀 Starting Concurrent Operations [$TIMESTAMP] ==="

# [Task 1] 좀비 프로세스 생성기 컴파일
gcc output_data/source_code/zombie_maker.c -o zombie_exec

# [Task 2] 동시성 테스트: 5개의 프로세스 병렬 실행
echo ">>> Spawning 5 Concurrent Processes..."
for i in {1..5}; do
  (
    echo "[Job $i] Started..."
    # 각각 다른 이름으로 복사하여 실행 (중복 수행 시뮬레이션)
    cp zombie_exec zombie_run_$i
    ./zombie_run_$i &
    PID=$!
    echo "[Job $i] PID: $PID running in background"
  ) &
done

# [Task 3] 시스템 부하 및 로그 스냅샷 (누적 저장)
LOG_FILE="output_data/logs/concurrent_history/sys_snapshot_${TIMESTAMP}.log"
echo "Recording System Snapshot to $LOG_FILE"

# 약간의 딜레이를 주어 프로세스들이 실행된 상태를 포착
sleep 2

{
  echo "=== System Snapshot at $TIMESTAMP ==="
  echo "--- Load Average ---"
  uptime
  echo "--- Memory Usage ---"
  free -h
  echo "--- Zombie Processes Detect ---"
  ps aux | grep 'Z\|defunct' | grep -v grep
  echo "--- Total Process Count ---"
  ps aux | wc -l
} > "$LOG_FILE"

# 백그라운드 작업들이 안정화될 때까지 대기
wait
# 임시 실행 파일 정리
rm -f zombie_run_* zombie_exec
echo "✅ Concurrent Tasks Finished."
