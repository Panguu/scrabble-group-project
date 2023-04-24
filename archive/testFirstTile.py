def AP(nums): #arithmetic progression
    if not isinstance(nums, list): raise Exception("Not a list")
    if len(nums) == 0: return 0 
    interval = nums[1] - nums[0]
    # validate interval
    for i in range(len(nums) - 1):
        if nums[i + 1] - nums[i] != interval: return None
    return interval


# pairs is tuple
def check_valid_pairs(pairs):
    AP_x = AP(list(map(lambda p: p[0], pairs)))
    if AP_x is None: return False
    AP_y = AP(list(map(lambda p: p[1], pairs)))
    if AP_y is None: return False
    return abs(sum([AP_x, AP_y])) == 1 and AP_x * AP_y == 0


# expect true
print(check_valid_pairs([(7,6), (7,7), (7,8)]))
# expect false
print(check_valid_pairs([(7,6), (7,7), (6, 7)]))

# expect true
print(check_valid_pairs([(6,7), (7,7), (8, 7)]))

# expect false
print(check_valid_pairs([(6,7), (7,7), (9, 7)]))