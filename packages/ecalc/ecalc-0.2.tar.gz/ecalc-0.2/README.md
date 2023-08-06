# NAME

ecasl - a simple Python-based calculator for network engineers/researchers.

# SYNOPSIS

  ecalc [-d] [-p #]

# DESCRIPTION

This manual page documents *ecalc*.  This program is an interactive text-based
calculator written in Python supporting GNU readline library.  *ecalc* is
specifically designed for network engineers/researchers since it can easily
handle network-related units such as bit, byte, packet, bps, and bit/s.

After invocation, *ecalc* displays a prompt "?", and ask for a user to enter
an arbitrary expression to be calculated, which must be a valid Python
expression.  *ecalc* then evaluates the expression as-is, and displays the
return value in a decimal format, followed by values in hexadecimal, octal,
and binary formats.

For typical daily use, the following mathematical functions and constants
imported from the Python standard math module would be convenient.  See
https://docs.python.org/3/library/math.html for the detail of other
mathematical functions.

- functions

  ceil, comb, copysign, fabs, factorial, floor, fmod, frexp, fsum, gcd,
  isclose, isfinite, isinf, isnan, isqrt, lcm, ldexp, modf, nextafter, perm,
  prod, remainder, trunc, ulp, exp, expml, log, loglp, log2, log10, pow, sqrt,
  asin, atan, atan2, cos, dist, hypot, sin, tan, degrees, radians, acosh,
  asinh, atanh, cosh, sinh, tanh, erf, erfc, gamma, lgamma,

- constants

  pi, e, tau, inf, nan

Note that *ecalc* supports GNU readline library, so that a user can
interactively edit his/her input with Emacs-like (user-configurable) key
bindings.  See the manual page of GNU readline library for the details.

*ecalc* understands the following units, which must be enclosed in square
brackets.

```
s            second
m            meter
bit          bit
bps          bit per second
byte, B      byte
pkt, packet  packet
```

By default, packet size is assumed to be 1,500 [byte] (i.e., the maximum
Ethernet payload size), but it can be changed by *-p* option.

*ecalc* supports the following prefixes.

```
p     pico   10**-12
n     nano   10**-9
u     micro  10**-6
m     milli  10**-3
k, K  kilo   10**3
M     mega   10**6
G     giga   10**9
T     tera   10**12
P     peta   10**15
```

In *ecalc*, the base unit is either second or byte, and all values in
other than second or byte are automatically converted.  For example,
1,000 [bit/ms] is automatically converted to 125,000 [byte/s].  See
EXAMPLES for detailed usage of *ecalc*.

# EXAMPLES

This section shows an example session with *ecalc*.

A simple arithmetic calculation:

```
? 1+2*(3+4/5)**6
%1 = 6022.872767999998
        1786 hex          13606 oct   00000000 00000000 00010111 10000110
       48.18 bit/ms   4.818e+04 bit/s        48.18 Kbit/s     0.04818 Mbit/s
       6.023 B/ms          6023 B/s          6.023 KB/s      0.006023 MB/s  
    0.004015 pkt/ms       4.015 pkt/s    1.807e+12 m        1.807e+09 km    
```

Blank spaces are arbitrary.

```
? 1 + 2 * (3 + 4 / 5) ** 6
%2 = 6022.872767999998
        1786 hex          13606 oct   00000000 00000000 00010111 10000110
       48.18 bit/ms   4.818e+04 bit/s        48.18 Kbit/s     0.04818 Mbit/s
       6.023 B/ms          6023 B/s          6.023 KB/s      0.006023 MB/s  
    0.004015 pkt/ms       4.015 pkt/s    1.807e+12 m        1.807e+09 km    
```

The previous result can be referred by "%".

```
? % + 1
%3 = 6023.872767999998
        1787 hex          13607 oct   00000000 00000000 00010111 10000111
       48.19 bit/ms   4.819e+04 bit/s        48.19 Kbit/s     0.04819 Mbit/s
       6.024 B/ms          6024 B/s          6.024 KB/s      0.006024 MB/s  
    0.004016 pkt/ms       4.016 pkt/s    1.807e+12 m        1.807e+09 km    
```

Past results can be referred by "%N".

```
? %1 - %2
%4 = 0.0
           0 hex              0 oct   00000000 00000000 00000000 00000000
           0 bit/ms           0 bit/s            0 Kbit/s           0 Mbit/s
           0 B/ms             0 B/s              0 KB/s             0 MB/s  
           0 pkt/ms           0 pkt/s            0 m                0 km    
```

Python builtin functions can be used.

```
? int(%1)
%5 = 6022
        1786 hex          13606 oct   00000000 00000000 00010111 10000110
       48.18 bit/ms   4.818e+04 bit/s        48.18 Kbit/s     0.04818 Mbit/s
       6.022 B/ms          6022 B/s          6.022 KB/s      0.006022 MB/s  
    0.004015 pkt/ms       4.015 pkt/s    1.807e+12 m        1.807e+09 km    
  ? log(sin(1) + cos(2))
%6 = -0.8549036989769139
           0 hex              0 oct   00000000 00000000 00000000 00000000
   -0.006839 bit/ms      -6.839 bit/s    -0.006839 Kbit/s  -6.839e-06 Mbit/s
  -0.0008549 B/ms       -0.8549 B/s     -0.0008549 KB/s    -8.549e-07 MB/s  
  -5.699e-07 pkt/ms  -0.0005699 pkt/s   -2.565e+08 m       -2.565e+05 km    
```

Binary, octal, and hexadecimal numbers as well as decimal numbers can be
combined.

```
? 1234 + 0b101100111 + 0o1234 + 0x1234
%7 = 6921
        1b09 hex          15411 oct   00000000 00000000 00011011 00001001
       55.37 bit/ms   5.537e+04 bit/s        55.37 Kbit/s     0.05537 Mbit/s
       6.921 B/ms          6921 B/s          6.921 KB/s      0.006921 MB/s  
    0.004614 pkt/ms       4.614 pkt/s    2.076e+12 m        2.076e+09 km    
```

Example usage of some builtin functions:

```
? sqrt(2943)
%8 = 54.249423960075376
          36 hex             66 oct   00000000 00000000 00000000 00110110
       0.434 bit/ms         434 bit/s        0.434 Kbit/s    0.000434 Mbit/s
     0.05425 B/ms         54.25 B/s        0.05425 KB/s     5.425e-05 MB/s  
   3.617e-05 pkt/ms     0.03617 pkt/s    1.627e+10 m        1.627e+07 km    
  ? abs(%)
%9 = 54.249423960075376
          36 hex             66 oct   00000000 00000000 00000000 00110110
       0.434 bit/ms         434 bit/s        0.434 Kbit/s    0.000434 Mbit/s
     0.05425 B/ms         54.25 B/s        0.05425 KB/s     5.425e-05 MB/s  
   3.617e-05 pkt/ms     0.03617 pkt/s    1.627e+10 m        1.627e+07 km    
? abs(-%)
%10 = 54.249423960075376
          36 hex             66 oct   00000000 00000000 00000000 00110110
       0.434 bit/ms         434 bit/s        0.434 Kbit/s    0.000434 Mbit/s
     0.05425 B/ms         54.25 B/s        0.05425 KB/s     5.425e-05 MB/s  
   3.617e-05 pkt/ms     0.03617 pkt/s    1.627e+10 m        1.627e+07 km    
```

Convert a transmission rate in several units:

```
? 123 [packet/ms]
%11 = 184500000.0
     aff3f20 hex     1277637440 oct   00001010 11111111 00111111 00100000
   1.476e+06 bit/ms   1.476e+09 bit/s    1.476e+06 Kbit/s        1476 Mbit/s
   1.845e+05 B/ms     1.845e+08 B/s      1.845e+05 KB/s         184.5 MB/s  
         123 pkt/ms    1.23e+05 pkt/s    5.535e+16 m        5.535e+13 km    
```

From the above result, one can see that 123 [packet/ms] is equivalent
to 1,476 [Mbit/s] with 1,500 [byte] packet.

Product of transmission rate and duration gives the total amount of
data transferred.

```
? % * 10 [s]
%12 = 1845000000.0
    6df87740 hex    15576073500 oct   01101101 11111000 01110111 01000000
   1.476e+07 bit/ms   1.476e+10 bit/s    1.476e+07 Kbit/s   1.476e+04 Mbit/s
   1.845e+06 B/ms     1.845e+09 B/s      1.845e+06 KB/s          1845 MB/s  
        1230 pkt/ms    1.23e+06 pkt/s    5.535e+17 m        5.535e+14 km    
```

Thus, if you continuosly send for 10 [s] at the transmission rate of
123 [packet/ms], the total volume transferred is 1,845 [MB].

Data size divided by duration gives the transmission rate.

```
? 6.4[Gbyte]/120[s]
%13 = 53333333.333333336
     32dcd55 hex      313346525 oct   00000011 00101101 11001101 01010101
   4.267e+05 bit/ms   4.267e+08 bit/s    4.267e+05 Kbit/s       426.7 Mbit/s
   5.333e+04 B/ms     5.333e+07 B/s      5.333e+04 KB/s         53.33 MB/s  
       35.56 pkt/ms   3.556e+04 pkt/s      1.6e+16 m          1.6e+13 km    
```

So, if 6.4 [Gbyte] is trensferred in 120 [s], the transmission rate of
the network is 426.7 [Mbit/s].

Calculating the bandwidth-delay product:

```
? 64[packet] * 1200[ms]
%14 = 115200.0
       1c200 hex         341000 oct   00000000 00000001 11000010 00000000
       921.6 bit/ms   9.216e+05 bit/s        921.6 Kbit/s      0.9216 Mbit/s
       115.2 B/ms     1.152e+05 B/s          115.2 KB/s        0.1152 MB/s  
      0.0768 pkt/ms        76.8 pkt/s    3.456e+13 m        3.456e+10 km    
```

which indicates that, for instance, the TCP socket buffer of 11.52
[KB] is at least required for TCP window flow control with its window
size of 64 [packet] and the round-trip time of 120 [ms].

Values in meters are converted to seconds --- time to need to travel in
the speed of the light.

```
? 128[km]
%15 = 0.00042666666666666667
           0 hex              0 oct   00000000 00000000 00000000 00000000
   3.413e-06 bit/ms    0.003413 bit/s    3.413e-06 Kbit/s   3.413e-09 Mbit/s
   4.267e-07 B/ms     0.0004267 B/s      4.267e-07 KB/s     4.267e-10 MB/s  
   2.844e-10 pkt/ms   2.844e-07 pkt/s     1.28e+05 m              128 km    
```

which shows the light travels 128 [km] in 0.000426 [s].

Conversely, values in seconds are displayed in meters.

```
? 0.0012[ms]
%16 = 1.2e-06
           0 hex              0 oct   00000000 00000000 00000000 00000000
     9.6e-09 bit/ms     9.6e-06 bit/s      9.6e-09 Kbit/s     9.6e-12 Mbit/s
     1.2e-09 B/ms       1.2e-06 B/s        1.2e-09 KB/s       1.2e-12 MB/s  
       8e-13 pkt/ms       8e-10 pkt/s          360 m             0.36 km    
```

So, one can see that the light travels 0.36 [km] in 0.0012 [ms].

# AVAILABILITY

The latest version of *ecalc* is available at 

# AUTHOR

Hiroyuki Ohsaki <ohsaki[atmark]lsnl.jp>
