import asyncio
from lib2to3.pgen2.tokenize import untokenize
from time import time
from timeit import timeit

unroll_2 = """
p = [-0.5937666, 0.684082, -0.5772033, 0.3481369, 0.0965215, 0.3667577]
q = [0.7946288, -0.4162117, 0.1517516, -0.4744227, -0.193617, 0.3375438]
p_flag = True
kernel_size = 2
i = 0
s = 0

norm_p = 0
norm_q = 0
len_q = len(q)

while i < len_q:
    s += p[i] * q[i]
    s += p[i+1] * q[i+1]

    if p_flag:
        norm_p += p[i] ** 2
        norm_p += p[i+1] ** 2

    norm_q += q[i] ** 2
    norm_q += q[i+1] ** 2

    i += kernel_size
"""
unroll_3 = """
p = [-0.5937666, 0.684082, -0.5772033, 0.3481369, 0.0965215, 0.3667577]
q = [0.7946288, -0.4162117, 0.1517516, -0.4744227, -0.193617, 0.3375438]
p_flag = True
kernel_size = 3
i = 0
s = 0

norm_p = 0
norm_q = 0
len_q = len(q)

while i < len_q:
    s += p[i] * q[i]
    s += p[i+1] * q[i+1]
    s += p[i+2] * q[i+2]

    if p_flag:
        norm_p += p[i] ** 2
        norm_p += p[i+1] ** 2
        norm_p += p[i+2] ** 2

    norm_q += q[i] ** 2
    norm_q += q[i+1] ** 2
    norm_q += q[i+2] ** 2

    i += kernel_size
"""

no_unroll = """
p = [-0.5937666, 0.684082, -0.5772033, 0.3481369, 0.0965215, 0.3667577]
q = [0.7946288, -0.4162117, 0.1517516, -0.4744227, -0.193617, 0.3375438]
dot = p[5] * q[5] + p[1] * q[1] + p[3] * q[3] + p[2] * q[2] + p[4] * q[4] + p[0] * q[0]
norm_p = pow(p[5] * p[5] + p[1] * p[1] + p[3] * p[3] + p[2] * p[2] + p[4] * p[4] + p[0] * p[0], 1/2)
norm_q = pow(q[5] * q[5] + q[1] * q[1] + q[3] * q[3] + q[2] * q[2] + q[4] * q[4] + q[0] * q[0], 1/2)
"""

RUNS = 100
ITER = 100000

async def avg_time(stmt, tag):
    t = 0
    for i in range(RUNS):
        t+= timeit(stmt=stmt, number=ITER)
    print(f"AVG for {tag}, RAN {ITER} times :", t/RUNS)


async def main():
    await asyncio.gather(
        avg_time(unroll_2, "unroll_2"),
        avg_time(unroll_3, "unroll_3"),
        avg_time(no_unroll,"no_unroll")
    )

asyncio.run(main())
