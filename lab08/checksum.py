def calc(arr, k = 16):
  sum = 0
  for i in range(0, len(arr), k // 8):
    sum += int.from_bytes(arr[i : min(len(arr), i + k // 8)])
    sum &= (1 << k) - 1;
  return ((1 << k) - 1) ^ sum;

def check(arr, sum, k = 16):
  if sum >= (1 << k):
    return False
  for i in range(0, len(arr), k // 8):
    sum += int.from_bytes(arr[i : i + k // 8])
    sum &= (1 << k) - 1
  return sum == (1 << k) - 1

text = "His palms are sweaty, knees weak, arms are heavy. There's vomit on his sweater already, mom's spaghetti"
arr = text.encode()
checksum = calc(arr)
assert check(arr, checksum)

checksum = calc(arr) ^ 1
assert not check(arr, checksum)

checksum = calc(arr)
arr = text.capitalize().encode()
assert not check(arr, checksum)
