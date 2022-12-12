from rouge_score import rouge_scorer


def get_rouge(tgt_text,test_labels):
    f_measure = 0
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    for i in range(len(tgt_text)):
        f_measure = f_measure + scorer.score(tgt_text[i], test_labels[i])['rouge1'][2]
    return f_measure / len(tgt_text)
