sample_path = "data/output.txt"
answer_path = "data/answer.txt"
total_chars = 0
total_sentences = 0
exact_chars = 0
exact_sentences = 0

with open(sample_path, "r", encoding="utf-8") as sample, open(answer_path, "r", encoding="utf-8") as ans:
    sample_lines = sample.readlines()
    ans_lines = ans.readlines()

    for sample_line, ans_line in zip(sample_lines, ans_lines):
        total_chars += len(ans_line)
        total_sentences += 1

        if sample_line == ans_line:
            exact_sentences += 1
            # print(ans_line)
        
        for index in range(min(len(sample_line), len(ans_line))):
            if sample_line[index] == ans_line[index]:
                exact_chars += 1

exact_chars_rate = exact_chars / total_chars
exact_sentences_rate = exact_sentences / total_sentences

print(f"Character level accuracy: {exact_chars_rate * 100:.2f}%")
print(f"Sentence level accuracy: {exact_sentences_rate * 100:.2f}%")