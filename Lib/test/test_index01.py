"""
unittests for 1-based indexing and relatives
"""

import unittest
from test import support

class Reveal:
    def __getitem__(self, arg):
        return arg

reveal = Reveal()

class Index01TestCase_SingleKey(unittest.TestCase):

    def test_integer_in_braces(self):
        s = "ABCDEFG"
        
        for i in range(-len(s), len(s)):
            with self.subTest(i=i):
                self.assertEqual(s{i+1}, s[i])
        
        for i in (-len(s)-1, len(s)):
            with self.subTest(i=i):
                with self.assertRaises(IndexError):
                    s{i+1}

    def test_semiopen_slice_in_braces(self):
        s = "ABCDEFG"

        # s[:]
        self.assertEqual(s{:}, s[:])
        self.assertEqual(s{None:}, s[:])
        self.assertEqual(s{:None}, s[:])
        self.assertEqual(s{None:None}, s[:])
        self.assertEqual(s{None:None:None}, s[:])
        
        # We also try invalid indices i, j
        
        # s[i:]
        for i in range(-len(s)-2, len(s)+3):
            with self.subTest(i=i):
                self.assertEqual(s{i+1:}, s[i:])
                self.assertEqual(s{i+1:None}, s[i:])
                self.assertEqual(s{i+1::}, s[i:])
                self.assertEqual(s{i+1:None:}, s[i:])
                self.assertEqual(s{i+1:None:None}, s[i:])

        # s[:j]
        for j in range(-len(s)-2, len(s)+3):
            with self.subTest(j=j):
                self.assertEqual(s{:j+1}, s[:j])
                self.assertEqual(s{:j+1:None}, s[:j])
                self.assertEqual(s{None:j+1}, s[:j])
                self.assertEqual(s{None:j+1:None}, s[:j])
        
        # s[::k]
        for k in (1, 2, 3, -1, -2, -3):
            with self.subTest(k=k):
                self.assertEqual(s{::k}, s[::k])
                self.assertEqual(s{None::k}, s[::k])
                self.assertEqual(s{:None:k}, s[::k])
                self.assertEqual(s{None:None:k}, s[::k])
            

        # s[i:j]
        for i in range(-len(s)-2, len(s)+3):
            for j in range(-len(s)-2, len(s)+3):
                with self.subTest(i=i, j=j):
                    self.assertEqual(s{i+1:j+1}, s[i:j])
                    self.assertEqual(s{i+1:j+1:None}, s[i:j])
        
        # s[i::k]
        for i in range(-len(s)-2, len(s)+3):
            for k in (1, 2, 3, -1, -2, -3):
                with self.subTest(i=i, k=k):
                    self.assertEqual(s{i+1::k}, s[i::k])
                    self.assertEqual(s{i+1:None:k}, s[i::k])

        # s[:j:k]
        for j in range(-len(s)-2, len(s)+3):
            for k in (1, 2, 3, -1, -2, -3):
                with self.subTest(j=j, k=k):
                    self.assertEqual(s{:j+1:k}, s[:j:k])
                    self.assertEqual(s{None:j+1:k}, s[:j:k])

        # s[i:j:k]
        for i in range(-len(s)-2, len(s)+3):
            for j in range(-len(s)-2, len(s)+3):
                for k in (1, 2, 3, -1, -2, -3):
                    with self.subTest(j=j, k=k):
                        self.assertEqual(s{i+1:j+1:k}, s[i:j:k])


    def test_closed_slice_on_tiny_example_no_step(self):
        s = "012"

        self.assertEqual(s[:0::], "0")
        self.assertEqual(s[:1::], "01")
        self.assertEqual(s[:2::], "012")
        self.assertEqual(s[:-1::], "012")
        self.assertEqual(s[:-2::], "01")
        self.assertEqual(s[:-3::], "0")
        self.assertEqual(s[:-4::], "")
        
        self.assertEqual(s[0:0::], "0")
        self.assertEqual(s[0:1::], "01")
        self.assertEqual(s[0:2::], "012")
        self.assertEqual(s[0:-1::], "012")
        self.assertEqual(s[0:-2::], "01")
        self.assertEqual(s[0:-3::], "0")
        self.assertEqual(s[0:-4::], "")

        self.assertEqual(s[1:0::], "")
        self.assertEqual(s[1:1::], "1")
        self.assertEqual(s[1:2::], "12")
        self.assertEqual(s[1:-1::], "12")
        self.assertEqual(s[1:-2::], "1")
        self.assertEqual(s[1:-3::], "")
        self.assertEqual(s[1:-4::], "")

        self.assertEqual(s[-2:0::], "")
        self.assertEqual(s[-2:1::], "1")
        self.assertEqual(s[-2:2::], "12")
        self.assertEqual(s[-2:-1::], "12")
        self.assertEqual(s[-2:-2::], "1")
        self.assertEqual(s[-2:-3::], "")
        self.assertEqual(s[-2:-4::], "")

        self.assertEqual(s[2:0::], "")
        self.assertEqual(s[2:1::], "")
        self.assertEqual(s[2:2::], "2")
        self.assertEqual(s[2:-1::], "2")
        self.assertEqual(s[2:-2::], "")
        self.assertEqual(s[2:-3::], "")
        self.assertEqual(s[2:-4::], "")

        self.assertEqual(s[-1:0::], "")
        self.assertEqual(s[-1:1::], "")
        self.assertEqual(s[-1:2::], "2")
        self.assertEqual(s[-1:-1::], "2")
        self.assertEqual(s[-1:-2::], "")
        self.assertEqual(s[-1:-3::], "")
        self.assertEqual(s[-1:-4::], "")
        
        self.assertEqual(s[3:0::], "")
        self.assertEqual(s[3:1::], "")
        self.assertEqual(s[3:2::], "")
        self.assertEqual(s[3:-1::], "")
        self.assertEqual(s[3:-2::], "")
        self.assertEqual(s[3:-3::], "")
        self.assertEqual(s[3:-4::], "")

    def test_closed_slice_on_tiny_example_step_2(self):
        s = "012"

        self.assertEqual(s[:0::2], "0")
        self.assertEqual(s[:1::2], "0")
        self.assertEqual(s[:2::2], "02")
        self.assertEqual(s[:-1::2], "02")
        self.assertEqual(s[:-2::2], "0")
        self.assertEqual(s[:-3::2], "0")
        self.assertEqual(s[:-4::2], "")
        
        self.assertEqual(s[0:0::2], "0")
        self.assertEqual(s[0:1::2], "0")
        self.assertEqual(s[0:2::2], "02")
        self.assertEqual(s[0:-1::2], "02")
        self.assertEqual(s[0:-2::2], "0")
        self.assertEqual(s[0:-3::2], "0")
        self.assertEqual(s[0:-4::2], "")

        self.assertEqual(s[1:0::2], "")
        self.assertEqual(s[1:1::2], "1")
        self.assertEqual(s[1:2::2], "1")
        self.assertEqual(s[1:-1::2], "1")
        self.assertEqual(s[1:-2::2], "1")
        self.assertEqual(s[1:-3::2], "")
        self.assertEqual(s[1:-4::2], "")

        self.assertEqual(s[-2:0::2], "")
        self.assertEqual(s[-2:1::2], "1")
        self.assertEqual(s[-2:2::2], "1")
        self.assertEqual(s[-2:-1::2], "1")
        self.assertEqual(s[-2:-2::2], "1")
        self.assertEqual(s[-2:-3::2], "")
        self.assertEqual(s[-2:-4::2], "")

        self.assertEqual(s[2:0::2], "")
        self.assertEqual(s[2:1::2], "")
        self.assertEqual(s[2:2::2], "2")
        self.assertEqual(s[2:-1::2], "2")
        self.assertEqual(s[2:-2::2], "")
        self.assertEqual(s[2:-3::2], "")
        self.assertEqual(s[2:-4::2], "")

        self.assertEqual(s[-1:0::2], "")
        self.assertEqual(s[-1:1::2], "")
        self.assertEqual(s[-1:2::2], "2")
        self.assertEqual(s[-1:-1::2], "2")
        self.assertEqual(s[-1:-2::2], "")
        self.assertEqual(s[-1:-3::2], "")
        self.assertEqual(s[-1:-4::2], "")
        
        self.assertEqual(s[3:0::2], "")
        self.assertEqual(s[3:1::2], "")
        self.assertEqual(s[3:2::2], "")
        self.assertEqual(s[3:-1::2], "")
        self.assertEqual(s[3:-2::2], "")
        self.assertEqual(s[3:-3::2], "")
        self.assertEqual(s[3:-4::2], "")

    def test_closed_slice_on_tiny_example_step_minus2(self):
        s = "012"

        self.assertEqual(s[:0::-2], "20")
        self.assertEqual(s[:1::-2], "2")
        self.assertEqual(s[:2::-2], "2")
        self.assertEqual(s[:-1::-2], "2")
        self.assertEqual(s[:-2::-2], "2")
        self.assertEqual(s[:-3::-2], "20")
        self.assertEqual(s[:-4::-2], "20")
        
        self.assertEqual(s[0:0::-2], "0")
        self.assertEqual(s[0:1::-2], "")
        self.assertEqual(s[0:2::-2], "")
        self.assertEqual(s[0:-1::-2], "")
        self.assertEqual(s[0:-2::-2], "")
        self.assertEqual(s[0:-3::-2], "0")
        self.assertEqual(s[0:-4::-2], "0")

        self.assertEqual(s[1:0::-2], "1")
        self.assertEqual(s[1:1::-2], "1")
        self.assertEqual(s[1:2::-2], "")
        self.assertEqual(s[1:-1::-2], "")
        self.assertEqual(s[1:-2::-2], "1")
        self.assertEqual(s[1:-3::-2], "1")
        self.assertEqual(s[1:-4::-2], "1")

        self.assertEqual(s[-2:0::-2], "1")
        self.assertEqual(s[-2:1::-2], "1")
        self.assertEqual(s[-2:2::-2], "")
        self.assertEqual(s[-2:-1::-2], "")
        self.assertEqual(s[-2:-2::-2], "1")
        self.assertEqual(s[-2:-3::-2], "1")
        self.assertEqual(s[-2:-4::-2], "1")

        self.assertEqual(s[2:0::-2], "20")
        self.assertEqual(s[2:1::-2], "2")
        self.assertEqual(s[2:2::-2], "2")
        self.assertEqual(s[2:-1::-2], "2")
        self.assertEqual(s[2:-2::-2], "2")
        self.assertEqual(s[2:-3::-2], "20")
        self.assertEqual(s[2:-4::-2], "20")

        self.assertEqual(s[-1:0::-2], "20")
        self.assertEqual(s[-1:1::-2], "2")
        self.assertEqual(s[-1:2::-2], "2")
        self.assertEqual(s[-1:-1::-2], "2")
        self.assertEqual(s[-1:-2::-2], "2")
        self.assertEqual(s[-1:-3::-2], "20")
        self.assertEqual(s[-1:-4::-2], "20")
        
        self.assertEqual(s[3:0::-2], "20")
        self.assertEqual(s[3:1::-2], "2")
        self.assertEqual(s[3:2::-2], "2")
        self.assertEqual(s[3:-1::-2], "2")
        self.assertEqual(s[3:-2::-2], "2")
        self.assertEqual(s[3:-3::-2], "20")
        self.assertEqual(s[3:-4::-2], "20")

    def test_closed_slice_step_minus1(self):
        s = "ABCDEFG"
        
        # for a closed slice, [i:j::-1] = reversed [j:i::]
        for i in range(-len(s)-2, len(s)+3):
            for j in range(-len(s)-2, len(s)+3):
                with self.subTest(i=i, j=j):
                    self.assertEqual(s[i:j::-1], s[j:i::][::-1])
        

