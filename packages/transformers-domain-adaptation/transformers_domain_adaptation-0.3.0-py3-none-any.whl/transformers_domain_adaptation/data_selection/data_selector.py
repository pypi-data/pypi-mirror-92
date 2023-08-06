from collections import Counter
from functools import reduce
from typing import List, Optional, Sequence, Set, Union, Counter as CounterType

import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import sparse
from sklearn.preprocessing import RobustScaler
from transformers import PreTrainedTokenizerFast
from sklearn.base import BaseEstimator, TransformerMixin

from transformers_domain_adaptation.type import Corpus, Token
from transformers_domain_adaptation.data_selection.metrics import (
    SIMILARITY_FEATURES,
    DIVERSITY_FEATURES,
    similarity_func_factory,
    diversity_func_factory,
)


class DataSelector(BaseEstimator, TransformerMixin):
    """Select subset of data that is likely to be beneficial for domain pre-training.

    This class is sklearn-compatible and implements the sklearn Transformers interface.
    """

    def __init__(
        self,
        keep: Union[int, float],
        tokenizer: PreTrainedTokenizerFast,
        similarity_metrics: Optional[Sequence[str]] = None,
        diversity_metrics: Optional[Sequence[str]] = None,
    ):
        """
        Args:
            keep: Quantity of documents from corpus to keep.
                  To specify number of documents, use :obj:`int`.
                  To specify percentage of documents in corpus, use :obj:`float`.
            tokenizer: A Rust-based 🤗 Tokenizer
            similarity_metrics: An optional list of similarity metrics
            diversity_metrics: An optional list of diversity metrics

        Note:
            For a list of similarity and diversity metrics, refer to :ref:`data-selection-metrics`

        Note:
            At least one similarity/diversity metric must be provided.
        """
        if isinstance(keep, int) and keep <= 0:
            raise ValueError(f"Int value for `keep` must be strictly positive.")
        if isinstance(keep, float) and not 0 <= keep <= 1:
            raise ValueError(
                f"Float value for `keep` must be between 0 and 1 (inclusive)."
            )
        if similarity_metrics is not None:
            _invalid_sim_metrics = set(similarity_metrics) - SIMILARITY_FEATURES
            if _invalid_sim_metrics:
                raise ValueError(
                    f"Invalid similarity metric(s) {_invalid_sim_metrics} found"
                )
        if diversity_metrics is not None:
            _invalid_div_metrics = set(diversity_metrics) - DIVERSITY_FEATURES
            if _invalid_div_metrics:
                raise ValueError(
                    f"Invalid diversity metric(s) {_invalid_div_metrics} found"
                )
        if similarity_metrics is None and diversity_metrics is None:
            raise ValueError(
                f"No metrics provided. Please provide at least one similarity or diversity metric."
            )

        self.keep = keep
        self.tokenizer = tokenizer
        self.similarity_metrics = similarity_metrics
        self.diversity_metrics = diversity_metrics

    def _to_term_counts(self, texts: Sequence[str]) -> List[CounterType[str]]:
        # Tokenize all documents using Rust tokenizer
        counters: List[CounterType[str]] = [
            Counter(enc.tokens)
            for enc in self.tokenizer.backend_tokenizer.encode_batch(
                texts, add_special_tokens=False
            )
        ]
        return counters

    @staticmethod
    def _to_term_dists(counters: List[CounterType[str]]) -> sparse.csr_matrix:
        vocab: Set[str] = reduce(lambda x, y: x | set(y), counters, set())
        vocab_mapping = {v: i for i, v in enumerate(vocab)}

        rows = np.array([val for i, counter in enumerate(counters) for val in [i] * len(counter)])
        cols = np.array([
            vocab_id for counter in counters for vocab_id in map(vocab_mapping.get, counter)
        ])
        data = []
        for counter in counters:
            n_elems = sum(counter.values())
            data.extend([val / n_elems for val in counter.values()])

        term_dists = sparse.csr_matrix(
            (data, (rows, cols)),
            shape=(len(counters), len(vocab)),
            dtype=np.float64,
        )
        return term_dists

    def fit(self, ft_corpus: Corpus):
        """Compute corpus-level term distribution of :obj:`ft_corpus`.

        Args:
            ft_corpus: The fine-tuning corpus. Not to be confused with
                       the domain pre-training corpus (which is used in :meth:`transform`)

        Note:
            The :obj:`ft_corpus` is treated as a single "document", which will be compared
            against other documents in the in-domain corpus in :meth:`transform`
        """
        # We cannot obtain a term distribution until we obtain the entire vocabulary of texts in `.transform`
        self.ft_term_counts_ = self._to_term_counts([' '.join(ft_corpus)])[0]
        return self

    def transform(self, docs: Corpus) -> Corpus:
        """Create a relevant subset of documents from the training corpus based on the provided data selection metrics.

        Args:
            docs: The training corpus

        Returns:
            A subset of relevant :obj:`docs` for domain pre-training
        """
        docs = [doc for doc in docs if len(doc.strip()) > 1]
        scores = self.compute_metrics(docs)
        composite_scores = scores["composite"].sort_values(ascending=False)

        n_select = (
            self.keep if isinstance(self.keep, int) else int(self.keep * len(docs))
        )
        selection_index = composite_scores.index[:n_select]
        subset_corpus = pd.Series(docs)[selection_index]

        return subset_corpus.tolist()

    def compute_metrics(self, docs: Corpus) -> pd.DataFrame:
        scores = pd.concat(
            [
                self.compute_similarities(docs),
                self.compute_diversities(docs),
            ],
            axis=1,
        )

        # Ensure metrics are normalized, before combining them into a composite score
        scores = pd.DataFrame(
            RobustScaler().fit_transform(scores), columns=scores.columns
        )
        scores["composite"] = scores.sum(axis=1)
        return scores

    def compute_similarities(self, docs: Corpus) -> pd.DataFrame:
        similarities = pd.DataFrame()  # of shape (n_docs, n_metrics)
        if (
            self.similarity_metrics is None
        ):  # Short-circuit function to avoid unnecessary computations
            return similarities

        term_counts = self._to_term_counts(docs)
        _term_dists = self._to_term_dists([self.ft_term_counts_] + term_counts)
        self.ft_term_dist_, term_dists = _term_dists[0], _term_dists[1:]

        pbar = tqdm(
            self.similarity_metrics,
            desc="computing similarity",
            unit="metric",
            dynamic_ncols=True,
        )
        for metric in pbar:
            sim_func = similarity_func_factory(metric)
            similarities[metric] = sim_func(
                term_dists, self.ft_term_dist_.toarray().reshape(1, -1)
            )

        return similarities

    def compute_diversities(self, docs: Corpus) -> pd.DataFrame:
        diversities = pd.DataFrame()  # of shape (n_docs, n_metrics)
        if self.diversity_metrics is None:
            return diversities

        tokenized_docs: List[List[Token]] = [
            enc.tokens for enc in self.tokenizer.backend_tokenizer.encode_batch(docs)
        ]

        pbar = tqdm(
            self.diversity_metrics,
            desc="computing diversity",
            unit="metric",
            dynamic_ncols=True,
        )
        for metric in pbar:
            div_func = diversity_func_factory(
                metric,
                train_term_dist=self.ft_term_dist_,
                vocab2id=self.tokenizer.vocab,
            )
            diversities[metric] = pd.Series(
                (div_func(tokenized_doc) for tokenized_doc in tokenized_docs)
            )

        return diversities
