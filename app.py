plates = 4
on_one = [x for x in range(plates)]

# move n number of plates from t1 to t3
def move(n, tower1, tower3, tower2):
    # move the last disk to the "goal" tower
    if n == 1:
        print("Move final disk %i from tower %s to tower %s" % (n, tower1, tower3))
    else:
        move(n - 1, tower1, tower2, tower3)
        print("Move disk %i from tower %s to tower %s" % (n, tower1, tower3))
        move(n - 1, tower2, tower3, tower1)



move(3, "A", "C", "B")