from dataclasses import dataclass
@dataclass
class CLOSED:
    x: object

@dataclass
class BRACED:
    x: object

class Reveal:
    def __getitem__(self, key):
        return key
    
    def __xkey__(self, key, braced, closed):
        if braced: key = BRACED(key)
        if closed: key = CLOSED(key)
        return key

reveal = Reveal()

class Index01TestCase_xkey(unittest.TestCase):
    
    def test_braced(self):
        self.assertEqual(reveal[1], 1)
        self.assertEqual(reveal{1}, BRACED(1))
        self.assertEqual(reveal[1, 2], (1, 2))
        self.assertEqual(reveal{1, 2}, (BRACED(1), BRACED(2)))
        self.assertEqual(reveal{1}.[2], (BRACED(1), 2))
        self.assertEqual(reveal[1].{2}, (1, BRACED(2)))
    
    def test_star(self):
        x = (7, 8, 9)
        
        self.assertEqual(reveal[*x], x)
        self.assertEqual(reveal[1, *x], (1,) + x)
        self.assertEqual(reveal[*x, 2], x + (2,))
        self.assertEqual(reveal[1, *x, 2], (1,) + x + (2,))
        
        def B(t):
            return tuple(BRACED(x) for x in t)
        
        self.assertEqual(reveal{*x}, B(x))
        self.assertEqual(reveal{1, *x}, B((1,) + x))
        self.assertEqual(reveal{*x, 2}, B(x + (2,)))
        self.assertEqual(reveal{1, *x, 2}, B((1,) + x + (2,)))
    
    def test_closed(self):
        self.assertEqual(reveal[1:2::3], CLOSED(slice(1, 2, 3)))
        self.assertEqual(reveal[1:2::], CLOSED(slice(1, 2)))
        self.assertEqual(reveal[:2::3], CLOSED(slice(None, 2, 3)))
        self.assertEqual(reveal[:2::], CLOSED(slice(None, 2)))

        self.assertEqual(reveal{1:2::3}, CLOSED(BRACED(slice(1, 2, 3))))
        self.assertEqual(reveal{1:2::}, CLOSED(BRACED(slice(1, 2))))
        self.assertEqual(reveal{:2::3}, CLOSED(BRACED(slice(None, 2, 3))))
        self.assertEqual(reveal{:2::}, CLOSED(BRACED(slice(None, 2))))
    
    def test_del(self):
        s = list("ABCDEFG")
        for i in range(-len(s)-2, len(s)+3):
            for j in range(-len(s)-2, len(s)+3):
                with self.subTest(i=i, j=j):
                    x = s[:]
                    y = s[:]
                    del x[i:j]
                    del y{i+1:j+1}
                    self.assertEqual(x, y)


if __name__ == "__main__":
    unittest.main()
