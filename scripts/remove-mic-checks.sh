#!/usr/bin/env bash

# This script removes all MIC checks from the rtl_433 code and replaces them with debug logging.
# Useful for fuzzing without checksums.

sed 's/return DECODE_FAIL_MIC;/if (decoder->verbose) { fprintf(stderr, "failed MIC"); }/g' src/devices/** -i
sed 's/continue; \/\/ DECODE_FAIL_MIC/if (decoder->verbose) { fprintf(stderr, "failed MIC"); }/g' src/devices/** -i

