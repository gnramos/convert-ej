import random
import sys

random.seed(sys.argv[1])
print(''.join(c for _ in range(random.randint(1, 1000))
              for c in random.choice(['C', 'O'])))
