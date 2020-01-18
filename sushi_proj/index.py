import sys
import MeCab
m = MeCab.Tagger("-Ochasen")
print(m.parse("トロが美味しい。柔らかく口の中でほどけるシャリの旨味も相まって最高。"))
#m.parse("トロが美味しい。柔らかく口の中でほどけるシャリの旨味も相まって最高。")
