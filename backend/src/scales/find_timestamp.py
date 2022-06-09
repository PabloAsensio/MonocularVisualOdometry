def find_timestamp(tss_gt: list, ts: int) -> str:
    return min(tss_gt, key=lambda x:abs(x-ts))