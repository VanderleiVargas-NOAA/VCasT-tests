#!/bin/bash
# Loop over thresholds and lead values.
for threshold in 20 30 40 50; do
  for lead in 9 25 81 361 729; do
    out_file="agg_${threshold}_${lead}.data"
    pattern=$'\t'"$lead"$'\t'
    echo "Creating file $out_file with threshold >=${threshold} and pattern $pattern"
    
    # Write the header (first line) and then append filtered lines from line 2 onward.
    ( head -n 1 agg.data; tail -n +2 agg.data | grep ">=$threshold" | grep "$pattern" ) > "$out_file"
  done
done

