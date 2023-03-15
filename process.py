with open("./output", "w") as output:

    d = ["" for _ in range(19683)]

    with open("./out", "r") as out:
        lines = out.readlines()
        for line in lines:
            (index, mapping, counter) = line.split("|")
            (pre, post) = index.split("/")
            pre = int(pre)
            d[pre] = line

    with open("./out-rev", "r") as out_rev:
        lines = out_rev.readlines()
        for line in lines:
            (index, mapping, counter) = line.split("|")
            (pre, post) = index.split("/")
            pre = int(pre)
            pre = 19682 - pre
            index = f"{pre} /{post}"
            if d[pre] is not None:
                d[pre] = f"{index}|{mapping}|{counter}"

    output.writelines(d)
