#!/usr/bin/env sh
qary -s qa < qary/data/testsets/test_questions.txt > qary/data/testsets/test_questions.output.txt
diff qary/data/testsets/test_questions.solution.txt qary/data/testsets/test_questions.output.txt
