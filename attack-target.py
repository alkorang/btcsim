"""
target manipulation by modifying timestamps - attack-target.py
Copyright (C) 2017 Yeon-Soo Kim <alkorang@outlook.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 and
only version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.
"""

import math
import pylab

class DeltaTarget:
    def __init__(self, times, delta=0):
        t = times[0]
        delayed = [t]
        for i in range(len(times) - 1):
            diff = times[i + 1] - times[i] + (delta * (i % 2))
            t += diff
            delayed.append(t)
        
        # "bits" not implemented
        self.largest_target = int("0x00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)
        self.target = self.largest_target
        self.difficulty = 1
        self.times = delayed
        self.index = 0
        
    def __iter__(self):
        self.index = 0
        self.target = self.largest_target
        self.difficulty = 1.0
        return self
    
    def __next__(self):
        if self.index >= len(self.times):
            raise StopIteration
        elif self.index == 0:
            self.index += 2016
            return self.target
        else:
            diff = self.times[self.index] - self.times[self.index - 2015]
            week = 7 * 24 * 60 * 60
            # over 4 weeks
            if diff > 4 * week:
                diff = 4 * week
            # under 0.5 weeks
            elif diff < week / 2:
                diff = week / 2
            # otherwise
            else:
                pass
            
            # calculate target/difficulty
            self.target = int(self.target * diff / (2 * week))
            if self.target > self.largest_target:
                self.target = self.largest_target
            elif self.target < 1:
                self.target = 1
            else:
                pass
            self.difficulty = self.largest_target / self.target
            self.index += 2016
            return self.target

# main
num_weeks = 500
mine_time = 9 * 60
times = [i * mine_time for i in range(0, 2016 * num_weeks)]

base = DeltaTarget(times)
lazy = DeltaTarget(times, 10)
rush = DeltaTarget(times, -10)

week = 7.0 * 24 * 60 * 60
base_x = [base.times[i] / week for i in range(0, len(base.times), 2016)]
base_y = list(map(math.log2, base))

lazy_x = [lazy.times[i] / week for i in range(0, len(lazy.times), 2016)]
lazy_y = list(map(math.log2, lazy))

rush_x = [rush.times[i] / week for i in range(0, len(rush.times), 2016)]
rush_y = list(map(math.log2, rush))

pylab.figure()
pylab.xlabel("time (week)")
pylab.ylabel("target (log2)")

pylab.plot(base_x, base_y, "b-")
pylab.plot(lazy_x, lazy_y, "g-")
pylab.plot(rush_x, rush_y, "r-")

pylab.draw()
pylab.show()
