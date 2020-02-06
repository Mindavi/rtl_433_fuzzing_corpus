# rtl\_433 fuzzing corpus

This repository is meant as a place to build a fuzzing corpus to be used against the rtl\_433 application (see https://github.com/merbanan/rtl_433).

## Quick tips

- The fdupes tool can be used to find duplicates. (`fdupes -d .` will give an interactive shell that helps decide which files to remove and which to keep)
- The afl-cmin tool (see https://github.com/google/AFL)  can be used for corpus minimization based on edge coverage.
- The afl-cov tool can help visualize coverage (https://github.com/mrash/afl-cov).
  - Keep in mind that this requires the code to be compiled with gcc <= 8.3, gcc 9 is not supported by the last lcov release (but support is available if you're will to run from the lcov master). 
