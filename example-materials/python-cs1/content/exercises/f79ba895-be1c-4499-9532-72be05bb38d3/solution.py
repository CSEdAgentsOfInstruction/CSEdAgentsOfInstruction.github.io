age = int(input())
agreement = input().strip().lower()

old_enough = age >= 16
agreed_to_rules = agreement == "yes"
may_access = old_enough and agreed_to_rules

print(may_access)
